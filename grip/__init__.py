"""\
Grip
----

Render local readme files before sending off to Github.

:copyright: (c) 2012 by Joe Esposito.
:license: MIT, see LICENSE for more details.
"""

__version__ = '0.2.1'


from . import command
from .server import serve
from .renderer import render_content, render_page
from .watcher import find_readme
