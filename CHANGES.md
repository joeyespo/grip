Grip Changelog
--------------


#### Version 4.6.2 (2023-10-12)

##### Bugs fixed

- Support Werkzeug 3 by using a default encoding of UTF-8 ([#377](https://github.com/joeyespo/grip/ issues/377) - thanks, [@daniel-eichinger-bl][]!)


#### Version 4.6.1 (2022-03-30)

##### Bugs fixed

- Fix "ImportError: cannot import name 'safe_join' from 'flask'" when using Flask 2.1.0+ ([#360](https://github.com/joeyespo/grip/pull/360) - thanks, [@bryce-carson][]!)


#### Version 4.6.0 (2022-02-01)

##### Notable changes

- Update output and **fix style issues**
- Add support for **Python 3.7, 3.8, 3.9, 3.10**
- Improve handling of PDFs and other binary files
- Fix deprecation warnings from newer dependency versions

##### Deprecations

- End-of-life [Python versions](https://devguide.python.org/#status-of-python-branches) no longer intentionally supported
  - Python 2.6, 2.7 (Python 2 compatibility will be removed entirely in the next major release)
  - Python 3.0, 3.1, 3.2, 3.3 ([#275](https://github.com/joeyespo/grip/pull/275) - thanks, [@svisser][]!), 3.4, 3.5, 3.6
- Current [dependency versions](requirements.txt) (more recent versions will be required in the next major release)

##### Bugs fixed

- Fix typo in error message ([#266](https://github.com/joeyespo/grip/pull/266) - thanks, [@Godron629][]!)
- Update HTML/CSS scaffold to match GitHub ([#297](https://github.com/joeyespo/grip/pull/297) - thanks, [@phyllisstein][]!)
- Fix tests by adding a missing `USER_CONTEXT` argument to one of the `GitHubRenderer` calls
- Serve non-`text/` MIME types as raw files for better handling of, e.g. PDF files ([#234](https://github.com/joeyespo/grip/pull/234) - thanks, [@wvspee][]!)
- Fix style parsing, which caused some styles to be missing ([#347](https://github.com/joeyespo/grip/issues/347))

##### Other changes

- Readme: Update to correct `--no-inline` option ([#267](https://github.com/joeyespo/grip/issues/267) - thanks, [@TomDLT][]!)
- Readme: Fix links to Grip class ([#276](https://github.com/joeyespo/grip/issues/276) - thanks, [@jacebrowning][]!)
- Readme: Clarify that this sends your markdown to GitHub ([#251](https://github.com/joeyespo/grip/issues/251) - thanks, [@courajs][]!)
- Update `pytest` usages (see [pytest 3.0.0 changelog](https://github.com/pytest-dev/pytest/blob/master/CHANGELOG.rst#300-2016-08-18))
- Add `.pytest_cache` to `.gitignore` ([#287](https://github.com/joeyespo/grip/pull/287) - thanks, [@svisser][]!)
- Add `.venv` and `.idea` to `.gitignore` and clean up
- Add `flake8` test dependency and fix linting errors ([#299](https://github.com/joeyespo/grip/pull/299))
- Add `pytest` test dependency ([#294](https://github.com/joeyespo/grip/pull/294) - thanks, [@Methacrylon][]!)
- License: Distribute LICENSE file ([#274](https://github.com/joeyespo/grip/pull/274) - thanks, [@synapticarbors][]!)
- License: Update year


###### Version 4.5.2 (2018-03-18)

- Enhancement: Show more helpful error message on TLSV1_ALERT_PROTOCOL_VERSION to help people through ([#262](https://github.com/joeyespo/grip/pull/262))
- Docs: Use smaller header for patch version titles in CHANGES.md


###### Version 4.5.1 (2018-03-18)

- Bugfix: Don't print "Downloading" from `--export` when using `--quiet`
- Cleanup: Move `quiet` kwarg of `export()` to the end like the other API methods
- Readme: Document `quiet` kwarg of `export()`
- Readme: Document `quiet` kwarg of `render_page()`


#### Version 4.5.0 (2018-03-18)

- Enhancement: Show warning if no styles are collected ([#265](https://github.com/joeyespo/grip/pull/265))
- Bugfix: Don't print "Exporting" from `--export` when using `--quiet` ([#247](https://github.com/joeyespo/grip/pull/247) - thanks, [@kagof][]!)
- Bugfix: Fix style parsing ([#265](https://github.com/joeyespo/grip/pull/265))
- Bugfix: Loosen up the style URLs matching ([#265](https://github.com/joeyespo/grip/pull/265))
- Internals: Fix `_strip_url_params` method name typo ([#254](https://github.com/joeyespo/grip/pull/254) - thanks, [@jwilk][]!)
- Readme: Fix syntax highlighting in README ([#264](https://github.com/joeyespo/grip/pull/264) - thanks, [@jwilk][]!)
- Readme: Remove Gratipay :frowning_face: ([Article](https://gratipay.news/the-end-cbfba8f50981))
- Readme: Tweak Contributing copy
- Tests: Wrap map() with list() for multiple iteration for Python 3 support
- Tests: Call `Popen.communicate()` only once
- Tests: Regenerate render output
- Cleanup: PEP8
- Thanks: [@jwilk][] for getting the GitHub repo to finally show the right Language stats :smiley: ([#263](https://github.com/joeyespo/grip/pull/263))


#### Version 4.4.0 (2017-09-24)

- Patch: Work around a GitHub API header bug ([#245](https://github.com/joeyespo/grip/pull/245))
- Bugfix: Fail cleanly when server address is already in use ([#216](https://github.com/joeyespo/grip/pull/216) - thanks, [@davisjam][]!)
- Bugfix: Fix `--browser` when running on a random port (port 0) ([#219](https://github.com/joeyespo/grip/pull/219))
- Bugfix: Add defaults to USERNAME and PASSWORD in case just one is provided ([#222](https://github.com/joeyespo/grip/pull/222))
- Internals: Fix deprecation warning in Python 3.6 by using triple-quoted raw strings in regexp constants ([#223](https://github.com/joeyespo/grip/pull/223) - thanks, [@jwilk][]!)
- Internals: Decouple patchers from renderers
- Docs: Fix typo in API docs ([#224](https://github.com/joeyespo/grip/pull/224) - thanks, [@jwilk][]!)
- Readme: Add Homebrew installation instructions ([#201](https://github.com/joeyespo/grip/issues/201) - thanks, [@zmwangx][]!)
- Readme: Use `pwd` instead of `PWD` in bash shell example ([#207](https://github.com/joeyespo/grip/pull/207) - thanks, [@xxd3vin][]!)
- Readme: Use 'index.html' in --export example for searchability
- Readme: Fix link to `offline-renderer` branch ([#230](https://github.com/joeyespo/grip/pull/230) - thanks, [@4ndrej][]!)
- Readme: Add Configuration troubleshooting tip and example
- Readme: Add [Say Thanks](http://saythanks.io/) badge :smiley:
- Thanks: [@JasonThomasData][] for investigating and working with GitHub Support to fix a heading bug ([#235](https://github.com/joeyespo/grip/pull/235))


#### Version 4.3.2 (2016-07-21)

- Bugfix: Fix `setup.py install` ([#199](https://github.com/joeyespo/grip/issues/199))


###### Version 4.3.1 (2016-07-21)

- Bugfix: Allow port 0 ([#197](https://github.com/joeyespo/grip/pull/197))
- Bugfix: Fix setup.py build and include octicon files in the build asset ([#198](https://github.com/joeyespo/grip/issues/198))


#### Version 4.3.0 (2016-07-19)

- Bugfix: Fix `--export` deadlock ([#184](https://github.com/joeyespo/grip/issues/184))
- Bugfix: Make `--quiet` truly quiet ([#188](https://github.com/joeyespo/grip/pull/188) - thanks, [@kba][]!)
- Bugfix: Allow `--clear` to work without a README file present ([#189](https://github.com/joeyespo/grip/issues/189))
- Bugfix: Fix tests by patching sys.exc_clear to have Flask 0.11 work on pypy3 ([#190](https://github.com/joeyespo/grip/issues/190))
- Bugfix: Fix minor version check during patch_svg ([#191](https://github.com/joeyespo/grip/issues/191))
- Bugfix: Add Octicon font until the Readme API inlines SVGs ([#192](https://github.com/joeyespo/grip/issues/192))
- Bugfix: Show '- Grip' in `<title>` only, not in page header ([#193](https://github.com/joeyespo/grip/issues/193))
- Readme: Remove duplicated words ([#177](https://github.com/joeyespo/grip/pull/177) - thanks, [@jwilk][]!)
- Readme: Remove download count badge since it's broken ([#194](https://github.com/joeyespo/grip/pull/194))


#### Version 4.2.0 (2016-04-12)

- Enhancement: Expose `render_inline` through `--no-inline` CLI option ([#165](https://github.com/joeyespo/grip/pull/165) - thanks, [@mrexmelle][]!)
- Bugfix: Update Readme width to match latest GitHub changes ([#167](https://github.com/joeyespo/grip/pull/167) - thanks, [@motevets][]!)
- Bugfix: Update Octicons to match latest GitHub changes ([#167](https://github.com/joeyespo/grip/pull/167) - thanks, [@motevets][]!)
- Bugfix: Enable SVG support for Python 2.6 and below ([#157](https://github.com/joeyespo/grip/issues/157))
- Readme: Fix Mac OS name ([#162](https://github.com/joeyespo/grip/pull/162) - thanks, [@ErikMHummel][]!)
- Readme: Add tip for generating docs from Readme files ([#168](https://github.com/joeyespo/grip/pull/168) - thanks, [@mrexmelle][]!)
- License: Update year


#### Version 4.1.0 (2015-12-11)

- Enhancement: Prompt for password when `--user` is provided without a `--pass` ([#154](https://github.com/joeyespo/grip/pull/154) - thanks, [@mekoda][]!)
- Bugfix: Default to UTF-8 when reading from stdin and there's no encoding ([#152](https://github.com/joeyespo/grip/issues/152))
- Readme: Document `-b`
- Readme: Add [link to Grip Release Letter](http://joeyespo.us2.list-manage.com/subscribe?u=255dd49194fa8078258d9a735&id=d76534e979&group[14285][1]=true) for getting notified about future releases
- Readme: Remove Known Issues section since they are now working


### Version 4.0.0 (2015-11-18)

##### Notable changes

- Content is now refreshed when the file changes ([#135](https://github.com/joeyespo/grip/pull/135) - thanks, [@markbt][]!)
- Rename `--gfm` to `--user-content` to reduce confusion ([#139](https://github.com/joeyespo/grip/pull/139))
- Fix general Readme [Task Lists](https://github.com/blog/1825-task-lists-in-all-markdown-documents) ([#149](https://github.com/joeyespo/grip/issues/149))
- Rearchitect the internals
- Add tests

##### Breaking changes (API)

- Reorder API function arguments for consistency
- Remove `STATIC_URL_PATH` from settings (use `Grip` constructor or the ENV variable instead)
- Remove `STYLE_URLS_SOURCE` and `STYLE_ASSET_` settings (they're now constants)
- Remove `CACHE_URL` setting (the cache URL is now `{}/cache.format(GRIPURL)`)
- Remove `github_renderer.render_content` (use `GitHubRenderer` instead)
- Remove `offline_renderer.render_content` (use `OfflineRenderer` instead)
- Remove `read_binary` and `read_text` functions (use `io.open` directly)
- Remove `resolve_readme` (use `DirectoryReader(path, force).filename_for(None)` instead)
- Remove `text.read` call in `TextReader.read(text)`
- Route Grip assets through `/__/grip` by default instead of `/`
- Raise `ReadmeNotFoundError` when a Readme is not found instead of `ValueError`
- Require a Unicode string when rendering Markdown
- Set `DEBUG` to `False` by default in settings
- Use UPPERCASE for constants

##### Assumptions fixed

- Update URL of GitHub assets

##### Bugs fixed

- Stop `--browser` from consuming all the sockets ([#136](https://github.com/joeyespo/grip/pull/136) - thanks, [@markbt][]!)
- Fix `--browser` to stop waiting when the server is terminated before it listens
- Fix `--browser` when listening on `0.0.0.0`
- Fix Python 2.6
- Fix Python 3.x with `python -m grip`
- Allow caching of assets that include query parameters
- Take the `route` argument into account in `Grip.render` (this was broken in the old `render_app`)
- Fix rendering Readme containing Unicode by manually decoding UTF-8 from the GitHub response

##### Other changes

- Add `Home.md` as a supported default file title for GitHub Wikis
- Add `AlreadyRunningError` for calling `Grip.run` while the server is already running
- Add `ReadmeNotFoundError` for cross-Python-version file-not-found errors
- Add `Grip`, a subclass of `Flask`
- Add `ReadmeAssetManager` and `GitHubAssetManager`
- Add `ReadmeReader`, `DirectoryReader`, `StdinReader`, and `TextReader`
- Add `ReadmeRenderer`, `GitHubRenderer`, and `OfflineRenderer`
- Add `grip.command.version` for printing version information (similar to `grip.command.usage`)
- Print version with `-V`
- Make `port` and `cancel_event` optional arguments in `wait_and_start_browser`
- Add `start_browser_when_ready` to wait and start the browser in a background thread
- Add the `--quiet` CLI option
- The `GRIPHOME` ENV variable now expands the user directory (`~`), e.g. `~/.config/grip`
- Add `DEFAULT_API_URL` constant as a fallback for when `api_url` is not specified in `render_content` or `GitHubRenderer`
- Add `grip_url` and its fallback constant `DEFAULT_GRIPURL` for specifying a route to serve Grip assets from
- Remove implicit dependencies in `requirements.txt`
- Readme: Add [Tips section](https://github.com/joeyespo/grip#tips)


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
- Bugfix: Add trailing slashes to directories and remove them for files so relative links are correct ([#131](https://github.com/joeyespo/grip/issues/131))
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
- Enhancement: Add "GitHub rate limit" page to replace the generic 403 error ([#48](https://github.com/joeyespo/grip/issues/48))
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


###### Version 2.0.1 (2014-06-14)

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
- Bugfix: Fix rendering local images (thanks, [@jgallagher][]!)
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


###### Version 1.1.1 (2013-01-05)

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
[@markbt]: https://github.com/markbt
[@mekoda]: https://github.com/mekoda
[@ErikMHummel]: https://github.com/ErikMHummel
[@mrexmelle]: https://github.com/mrexmelle
[@motevets]: https://github.com/motevets
[@kba]: https://github.com/kba
[@jwilk]: https://github.com/jwilk
[@xxd3vin]: https://github.com/xxd3vin
[@davisjam]: https://github.com/davisjam
[@JasonThomasData]: https://github.com/JasonThomasData
[@4ndrej]: https://github.com/4ndrej
[@erikrtn]: https://github.com/erikrtn
[@kagof]: https://github.com/kagof
[@Godron629]: https://github.com/Godron629
[@TomDLT]: https://github.com/TomDLT
[@synapticarbors]: https://github.com/synapticarbors
[@svisser]: https://github.com/svisser
[@jacebrowning]: https://github.com/jacebrowning
[@phyllisstein]: https://github.com/phyllisstein
[@courajs]: https://github.com/courajs
[@wvspee]: https://github.com/wvspee
[@Methacrylon]: https://github.com/Methacrylon
[@bryce-carson]: https://github.com/bryce-carson
[@daniel-eichinger-bl]: https://github.com/daniel-eichinger-bl
