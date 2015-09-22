import os

from flask import Flask

from .constants import default_static_url_path


# TODO: Refactor the internals of Grip to use this class in order
#       to organize state and for overriding behavior


class Grip(Flask):
    """
    The Grip server application.
    """
    def __init__(self, instance_path=None, static_url_path=None):
        if instance_path is None:
            instance_path = os.path.abspath(os.path.expanduser('~/.grip'))
        if static_url_path is None:
            static_url_path = default_static_url_path

        # Flask application
        super(Grip, self).__init__(__name__,
                                   static_url_path=static_url_path,
                                   instance_path=instance_path)

        # Load grip settings and local dev settings
        self.config.from_object('grip.settings')
        self.config.from_pyfile('settings_local.py', silent=True)

        # Load user instance settings
        user_settings = os.path.join(instance_path, 'settings.py')
        self.config.from_pyfile(user_settings, silent=True)
