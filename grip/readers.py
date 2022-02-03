from __future__ import print_function, unicode_literals

import errno
import io
import mimetypes
import os
import posixpath
import sys
from abc import ABCMeta, abstractmethod

from ._compat import safe_join

from .constants import DEFAULT_FILENAMES, DEFAULT_FILENAME
from .exceptions import ReadmeNotFoundError
from .vendor.six import add_metaclass


@add_metaclass(ABCMeta)
class ReadmeReader(object):
    """
    Reads Readme content from a URL subpath.
    """
    def __init__(self):
        super(ReadmeReader, self).__init__()

    def normalize_subpath(self, subpath):
        """
        Returns the normalized subpath.

        This allows Readme files to be inferred from directories while
        still allowing relative paths to work properly.

        Override to change the default behavior of returning the
        specified subpath as-is.
        """
        if subpath is None:
            return None

        return posixpath.normpath(subpath)

    def filename_for(self, subpath):
        """
        Returns the relative filename for the specified subpath, or None
        if the file does not exist.
        """
        return None

    def mimetype_for(self, subpath=None):
        """
        Gets the mimetype for the specified subpath.
        """
        if subpath is None:
            subpath = DEFAULT_FILENAME
        mimetype, _ = mimetypes.guess_type(subpath)
        return mimetype

    def is_binary(self, subpath=None):
        """
        Gets whether the specified subpath is a supported binary file.
        """
        return False

    def last_updated(self, subpath=None):
        """
        Returns the time of the last modification of the Readme or
        specified subpath. None is returned if the reader doesn't
        support modification tracking.

        The format of return value is dependent on the implementing
        reader. It can be any object as long as equality indicates
        that the content was not updated.
        """
        return None

    @abstractmethod
    def read(self, subpath=None):
        """
        Returns the UTF-8 content of the specified subpath, or None if
        subpath does not exist.
        """
        pass


class DirectoryReader(ReadmeReader):
    """
    Reads Readme files from URL subpaths.
    """
    def __init__(self, path=None, silent=False):
        super(DirectoryReader, self).__init__()
        root_filename = os.path.abspath(self._resolve_readme(path, silent))
        self.root_filename = root_filename
        self.root_directory = os.path.dirname(root_filename)

    def _find_file(self, path, silent=False):
        """
        Gets the full path and extension, or None if a README file could not
        be found at the specified path.
        """
        for filename in DEFAULT_FILENAMES:
            full_path = os.path.join(path, filename) if path else filename
            if os.path.exists(full_path):
                return full_path

        # Return default filename if silent
        if silent:
            return os.path.join(path, DEFAULT_FILENAME)

        raise ReadmeNotFoundError(path)

    def _resolve_readme(self, path=None, silent=False):
        """
        Returns the path if it's a file; otherwise, looks for a compatible
        README file in the directory specified by path.

        If path is None, the current working directory is used.

        If silent is set, the default relative filename will be returned
        if path is a directory or None if it does not exist.

        Raises ReadmeNotFoundError if no compatible README file can be
        found and silent is False.
        """
        # Default to current working directory
        if path is None:
            path = '.'

        # Normalize the path
        path = os.path.normpath(path)

        # Resolve README file if path is a directory
        if os.path.isdir(path):
            return self._find_file(path, silent)

        # Return path if file exists or if silent
        if silent or os.path.exists(path):
            return path

        raise ReadmeNotFoundError(path, 'File not found: ' + path)

    def _read_text(self, filename):
        """
        Helper that reads the UTF-8 content of the specified file, or
        None if the file doesn't exist. This returns a unicode string.
        """
        with io.open(filename, 'rt', encoding='utf-8') as f:
            return f.read()

    def _read_binary(self, filename):
        """
        Helper that reads the binary content of the specified file, or
        None if the file doesn't exist. This returns a byte string.
        """
        with io.open(filename, 'rb') as f:
            return f.read()

    def normalize_subpath(self, subpath):
        """
        Normalizes the specified subpath, or None if subpath is None.

        This allows Readme files to be inferred from directories while
        still allowing relative paths to work properly.

        Raises werkzeug.exceptions.NotFound if the resulting path
        would fall out of the root directory.
        """
        if subpath is None:
            return None

        # Normalize the subpath
        subpath = posixpath.normpath(subpath)

        # Add or remove trailing slash to properly support relative links
        filename = os.path.normpath(safe_join(self.root_directory, subpath))
        if os.path.isdir(filename):
            subpath += '/'

        return subpath

    def readme_for(self, subpath):
        """
        Returns the full path for the README file for the specified
        subpath, or the root filename if subpath is None.

        Raises ReadmeNotFoundError if a README for the specified subpath
        does not exist.

        Raises werkzeug.exceptions.NotFound if the resulting path
        would fall out of the root directory.
        """
        if subpath is None:
            return self.root_filename

        # Join for safety and to convert subpath to normalized OS-specific path
        filename = os.path.normpath(safe_join(self.root_directory, subpath))

        # Check for existence
        if not os.path.exists(filename):
            raise ReadmeNotFoundError(filename)

        # Resolve README file if path is a directory
        if os.path.isdir(filename):
            return self._find_file(filename)

        return filename

    def filename_for(self, subpath):
        """
        Returns the relative filename for the specified subpath, or the
        root filename if subpath is None.

        Raises werkzeug.exceptions.NotFound if the resulting path
        would fall out of the root directory.
        """
        try:
            filename = self.readme_for(subpath)
            return os.path.relpath(filename, self.root_directory)
        except ReadmeNotFoundError:
            return None

    def is_binary(self, subpath=None):
        """
        Gets whether the specified subpath is a supported binary file.
        """
        mimetype = self.mimetype_for(subpath)
        return mimetype and not mimetype.startswith('text/')

    def last_updated(self, subpath=None):
        """
        Returns the time of the last modification of the Readme or
        specified subpath, or None if the file does not exist.

        The return value is a number giving the number of seconds since
        the epoch (see the time module).

        Raises werkzeug.exceptions.NotFound if the resulting path
        would fall out of the root directory.
        """
        try:
            return os.path.getmtime(self.readme_for(subpath))
        except ReadmeNotFoundError:
            return None
        # OSError for Python 3 base class, EnvironmentError for Python 2
        except (OSError, EnvironmentError) as ex:
            if ex.errno == errno.ENOENT:
                return None
            raise

    def read(self, subpath=None):
        """
        Returns the UTF-8 content of the specified subpath.

        subpath is expected to already have been normalized.

        Raises ReadmeNotFoundError if a README for the specified subpath
        does not exist.

        Raises werkzeug.exceptions.NotFound if the resulting path
        would fall out of the root directory.
        """
        is_binary = self.is_binary(subpath)
        filename = self.readme_for(subpath)
        try:
            if is_binary:
                return self._read_binary(filename)
            return self._read_text(filename)
        # OSError for Python 3 base class, EnvironmentError for Python 2
        except (OSError, EnvironmentError) as ex:
            if ex.errno == errno.ENOENT:
                raise ReadmeNotFoundError(filename)
            raise


class TextReader(ReadmeReader):
    """
    Reads Readme content from the provided unicode string.
    """
    def __init__(self, text, display_filename=None):
        super(TextReader, self).__init__()
        self.text = text
        self.display_filename = display_filename

    def filename_for(self, subpath):
        """
        Returns the display filename, or None if subpath is specified
        since subpaths are not supported for text readers.
        """
        if subpath is not None:
            return None

        return self.display_filename

    def read(self, subpath=None):
        """
        Returns the UTF-8 Readme content.

        Raises ReadmeNotFoundError if subpath is specified since
        subpaths are not supported for text readers.
        """
        if subpath is not None:
            raise ReadmeNotFoundError(subpath)

        return self.text


class StdinReader(TextReader):
    """
    Reads Readme text from STDIN.
    """
    def __init__(self, display_filename=None):
        super(StdinReader, self).__init__(None, display_filename)

    def read(self, subpath=None):
        """
        Returns the UTF-8 Readme content.

        Raises ReadmeNotFoundError if subpath is specified since
        subpaths are not supported for text readers.
        """
        # Lazily read STDIN
        if self.text is None and subpath is None:
            self.text = self.read_stdin()

        return super(StdinReader, self).read(subpath)

    def read_stdin(self):
        """
        Reads STDIN until the end of input and returns a unicode string.
        """
        text = sys.stdin.read()

        # Decode the bytes returned from earlier Python STDIN implementations
        if sys.version_info[0] < 3 and text is not None:
            text = text.decode(sys.stdin.encoding or 'utf-8')

        return text
