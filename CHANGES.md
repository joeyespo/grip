Grip Changelog
==============


Version 2.0.0 (2013-09-26)
--------------------------

- Feature: Styles are now cached (from the not-yet-released offline rendering) (thanks, [@isbadawi][]!)
- Feature: Add user/pass options for GitHub auth (thanks, [@joelittlejohn][]!)
- Feature: Add support for rendering images (thanks, [@jgallagher][]!)
- Feature: Add export to single HTML file (thanks, [@iliggio][]!)
- Enhancement: Better HTML titles by normalizing the path, always providing a title
- Enhancement: Allow styles to be overridden, with examples in static directory
- Enhancement: Relay GitHub API HTTP errors to browser for debuggability
- Enhancement: Extract render_app and add create_app in API
- Bugfix: Fix manual installs using setup.py (thanks, [@briancappello][]!)
- Bugfix: Handle File Not Found errors as 404 when given a directory
- Rename and re-arrange the configuration files
- Update README.md with new features
- Update AUTHORS.md format
- Upgrade requirements
- Simplify code


Version 1.2.0 (2013-03-17)
--------------------------

- Add AUTHORS.md for attributing credit.
- Feature: Can now click hyperlinks to render other files
  without re-running (thanks, [@vladwing][]!)
- Update GitHub CSS regular expression.


Version 1.1.1 (2013-01-05)
--------------------------

- Upgrade path-and-address.
- Use exact versions in requirements.


Version 1.1 (2013-01-04)
------------------------

- Readme: Clarify and add examples.
- Bugfix: Typo in requirements.
- Clean up setup.py


Version 1.0 (2012-12-08)
------------------------

- CLI: now accepts an address, not just a port.
- CLI: now accepts --gfm and --context=<repo> arguments for rendering
  GitHub Flavored Markdown.
- API: `serve` function now accepts `None` for its arguments to
  indicate 'use default'.
- API: `serve` function now accepts a 'host'.
- API: `serve` now resolves the default file when given a path.
- Now using docopt for more advanced argument processing.
- Now using path-and-address for humanistic path / address handling.


Version 0.2.1 (2012-12-02)
--------------------------

- Issue #5: Fixed the installer to work in the case where
  the requirements are not already installed.


Version 0.2 (2012-12-01)
------------------------

- Github styles are now retrieved dynamically when run,
  instead of using the outdated styles from the config.


Version 0.1.1 (2012-11-20)
--------------------------

- Added the port command-line argument.


Version 0.1 (2012-11-19)
------------------------

First public preview release.


[@vladwing]: https://github.com/vladwing
[@isbadawi]: https://github.com/isbadawi
[@joelittlejohn]: https://github.com/joelittlejohn
[@briancappello]: https://github.com/briancappello
[@jgallagher]: https://github.com/jgallagher
[@iliggio]: https://github.com/iliggio
