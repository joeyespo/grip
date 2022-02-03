# TODO: Use Werkzeug's directly after dropping support for older Flask versions
try:
    # Use older Flask implementation directly to ensure backwards compatibility
    from flask import safe_join
except ImportError:
    import werkzeug.utils
    from werkzeug.exceptions import NotFound

    # Use port of Flask 2.0 safe_join to match behavior
    def safe_join(directory, *pathnames):
        """Safely join zero or more untrusted path components to a base
        directory to avoid escaping the base directory.

        :param directory: The trusted base directory.
        :param pathnames: The untrusted path components relative to the
            base directory.
        :return: A safe path.
        """
        path = werkzeug.utils.safe_join(directory, *pathnames)

        if path is None:
            raise NotFound()

        return path


__all__ = ['safe_join']
