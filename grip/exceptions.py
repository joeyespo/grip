import errno
try:
    NotFoundError = FileNotFoundError
except NameError:
    NotFoundError = IOError


class AlreadyRunningError(RuntimeError):
    pass


class ReadmeNotFoundError(NotFoundError):
    """
    This class inherits from FileNotFoundError on Python 3 and above.
    """
    def __init__(self, path=None, message=None):
        self.path = path
        self.message = message
        super(ReadmeNotFoundError, self).__init__(
            errno.ENOENT, 'README not found', path)

    def __repr__(self):
        return '{0}({!r}, {!r})'.format(
            type(self).__name__, self.path, self.message)

    def __str__(self):
        if self.message:
            return self.message

        if self.path is not None:
            return 'No README found at {0}'.format(self.path)

        return self.strerror
