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

:copyright: (c) 2012 by Joe Esposito.
:license: MIT, see LICENSE for more details.
"""

__title__ = 'grip'
__version__ = '0.2'
__author__ = 'Joe Esposito'
__description__ = '\n\n'.join(__doc__.split('\n\n')[1:]).split('\n\n\n')[0]
__copyright__ = 'Copyright 2012 Joe Esposito'
__license__ = 'MIT'


from . import command
from .server import serve
from .renderer import render_content, render_page
from .watcher import find_readme
