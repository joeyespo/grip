"""\
Grip
----

Render local readme files before sending off to Github.


Grip is easy to set up
``````````````````````

::

    $ pip install grip
    $ cd myproject
    $ grip
     * Running on http://localhost:5000/


Links
`````

* `Website <http://github.com/joeyespo/grip/>`_
"""

import command
from .server import serve
from .renderer import render_content, render_page
from .watcher import find_readme

__all__ = ['command', 'serve', 'render_content', 'render_page', 'find_readme']

__version__ = '0.1.1'
__description__ = '\n\n'.join(__doc__.split('\n\n')[1:]).split('\n\n\n')[0]
