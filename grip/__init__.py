"""\
Grip
----

Render local readme files before sending off to GitHub.

:copyright: (c) 2014 by Joe Esposito.
:license: MIT, see LICENSE for more details.
"""

__version__ = '3.0.0'


from . import command
from .constants import supported_extensions, default_filenames
from .server import create_app, serve, clear_cache
from .renderer import render_content
from .exporter import export
