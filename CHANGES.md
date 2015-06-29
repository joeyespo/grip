Grip Changelog
--------------


#### Version 3.3.0 (2015-06-28)

- Enhancement: Add `GRIPHOME` environment variable for alternative `settings.py` locations ([#117](https://github.com/joeyespo/grip/pull/117) - thanks, [@zmwangx][]!)
- Enhancement: Allow alternative github API URL ([#119](https://github.com/joeyespo/grip/pull/119) - thanks, [@dandavison][]!)
- Enhancement: Change the default port to `6419` to avoid conflicts ([#124](https://github.com/joeyespo/grip/pull/124))
- Enhancement: Automatically open grip in a new tab in browser ([122](https://github.com/joeyespo/grip/pull/122) - thanks, [@ssundarraj][]!)
- Enhancement: Only cache styles and assets if all downloads are successful
- Enhancement: Add `--title` option to manually set the title on the rendered page ([#125](https://github.com/joeyespo/grip/pull/125) - thanks, [@jlhonora][]!)
- Enhancement: Render tables and lists in `render_offline` mode ([#133](https://github.com/joeyespo/grip/pull/133) - thanks, [@akawhy][]!)
- Bugfix: Don't print info messages to `STDOUT` for when exporting to `STDOUT` ([#101](https://github.com/joeyespo/grip/issues/101))
- Bugfix: Don't swallow system exceptions
- Bugfix: Use list builder notation instead of `map` to get `default_filenames` to evaluate it to non-empty on Python 3
- Bugfix: Fix asset retrieval on both Python 2 and 3
- Bugfix: Fix `InsecureRequestWarning` problems ([#111](https://github.com/joeyespo/grip/issues/111), [#128](https://github.com/joeyespo/grip/issues/128))
- Bugfix: Fix missing Octicons by properly downloading assets as binary files ([#127](https://github.com/joeyespo/grip/issues/127))
- Bugfix: Add trailing slashes to directories and remove them for files so so relative links are correct ([#131](https://github.com/joeyespo/grip/issues/131))
- CLI: Add "Omit this to render as a normal GitHub README file." to help avoid confusion of `--gfm`
- Readme: Add note about `^D` and `^Z` on Windows ([#105](https://github.com/joeyespo/grip/issues/105))
- Cleanup: PEP8


#### Version 3.2.0 (2015-02-24)

- Bugfix: Encode to UTF-8 before sending text off to GitHub to support non-`latin-1` characters ([#99](https://github.com/joeyespo/grip/issues/99))


#### Version 3.1.0 (2015-02-08)

- Bugfix: Support non-ascii languages ([#86](https://github.com/joeyespo/grip/issues/86))
- Bugfix: Fix links to header anchors ([#94](https://github.com/joeyespo/grip/issues/94))
- Bugfix: Unpin dependencies so there's no conflict with other globally-installed packages
- Bugfix: Fix missing octicons ([#95](https://github.com/joeyespo/grip/pull/95) - thanks, [@madflow][]!)
- Bugfix: Fix "Could not retrieve styles" error on Windows ([#90](https://github.com/joeyespo/grip/pull/90) - thanks, [@alexandre-mbm][]!)
- Cleanup


### Version 3.0.0 (2014-08-08)

- Enhancement: Add `{version}` format argument to `CACHE_DIRECTORY` so upgrades can start fresh and also drive cache clearing
- Enhancement: Allow exporting to stdout ([#73](https://github.com/joeyespo/grip/issues/73))
- Enhancement: Allow reading from stdin ([#72](https://github.com/joeyespo/grip/issues/72))
- Enhancement: Allow `:<port>` pattern in CLI
- Enhancement: Add a favicon ![favicon](artwork/favicon.ico) ([#60](https://github.com/joeyespo/grip/issues/60))
- Enhancement: Add "GitHub rate limit" page to replace the a generic 403 error ([#48](https://github.com/joeyespo/grip/issues/48))
- Enhancement: Add option to clear the cache ([#68](https://github.com/joeyespo/grip/issues/68))
- Enhancement: Allow storing credentials in config file ([#61](https://github.com/joeyespo/grip/issues/61))
- Enhancement: Read user settings from `~/.grip`
- Enhancement: Add `__main__.py` for allowing grip to be run as a module with `python -m grip`
- Enhancement: Add `--wide` option to render as the old GitHub size (to opt out of [#47](https://github.com/joeyespo/grip/issues/47))
- Enhancement: Add title to rendered page to look more like GitHub
- Bugfix: Allow using [personal auth tokens](https://github.com/settings/tokens/new?scopes=) without a username
- Bugfix: Show images from their canonical source instead of using GitHub's cache ([#50](https://github.com/joeyespo/grip/issues/50))
- Bugfix: Inline assets into the exported file ([#69](https://github.com/joeyespo/grip/issues/69))
- Bugfix: Cache the assets of the styles, ([#56](https://github.com/joeyespo/grip/issues/56))
- Bugfix: Allow cross-platform newlines in config ([#67](https://github.com/joeyespo/grip/pull/67))
- Bugfix: Fix running from another directory ([#36](https://github.com/joeyespo/grip/issues/36))
- Bugfix: Move `instance_path` to `~/.grip` to cache to a non-privileged directory ([#39](https://github.com/joeyespo/grip/pull/39) - thanks, [@swsnider][]!)
- Bugfix: Change the default width to match GitHub's new README style ([#47](https://github.com/joeyespo/grip/issues/47))
- Readme: Mention personal access tokens and link to the appropriate GitHub page ([#74](https://github.com/joeyespo/grip/pull/74) - thanks, [@davejamesmiller][]!)
- Readme: Add badges, more usage example, and support and contact information
- Readme: Specify that HTTPS is always used to access the GitHub API
- Readme: Document credentials and rate limit ([#46](https://github.com/joeyespo/grip/issues/46))
- Readme: Document configuration options
- Readme: Clarify command line arguments and `--gfm`
- Readme: Add Known Issues section
- Infrastructure and code cleanup


#### Version 2.0.1 (2014-06-14)

- Enhancement: Add ability to export to a specific file using the CLI ([#33](https://github.com/joeyespo/grip/issues/33))
- Enhancement: Python 3 compatibility ([#54](https://github.com/joeyespo/grip/pull/54) - thanks, [@fly][]!)
- Bugfix: Fix issue styles weren't being downloaded properly (thanks, [@fly][]!)
- Bugfix: Support anchoring to section headers like GitHub ([#58](https://github.com/joeyespo/grip/issues/58))
- Readme: Document rate limits and --user / --pass
- Readme: Refer to the "offline rendering" work
- Readme: Fix 'GitHub' spelling
- Extract and expose constants
- Update requirements


### Version 2.0.0 (2013-09-26)

- Feature: Styles are now cached (from the not-yet-released offline rendering) (thanks, [@isbadawi][]!)
- Feature: Add user/pass options for GitHub auth (thanks, [@joelittlejohn][]!)
- Feature: Add export to single HTML file (thanks, [@iliggio][]!)
- Enhancement: Better HTML titles by normalizing the path, always providing a title
- Enhancement: Allow styles to be overridden, with examples in static directory
- Enhancement: Relay GitHub API HTTP errors to browser for debuggability
- Enhancement: Extract render_app and add create_app in API
- Bugfix: Fix manual installs using setup.py (thanks, [@briancappello][]!)
- Bugfix: Fix rendering rendering local images (thanks, [@jgallagher][]!)
- Bugfix: Handle File Not Found errors as 404 when given a directory
- Rename and re-arrange the configuration files
- Update README.md with new features
- Update AUTHORS.md format
- Upgrade requirements
- Simplify code


#### Version 1.2.0 (2013-03-17)

- Add AUTHORS.md for attributing credit
- Feature: Can now click hyperlinks to render other files without re-running (thanks, [@vladwing][]!)
- Update GitHub CSS regular expression


#### Version 1.1.1 (2013-01-05)

- Upgrade path-and-address
- Use exact versions in requirements


#### Version 1.1 (2013-01-04)

- Readme: Clarify and add examples
- Bugfix: Typo in requirements
- Clean up setup.py


### Version 1.0 (2012-12-08)

- CLI: now accepts an address, not just a port
- CLI: now accepts --gfm and --context=<repo> arguments for rendering GitHub Flavored Markdown
- API: `serve` function now accepts `None` for its arguments to indicate 'use default'
- API: `serve` function now accepts a 'host'
- API: `serve` now resolves the default file when given a path
- Now using docopt for more advanced argument processing
- Now using path-and-address for humanistic path / address handling


#### Version 0.2.1 (2012-12-02)

- Issue #5: Fixed the installer to work in the case where the requirements are not already installed


#### Version 0.2 (2012-12-01)

- GitHub styles are now retrieved dynamically when run, instead of using the outdated styles from the config


#### Version 0.1.1 (2012-11-20)

- Added the port command-line argument


#### Version 0.1 (2012-11-19)

- First public preview release


[@vladwing]: https://github.com/vladwing
[@isbadawi]: https://github.com/isbadawi
[@joelittlejohn]: https://github.com/joelittlejohn
[@briancappello]: https://github.com/briancappello
[@jgallagher]: https://github.com/jgallagher
[@iliggio]: https://github.com/iliggio
[@fly]: https://github.com/fly
[@swsnider]: https://github.com/swsnider
[@davejamesmiller]: https://github.com/davejamesmiller
[@alexandre-mbm]: https://github.com/alexandre-mbm
[@madflow]: https://github.com/madflow
[@zmwangx]: https://github.com/zmwangx
[@dandavison]: https://github.com/dandavison
[@ssundarraj]: https://github.com/ssundarraj
[@jlhonora]: https://github.com/jlhonora
[@akawhy]: https://github.com/akawhy
