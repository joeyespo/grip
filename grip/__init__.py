"""\
Grip

Preview your readme files with the Github mockup renderers.
"""

import command
from .server import serve
from .renderer import render_content, render_page
from .watcher import find_readme

__all__ = ['command', 'serve', 'render_content', 'render_page', 'find_readme']
__version__ = '0.1'
__description__ = '\n\n'.join(__doc__.split('\n\n')[1:])
