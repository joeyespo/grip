import os


def find_readme(directory='.', readme_file='README'):
    """Returns the readme filename at the specified directory, or None."""
    for filename in os.listdir(directory):
        if os.path.splitext(filename.lower())[0] == readme_file.lower():
            return os.path.join(os.path.abspath(directory), filename)
    return None


def read_file(filename):
    """Reads the contents of the specified file."""
    with open(filename) as f:
        return f.read()
