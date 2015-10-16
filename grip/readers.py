from __future__ import print_function, unicode_literals

import errno
import io
import mimetypes
import os
import posixpath
import sys
from abc import ABCMeta, abstractmethod

from flask import safe_join

from .constants import DEFAULT_FILENAMES
from .resolver import find_file


class ReadmeReader(object):
    """
    Reads Readme content from a URL subpath.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        super(ReadmeReader, self).__init__()

    def normalize(self, subpath):
        """
        Returns the normalized subpath.

        This allows Readme files to be inferred from directories while
        still allowing relative paths to work properly.

        This returns subpath as-is, implying that no subpaths are
        identical by default.
        """
        return subpath

    def filename_for(self, subpath):
        """
        Returns the full relative filename for the specified subpath,
        or None if the file does not exist.
        """
        return subpath

    def mimetype_for(self, subpath=None):
        """
        Gets the mimetype for the specified subpath.
        """
        if subpath is None:
            return None

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
        Returns the UTF-8 content of the normalized subpath, or None if
        subpath does not exist.
        """
        pass


class DirectoryReader(ReadmeReader):
    """
    Reads Readme files from URL subpaths.
    """
    def __init__(self, path=None):
        super(DirectoryReader, self).__init__()
        self.path = path
        # TODO: Resolve in_filename
        in_filename = path
        self.filename = in_filename
        self.directory = os.path.dirname(in_filename)

    def read_text_file(self, filename):
        """
        Helper that reads the UTF-8 content of the specified file, or
        None if the file doesn't exist. This returns a unicode string.
        """
        try:
            with io.open(filename, 'rt', encoding='utf-8') as f:
                return f.read()
        except IOError as ex:
            if ex.errno == errno.ENOENT:
                return None
            raise

    def read_binary_file(self, filename):
        """
        Helper that reads the binary content of the specified file, or
        None if the file doesn't exist. This returns a byte string.
        """
        try:
            with io.open(filename, 'rb') as f:
                return f.read()
        except IOError as ex:
            if ex.errno == errno.ENOENT:
                return None
            raise

    def normalize(self, subpath):
        """
        Normalizes the specified subpath, or None if subpath is None.
        """
        if subpath is None:
            return None

        # Resolve filename
        filename = safe_join(self.directory, self.filename_for(subpath))
        if not os.path.isdir(filename):
            return subpath.rstrip('/')
        elif not subpath.endswith('/'):
            return subpath + '/'

        return subpath

    def filename_for(self, subpath):
        """
        Returns the relative filename for the specified subpath.
        """
        if subpath is None:
            return self.filename

        # Convert URL path to OS-specific path
        return os.path.join(*posixpath.split(subpath))

    def last_updated(self, subpath=None):
        """
        Returns the time of the last modification of the Readme or
        specified subpath. None is returned if the reader doesn't
        support modification tracking.

        The return value is a number giving the number of seconds since
        the epoch (see the time module).
        """
        # TODO: Validate / normalize subpath?
        return os.path.getmtime(
            subpath if subpath is not None else self.filename)

    def is_binary(self, subpath=None):
        """
        Gets whether the specified subpath is a supported binary file.
        """
        mimetype = self.mimetype_for(subpath)
        return mimetype and mimetype.startswith('image/')

    def read(self, subpath=None):
        """
        Returns the UTF-8 content of the normalized subpath, or None if
        subpath does not exist.
        """
        if subpath is None:
            return self.read_text_file(self.filename)

        # Resolve filename
        filename = safe_join(self.directory, self.filename_for(subpath))
        if os.path.isdir(filename):
            filename = find_file(filename)
            if filename is None:
                return None

        # Read UTF-8 text or binary file
        is_text = not self.is_binary(subpath)
        return (self.read_text_file(filename)
                if is_text
                else self.read_binary_file(filename))


class TextReader(ReadmeReader):
    """
    Reads Readme content from STDIN.
    """
    def __init__(self, text):
        super(TextReader, self).__init__()
        self.text = text

    def filename_for(self, subpath):
        """
        Returns None.
        """
        return DEFAULT_FILENAMES[0] if not subpath else None

    def read(self, subpath=None):
        """
        Returns the UTF-8 Readme content, or None if subpath is specified.
        """
        if subpath is not None:
            return None, None
        # TODO: Delete this
        if hasattr(self.text, 'read'):
            return self.text.read(), None
        return str(self.text), None


class StdinReader(TextReader):
    """
    Reads Readme text from STDIN.
    """
    def __init__(self):
        # Handle debug mode special case
        if self.config['DEBUG_GRIP']:
            text = (os.environ['GRIP_STDIN_TEXT']
                    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
                    else sys.stdin.read())
            if not os.environ.get('WERKZEUG_RUN_MAIN'):
                os.environ['GRIP_STDIN_TEXT'] = text
        else:
            text = sys.stdin.read()

        super(StdinReader, self).__init__(text)
