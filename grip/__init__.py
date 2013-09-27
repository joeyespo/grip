"""\
Grip
----

Render local readme files before sending off to Github.

:copyright: (c) 2012 by Joe Esposito.
:license: MIT, see LICENSE for more details.
"""

__version__ = '2.0.0'


from . import command
from .renderer import render_content, render_page
from .server import default_filenames, create_app, serve
from .exporter import export
