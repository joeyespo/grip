Grip -- GitHub Readme Instant Preview
=====================================

[![Downloads/month on PyPI](http://img.shields.io/pypi/dm/grip.svg)][pypi]
[![Current version on PyPI](http://img.shields.io/pypi/v/grip.svg)][pypi]

Render local readme files before sending off to GitHub.

Grip is a command-line server application written in Python that uses the
[GitHub markdown API][markdown] to render a local readme file. The styles also
come directly from GitHub, so you'll know exactly how it will appear. Changes
you make to the Readme file will be instantly reflected in the browser.


Motivation
----------

Sometimes you just want to see the exact readme
result before committing and pushing to GitHub.

Especially when doing [Readme-driven development][rdd].


Installation
------------

To install grip, simply:

```bash
$ pip install grip
```


Usage
-----

To render the readme of a repository:

```bash
$ cd myrepo
$ grip
 * Running on http://localhost:6419/
```

Now open a browser and visit [http://localhost:6419](http://localhost:6419/).

You can also specify a port:

```bash
$ grip 80
 * Running on http://localhost:80/
```

Or an explicit file:

```bash
$ grip AUTHORS.md
 * Running on http://localhost:6419/
```

Alternatively, you could just run `grip` and visit [localhost:6419/AUTHORS.md][AUTHORS.md]
since grip supports relative URLs.

You can combine the previous examples. Or specify a hostname instead of a port. Or provide both.

```bash
$ grip AUTHORS.md 80
 * Running on http://localhost:80/
```

```bash
$ grip CHANGES.md 0.0.0.0
 * Running on http://0.0.0.0:6419/
```

```bash
$ grip . 0.0.0.0:80
 * Running on http://0.0.0.0:80/
```

You can even bypass the server and **export** to a single HTML file, with all the styles and assets inlined:

```bash
$ grip --export
Exporting to README.html
```

Control the output name with the second argument:

```bash
$ grip README.md --export readme.html
Exporting to readme.html
```

Reading and writing from **stdin** and **stdout** is also supported, allowing you to use Grip with other programs:

```bash
$ cat README.md | grip -
 * Running on http://localhost:6419/
```

```bash
$ grip AUTHORS.md --export - | bcat
```

```bash
$ cat README.md | grip --export - | less
```

This allows you to quickly test how things look by entering Markdown directly in your terminal:

```bash
$ grip -
Hello **world**!
^D
 * Running on http://localhost:6419/
```

*Note: `^D` means `Ctrl+D`, which works on Linux and iOS. On Windows you'll have to use `Ctrl+Z`.*

**Comment / issue-style GFM** is also supported, with an optional repository context for linking to issues:

```bash
$ grip --gfm --context=joeyespo/grip
 * Running on http://localhost:6419/
```

For more details and additional options, see the help:

```bash
$ grip -h
```


Access
------

Grip strives to be as close to GitHub as possible. To accomplish this, grip
uses [GitHub's Markdown API][markdown] so that changes to their rendering
engine are reflected immediately without requiring you to upgrade grip.
However, because of this you may hit the API's hourly rate limit. If this
happens, grip offers a way to access the API using your credentials
to unlock a much higher rate limit.

```bash
$ grip --user <your-username> --pass <your-password>
```

Or use a [personal access token][] with an empty scope (note that a token is
*required* if your GitHub account is set up with two-factor authentication):

```bash
$ grip --pass <token>
```

You can persist these options [in your local configuration](#configuration).
For security purposes, it's highly recommended that you **use an access token
over a password**. (You could also keep your password safe by configuring
Grip to [grab your password from a password manager][keychain-access].)

There's also a [work-in-progress branch][fix-render-offline] to provide
**offline rendering**. Once this resembles GitHub more precisely, it'll
be exposed in the CLI, and will ultimately be used as a seamless fallback
engine for when the API can't be accessed.

Grip always accesses GitHub over HTTPS,
so your README and credentials are protected.


Tips
----

Here's how others from the community are using Grip.

#### Create a local mirror of a Github Wiki

```bash
$ git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.wiki.git
$ cd YOUR_REPOSITORY.wiki
$ grip
```

*By [Joshua Gourneau](https://twitter.com/gourneau/status/636329126643658753)*.

*Want to share your own? [Say hello][twitter] or [see below](#contributing).*


Known issues
------------

- [ ] GitHub introduced read-only task lists to all Markdown documents in
      repositories and wikis [back in April][task-lists], but
      [the API][markdown] doesn't respect this yet.


Configuration
-------------

To customize Grip, create `~/.grip/settings.py`, then add one or more of the following variables:

- `HOST`: The host to use when not provided as a CLI argument, `localhost` by default
- `PORT`: The port to use when not provided as a CLI argument, `6419` by default
- `DEBUG`: Whether to use Flask's debugger when an error happens, `True` by default
- `DEBUG_GRIP`: Prints extended information when an error happens, `False` by default
- `USERNAME`: The username to use when not provided as a CLI argument, `None` by default
- `PASSWORD`: The password or [personal access token][] to use when not provided as a CLI argument (*Please don't save your passwords here.* Instead, use an access token or drop in this code [grab your password from a password manager][keychain-access]), `None` by default
- `API_URL`: Base URL for the github API, for example that of a Github Enterprise instance. The default is the public API https://api.github.com.
- `CACHE_DIRECTORY`: The directory, relative to `~/.grip`, to place cached assets (this gets run through the following filter: `CACHE_DIRECTORY.format(version=__version__)`), `'cache-{version}'` by default
- `CACHE_URL`: The URL to serve cached styles and assets from, in case there's a URL conflict, `'/grip-cache'` by default
- `STATIC_URL_PATH`: The URL to serve static assets from, in case there's a URL conflict, `'/grip-static'` by default
- `STYLE_URLS`: Additional URLs that will be added to the rendered page, `[]` by default
- `STYLE_URLS_SOURCE`: The URL to use to locate and download the styles from, `https://github.com/joeyespo/grip` by default
- `STYLE_URLS_RE`: The regular expression to use to parse the styles from the source
- `STYLE_ASSET_URLS_RE`: The regular expression to use to parse the assets from the styles
- `STYLE_ASSET_URLS_SUB`: Replaces the above regular expression with a local URL, as saved in the cache
- `STYLE_ASSET_URLS_INLINE`: The regular expression to use when inlining assets into the downloaded style
   Note that this must include both the original and post-`STYLE_ASSET_URLS_SUB` patterns.

#### Advanced

This file is a normal Python script, so you can add more advanced configuration.

For example, to read a setting from the environment and provide a default value
when it's not set:

```python
PORT = os.environ.get('GRIP_PORT', 8080)
```


API
---

You can access the API directly with Python, using it in your own projects:

```python
from grip import serve

serve(port=8080)
 * Running on http://localhost:8080/
```

Or access the underlying Flask application for even more flexibility:

```python
from grip import create_app

grip_app = create_app(gfm=True)
# Use in your own app
```


### Documentation

#### serve

Runs a local server and renders the Readme file located
at `path` when visited in the browser.

```python
serve(path=None, host=None, port=None, gfm=False, context=None, username=None, password=None, render_offline=False, render_wide=False, render_inline=False, api_url=None, title=None, autoupdate=True, grip_class=None)
```

- `path`: The filename to render, or the directory containing your Readme file, defaulting to the current working directory
- `host`: The host to listen on, defaulting to the HOST configuration variable
- `port`: The port to listen on, defaulting to the PORT configuration variable
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `username`: The user to authenticate with GitHub to extend the API limit
- `password`: The password to authenticate with GitHub to extend the API limit
- `render_offline`: Whether to render locally using [Python-Markdown][] (Note: this is a work in progress)
- `render_wide`: Whether to render a wide page, `False` by default (this has no effect when used with `gfm`)
- `render_inline`: Whether to inline the styles within the HTML file
- `api_url`: A different base URL for the github API, for example that of a Github Enterprise instance. The default is the public API https://api.github.com.
- `title`: The page title, derived from `path` by default
- `autoupdate`: Automatically update the rendered content when the Readme file changes, `True` by default
- `grip_class`: Use a custom [Grip class](#grip-class)


#### export

Writes the specified Readme file to an HTML file with styles and assets inlined.

```python
export(path=None, gfm=False, context=None, username=None, password=None, render_offline=False, render_wide=False, render_inline=True, out_filename=None, api_url=None, title=None)
```

- `path`: The filename to render, or the directory containing your Readme file, defaulting to the current working directory
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `username`: The user to authenticate with GitHub to extend the API limit
- `password`: The password to authenticate with GitHub to extend the API limit
- `render_offline`: Whether to render locally using [Python-Markdown][] (Note: this is a work in progress)
- `render_wide`: Whether to render a wide page, `False` by default (this has no effect when used with `gfm`)
- `render_inline`: Whether to inline the styles within the HTML file (Note: unlike the other API functions, this defaults to `True`)
- `out_filename`: The filename to write to, `<in_filename>.html` by default
- `api_url`: A different base URL for the github API, for example that of a Github Enterprise instance. The default is the public API https://api.github.com.
- `title`: The page title, derived from `path` by default


#### create_app

Creates a Flask application you can use to render and serve the Readme files.
This is the same app used by `serve` and `export` and initializes the cache,
using the cached styles when available.

```python
create_app(path=None, gfm=False, context=None, username=None, password=None, render_offline=False, render_wide=False, render_inline=False, api_url=None, title=None, text=None, autoupdate=True, grip_class=None)
```

- `path`: The filename to render, or the directory containing your Readme file, defaulting to the current working directory
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `username`: The user to authenticate with GitHub to extend the API limit
- `password`: The password to authenticate with GitHub to extend the API limit
- `render_offline`: Whether to render locally using [Python-Markdown][] (Note: this is a work in progress)
- `render_wide`: Whether to render a wide page, `False` by default (this has no effect when used with `gfm`)
- `render_inline`: Whether to inline the styles within the HTML file
- `api_url`: A different base URL for the github API, for example that of a Github Enterprise instance. The default is the public API https://api.github.com.
- `title`: The page title, derived from `path` by default
- `text`: A string or stream of Markdown text to render instead of being loaded from `path` (Note: `path` can be used to set the page title)
- `autoupdate`: Automatically update the rendered content when the Readme file changes, `True` by default
- `grip_class`: Use a custom [Grip class](#grip-class)


#### render_app

Renders the application created by `create_app` and returns the HTML that would
normally appear when visiting that route.

```python
render_app(app, route='/')
```

- `app`: The Flask application to render
- `route`: The route to render, '/' by default


#### render_content

Renders the specified markdown text without caching.

```python
render_content(text, gfm=False, context=None, username=None, password=None, render_offline=False, api_url=None, title=None)
```

- `text`: The Markdown text to render
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `username`: The user to authenticate with GitHub to extend the API limit
- `password`: The password to authenticate with GitHub to extend the API limit
- `render_offline`: Whether to render locally using [Python-Markdown][] (Note: this is a work in progress)
- `api_url`: A different base URL for the github API, for example that of a Github Enterprise instance. This is required when not using the offline renderer.
- `title`: The page title, derived from `path` by default


#### render_page

Renders the markdown from the specified path or text, without caching,
and returns an HTML page that resembles the GitHub Readme view.

```python
render_page(path=None, gfm=False, context=None, username=None, password=None, render_offline=False, render_wide=False, render_inline=False, api_url=None, title=None, text=None)
```

- `path`: The path to use for the page title, rendering `'README.md'` if None
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `username`: The user to authenticate with GitHub to extend the API limit
- `password`: The password to authenticate with GitHub to extend the API limit
- `render_offline`: Whether to render offline using [Python-Markdown][] (Note: this is a work in progress)
- `render_wide`: Whether to render a wide page, `False` by default (this has no effect when used with `gfm`)
- `render_inline`: Whether to inline the styles within the HTML file
- `api_url`: A different base URL for the github API, for example that of a Github Enterprise instance. The default is the public API https://api.github.com.
- `title`: The page title, derived from `path` by default
- `text`: A string or stream of Markdown text to render instead of being loaded from `path` (Note: `path` can be used to set the page title)

#### resolve_readme

Returns the path if it's a file; otherwise, looks for a compatible README file
in the directory specified by path. If path is None, the current working
directory is used. If no compatible README can be found, ValueError is raised.

```python
resolve_readme(path=None, force=False)
```

- `path`: The filename to render, or the directory containing your Readme file, defaulting to the current working directory
- `force`: Whether to force a result, even when a readme file is not found


#### clear_cache

Clears the cached styles and assets.

```python
clear_cache()
```


### Grip class

A Flask application that provides the following overridable methods.


#### read_text

Reads the text content of the specified file. Returns a UTF-8 string.

```python
read_text(self, filename)
```

- `filename`: The UTF-8 file to read.


#### read_binary

Reads the text content of the specified file. Returns a byte string.

```python
read_binary(self, filename)
```

- `filename`: The UTF-8 file to read.


#### supported_extensions

The supported extensions, as defined by [GitHub][markdown].

```python
supported_extensions = ['.md', '.markdown']
```


#### default_filenames

This constant contains the names Grip looks for when no file is provided.

```python
default_filenames = map(lambda ext: 'README' + ext, supported_extensions)
```


Contributing
------------

1. Check the open issues or open a new issue to start a discussion around
   your feature idea or the bug you found
2. Fork the repository, make your changes, and add yourself to [Authors.md][]
3. Send a pull request

If your PR has been waiting a while, feel free to [ping me on Twitter][twitter].

Use this software often? Please consider supporting Grip on
<a href="https://gratipay.com/grip/" title="Thank you!" target="_blank">
  <img align="center" style="margin-bottom:1px" src="http://joeyespo.com/images/gratipay-button.png" alt="Gratipay">
</a>


[pypi]: http://pypi.python.org/pypi/grip/
[markdown]: http://developer.github.com/v3/markdown
[rdd]: http://tom.preston-werner.com/2010/08/23/readme-driven-development.html
[authors.md]: AUTHORS.md
[fix-render-offline]: http://github.com/joeyespo/grip/tree/fix-render-offline
[personal access token]: https://github.com/settings/tokens/new?scopes=
[keychain-access]: https://gist.github.com/klmr/3840aa3c12f947e4064c
[task-lists]: https://github.com/blog/1825-task-lists-in-all-markdown-documents
[gfm]: http://github.github.com/github-flavored-markdown
[python-markdown]: http://github.com/waylan/Python-Markdown
[twitter]: http://twitter.com/joeyespo
