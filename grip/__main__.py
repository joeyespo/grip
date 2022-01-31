"""\
Grip
----

Render local readme files before sending off to GitHub.

:copyright: (c) 2014-2022 by Joe Esposito.
:license: MIT, see LICENSE for more details.
"""

import os
import sys


if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))

    from grip.command import main
    main()
