
import os, getpass

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var.upper().replace("-", "_")] = getpass.getpass(f"{var}:")

def print_env(var: str):
    print(os.environ.get(var))

print_env("FAKE_PASSWORD")