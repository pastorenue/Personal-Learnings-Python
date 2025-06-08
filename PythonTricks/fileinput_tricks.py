import fileinput

def read_all_files(files: list=[]):
    for line in fileinput.input(files):
        yield line

generator_read = read_all_files(["file1.csv", "file2.csv"])
for line in generator_read:
    print(line)
# print(generator_read)