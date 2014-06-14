"""\
Grip
----

Render local readme files before sending off to Github.

:copyright: (c) 2014 by Joe Esposito.
:license: MIT, see LICENSE for more details.
"""

__version__ = '2.0.0'


from . import command
from .constants import supported_extensions, default_filenames
from .renderer import render_content, render_page
from .server import create_app, serve
from .exporter import export
