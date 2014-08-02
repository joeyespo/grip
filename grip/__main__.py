"""\
Grip
----

Render local readme files before sending off to Github.

:copyright: (c) 2014 by Joe Esposito.
:license: MIT, see LICENSE for more details.
"""

import os
import sys


if __name__ == '__main__':
    sys.path.append(os.path.dirname(__file__))

    from grip.command import main
    main()
