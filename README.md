Grip -- GitHub Readme Instant Preview
=====================================

Render local readme files before sending off to GitHub.

Grip is a command-line server application written in Python that uses the
[GitHub markdown API][markdown] to render a local readme file. The styles also
come directly from GitHub, so you'll know exactly how it will appear.


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
 * Running on http://localhost:5000/
```

Now open a browser and visit [http://localhost:5000](http://localhost:5000/).

You can also specify a port:

```bash
$ grip 80
 * Running on http://localhost:80/
```

Or an explicit file:

```bash
$ grip AUTHORS.md
 * Running on http://localhost:5000/
```

Alternatively, you could just run `grip` and visit [localhost:5000/AUTHORS.md][AUTHORS.md]
since grip supports relative URLs.

You can combine the previous examples. You can also specify a hostname instead of a port. Or provide both:

```bash
$ grip AUTHORS.md 0.0.0.0:80
 * Running on http://0.0.0.0:80/
```

You can even bypass the server and export to a single HTML:

```bash
$ grip --export AUTHORS.md authors.html
```

Comment / issue-style GFM is also supported, with an optional repository context for linking to issues:

```bash
$ grip --gfm --context=joeyespo/grip
 * Running on http://localhost:5000/
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

Or store this information [in a configuration variable](#configuration).

There's also a [work-in-progress branch][fix-render-offline] to provide
**offline rendering**. Once this resembles GitHub more precisely, it'll
be exposed in the CLI, and will ultimately be used as a seamless fallback
engine for when the API can't be accessed.


Known issues
------------

- [ ] GitHub introduced read-only task lists to all Markdown documents in
      repositories and wikis [back in April][task-lists], but
      [the API][markdown] doesn't seem to respect this yet.


Configuration
-------------

You can add the following variables to a settings file:

- `HOST`: The host to use when not provided as a CLI argument, `localhost` by default
- `PORT`: The port to use when not provided as a CLI argument, `5000` by default
- `DEBUG`: Whether to use Flask's debugger when an error happens, `True` by default
- `DEBUG_GRIP`: Prints extended information when an error happens, `False` by default
- `USERNAME`: The username to use when not provided as a CLI argument, `None` by default
- `PASSWORD`: The password to use when not provided as a CLI argument, `None` by default
- `CACHE_DIRECTORY`: The directory to place the cached styles and assets (relative to `~/.grip`), `cache` by default
- `CACHE_URL`: The URL to serve cached styles and assets from
- `STYLE_URLS`: Additional URLs that will be added to the rendered page, `[]` by default <br />
                See [grip/static/README.md][static-readme] for details.
- `STYLE_URLS_SOURCE`: The URL to use to locate and download the styles from, `https://github.com/joeyespo/grip` by default
- `STYLE_URLS_RE`: The regular expression to use to parse the styles from the source
- `STYLE_ASSET_URLS_RE`: The regular expression to use to parse the assets from the styles
- `STYLE_ASSET_URLS_SUB`: Replaces the above regular expression with a local URL, as saved in the cache

Put these variables in either:

1. `~/.grip/settings.py` (create this file if it doesn't already exist)
2. `grip/settings_local.py` from your current Python installation's `site-packages`


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
serve(path=None, host=None, port=None, gfm=False, context=None, username=None, password=None, render_offline=False, render_wide=False)
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


#### export

Writes the specified Readme file to an HTML file with styles inlined.

```python
export(path=None, gfm=False, context=None, username=None, password=None, render_offline=False, render_wide=False, out_filename=None)
```

- `path`: The filename to render, or the directory containing your Readme file, defaulting to the current working directory
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `username`: The user to authenticate with GitHub to extend the API limit
- `password`: The password to authenticate with GitHub to extend the API limit
- `render_offline`: Whether to render locally using [Python-Markdown][] (Note: this is a work in progress)
- `render_wide`: Whether to render a wide page, `False` by default (this has no effect when used with `gfm`)
- `out_filename`: The filename to write to, `<in_filename>.html` by default


#### create_app

Creates a Flask application you can use to render and serve the Readme files.
This is the same app used by `serve` and `export` and initializes the cache,
using the cached styles when available.

```python
create_app(path=None, gfm=False, context=None, username=None, password=None, render_offline=False, render_wide=False, render_inline=False)
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


#### render_app

```python
render_app(app, route='/')
```

- `app`: The Flask application to render
- `route`: The route to render, '/' by default


#### render_content

Renders the specified markdown text without caching.

```python
render_content(text, gfm=False, context=None, username=None, password=None, render_offline=False)
```

- `text`: The content to render
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `username`: The user to authenticate with GitHub to extend the API limit
- `password`: The password to authenticate with GitHub to extend the API limit
- `render_offline`: Whether to render locally using [Python-Markdown][] (Note: this is a work in progress)


#### render_page

Renders the specified markdown text without caching and outputs an HTML
page that resembles the GitHub Readme view.

```python
render_page(text, filename=None, gfm=False, context=None, username=None, password=None, render_offline=False, style_urls=[], styles=[], render_title=None, render_wide=False)
```

- `text`: The content to render
- `filename`: The text to render at the top of the page and to use in the page's title, if provided
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `username`: The user to authenticate with GitHub to extend the API limit
- `password`: The password to authenticate with GitHub to extend the API limit
- `render_offline`: Whether to render offline using [Python-Markdown][] (Note: this is a work in progress)
- `style_urls`: A list of URLs that contain CSS to include in the rendered page
- `styles`: A list of style content strings to inline in the rendered page
- `render_title`: Whether to render the title section on the page, `not gfm` by default
- `render_wide`: Whether to render a wide page, `False` by default (this has no effect when used with `gfm`)


#### resolve_readme

Returns the path if it's a file; otherwise, looks for a compatible README file
in the directory specified by path. If path is None, the current working
directory is used. If no compatible README can be found, ValueError is raised.

```python
resolve_readme(path=None)
```

- `path`: The filename to render, or the directory containing your Readme file, defaulting to the current working directory


#### clear_cache

Clears the cached styles and assets and exits.

```python
clear_cache()
```


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


[markdown]: http://developer.github.com/v3/markdown
[fix-render-offline]: http://github.com/joeyespo/grip/tree/fix-render-offline
[static-readme]: grip/static/README.md
[task-lists]: https://github.com/blog/1825-task-lists-in-all-markdown-documents
[rdd]: http://tom.preston-werner.com/2010/08/23/readme-driven-development.html
[gfm]: http://github.github.com/github-flavored-markdown
[python-markdown]: https://github.com/waylan/Python-Markdown
[authors.md]: AUTHORS.md
