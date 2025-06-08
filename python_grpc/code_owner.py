import os
import logging
from typing import Optional
import git
import argparse

from dataclasses import dataclass
from collections import defaultdict, Counter

log = logging.getLogger(__name__)

ACTIVE_CONTRIBUTORS = [
    "benjamin.idewor@momox.biz"
    "emmanuel.pastor@momox.biz",
    "feroz.khan@momox.biz",
    "hesam.fatemi@momox.biz",
    "min.ke@momox.biz",
    "tobias.doersch@momox.biz",
]
GIT_TRACEABLE_FILE_SUFFIX = (".py", ".sh", ".sql", ".js", ".ts", ".json", ".cfg", ".txt")
MAX_PRINT_CHUNK = 25

@dataclass
class CodeOwnersGenerator:
    repo_path: str
    directory_to_scan: str

    def __post_init__(self):
        self.repo = git.Repo(self.repo_path)
        self.code_owner_file_path = os.path.join(self.repo_path, 'CODEOWNERS')

    def execute(self, read_only: bool = False):
        if read_only:
            content = self.generate_code_owners()
            CodeOwnersGenerator.print_in_chunks(content)
        else:
            print(f"Generating CODEOWNERS file for {self.repo_path}")
            self.write_file(self.generate_code_owners())

    @staticmethod
    def print_in_chunks(text: str, lines_per_chunk: int=MAX_PRINT_CHUNK) -> None:
        print("Generating CODEOWNERS for in read-only mode")
        print("----++++++++-----" * 5)
        lines = text.splitlines()
        try:
            terminal_height = os.get_terminal_size().lines
        except OSError:
            terminal_height = lines_per_chunk
        
        chunk_size = min(terminal_height, lines_per_chunk)
        for i in range(0, len(lines), chunk_size):
            print("\n".join(lines[i:i+chunk_size]))
            if i + chunk_size < len(lines):
                _ = input("Press Enter to continue...")

    def generate_code_owners(self) -> str:
        owner_map = self.get_owner_map()
        file_content: str = ""
        for top_level_directory, files in owner_map.items():
            file_content += f"[{top_level_directory}]\n"
            for file_path, owners in files.items():
                owners_str = ' '.join([f"@{owner}" for owner in owners])
                file_content += f"/{file_path} {owners_str}\n"
            file_content += "\n"

        return file_content

    def write_file(self, content: str) -> None:
        with open(self.code_owner_file_path, 'w') as f:
            f.write(content)

        print("CodeOwners generated successfully!")

    def get_owner_map(self) -> defaultdict:
        """Returns a nested dictionary that maps top-level directories and file paths to a set of owners.

        Returns:
            defaultdict: A nested dictionary where the keys are top-level directories, the values are dictionaries
            where the keys are file paths, and the values are sets of owners.
        """
        owner_map: defaultdict = defaultdict(lambda: defaultdict(set))
        repo_tree_generator = os.walk(os.path.join(self.repo_path, self.directory_to_scan))
        for root, _, files in repo_tree_generator:
            for file in files:
                if not self._is_git_traceable(file):
                    continue
                try:
                    owners, top_level_directory, file_path = self._extract_owners(root, file)
                    if not owners:
                        continue
                    
                    for owner in owners:
                        owner_map[top_level_directory][file_path].add(owner)
                except Exception as e:
                    log.error(f"Failed to extract owners for {file}: {e}")
        return owner_map

    def _is_git_traceable(self, file: str) -> bool:
        """Checks if a file is traceable by Git.

        Args:
            file (str): The name of the file to check.
        Returns:
            bool: True if the file is traceable, False otherwise.
        """
        return file.endswith(GIT_TRACEABLE_FILE_SUFFIX) or file == "Dockerfile" or file == "crontab"

    def _extract_owners(self, root, file):
        file_path = os.path.relpath(os.path.join(root, file), self.repo_path)
        top_level_directory = (
            file_path.split(os.sep)[1] if len(file_path.split(os.sep)) > 1
            else file_path.split(os.sep)[0]
        )
        owners = self.get_code_owners(file_path)
        if owners:
            return owners, top_level_directory, file_path

        return None, None, None

    def get_code_owners(self, file_path):

        top_contributors = self.get_top_contributors(file_path)
        if top_contributors:
            return [
                top_contributor
                for top_contributor in top_contributors
                if top_contributor in ACTIVE_CONTRIBUTORS
            ]

        return None

    def get_top_contributors(self, file_path: str) -> Optional[list]:
        try:
            # Check if the file exists in the repository
            if file_path not in self.repo.git.ls_tree('HEAD', file_path):
                return None

            # Run git blame on the file
            blame_info = self.repo.blame('HEAD', file_path)
            if blame_info:
                return self._get_contributors_from_blame_info(blame_info)
        except git.exc.GitCommandError as e:
            if 'no such path' in str(e):
                log.warning(f"File {file_path} does not exist in HEAD")
            else:
                raise Exception(f"Error processing file {file_path}: {e}")
    
    def _get_contributors_from_blame_info(self, blame_info) -> Optional[list]:
        """Get the top contributors from the blame information.

        Args:
            blame_info (list): A list of blame information containing commit details.
        Returns:
            list: A list of top contributors based on the frequency of their commits.
        """
        # Count the frequency of each contributor by commit
        contributors = [commits[0].author.email for commits in blame_info]
        if contributors:
            contributors_counter = Counter(contributors).most_common(3)
            top_contributors = [contributor[0] for contributor in contributors_counter]
            return top_contributors

        return None

def main(repo_path: str = ".", directory_to_scan: str = ".", read_only: bool = False):
    # Generate code to get args from the command line
    try:
        generator = CodeOwnersGenerator(repo_path=repo_path, directory_to_scan=directory_to_scan)
        generator.execute(read_only)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    # Execute the code
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_path", type=str, action="store", help="Path to the repository")
    parser.add_argument("directory_to_scan", type=str, action="store", help="Directory in the repository to scan for code owners.")
    parser.add_argument("--read_only", action="store_true", help="Generate code owners in read-only mode")
    args = parser.parse_args()
    read_only = args.read_only
    repo_path = args.repo_path
    directory_to_scan = args.directory_to_scan
    main(repo_path, directory_to_scan, read_only)
