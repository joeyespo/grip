import os

from .constants import DEFAULT_FILENAME, DEFAULT_FILENAMES


def find_file(path):
    """
    Gets the full path and extension, or None if a README file could not
    be found at the specified path.
    """
    if path is None:
        path = '.'
    for filename in DEFAULT_FILENAMES:
        full_path = os.path.join(path, filename) if path else filename
        if os.path.exists(full_path):
            return full_path
    return None


def resolve_readme(path=None, force=False):
    """
    Returns the path if it's a file; otherwise, looks for a compatible
    README file in the directory specified by path.

    If path is None, the current working directory is used.

    If force is set, the default relative filename will be returned if
    path is a directory or None, even if it does not exist.

    Raises ValueError if no compatible README file can be found.
    """
    if not path or os.path.isdir(path):
        path = find_file(path)
        if path is None:
            if force:
                return DEFAULT_FILENAME
            raise ValueError('No README found at ' + path)
    if not os.path.exists(path) and not force:
        raise ValueError('File not found: ' + path)
    return os.path.normpath(path)
