"""
Tests the Grip command-line interface.
"""

from __future__ import print_function, unicode_literals

import sys
from subprocess import PIPE, STDOUT, CalledProcessError, Popen

import pytest

from grip.command import usage, version


if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    class CalledProcessError(CalledProcessError):
        def __init__(self, returncode, cmd, output):
            super(CalledProcessError, self).__init__(returncode, cmd)
            self.output = output


def run(*args, **kwargs):
    command = kwargs.pop('command', 'grip')
    stdin = kwargs.pop('stdin', None)

    cmd = [command] + list(args)
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
              universal_newlines=True)
    # Sent input as STDIN then close it
    output, _ = p.communicate(input=stdin)
    p.stdin.close()
    # Wait for process to terminate
    returncode = p.wait()
    # Raise exception on failed process calls
    if returncode != 0:
        raise CalledProcessError(returncode, cmd, output=output)
    return output


def test_help():
    assert run('-h') == usage
    assert run('--help') == usage


def test_version():
    assert run('-V') == version + '\n'
    assert run('--version') == version + '\n'


def test_bad_command():
    simple_usage = '\n\n'.join(usage.split('\n\n')[:1])
    with pytest.raises(CalledProcessError) as excinfo:
        run('--does-not-exist')
    assert excinfo.value.output == simple_usage + '\n'


# TODO: Figure out how to run the CLI and still capture requests
# TODO: Test all Grip CLI commands and arguments
# TODO: Test settings wire-up (settings.py, settings_local.py, ~/.grip)

# TODO: Test `cat README.md | ~/.local/bin/grip - --export -` (#152)
