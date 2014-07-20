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

You can even bypass the server and export to a single HTML:

```bash
$ grip --export AUTHORS.md authors.html
```

GitHub-Flavored Markdown is also supported, with an optional repository context for linking to issues:

```bash
$ grip --gfm --context=joeyespo/grip
 * Running on http://localhost:5000/
```

For more details, see the help:

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

There's also a [work-in-progress branch][fix-render-offline] to provide
**offline rendering**. Once this resembles GitHub more precisely, it'll
be exposed in the CLI, and will ultimately be used as a seamless fallback
engine for when the API can't be accessed.


Known issues
------------

- [ ] GitHub introduced read-only task lists to all Markdown documents in
      repositories and wikis [back in April][task-lists], but
      [the API][markdown] doesn't seem to respect this yet.


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
serve(path='file-or-directory', host='localhost', port=5000, gfm=False, context=None, username=None, password=None, render_offline=False)
```

- `path`: The filename to render, or the directory containing your Readme file
- `host`: The host to serve on
- `port`: The port to serve on
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `username`: The user to authenticate with GitHub to extend the API limit
- `password`: The password to authenticate with GitHub to extend the API limit
- `render_offline`: Whether to render locally using [Python-Markdown][] (Note: this is a work in progress)


#### export

Writes the specified Readme file to an HTML file with styles inlined.

```python
export(path='file-or-directory', gfm=False, context=None, username=None, password=None, render_offline=False, out_filename=None)
```

- `path`: The filename to render, or the directory containing your Readme file
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `username`: The user to authenticate with GitHub to extend the API limit
- `password`: The password to authenticate with GitHub to extend the API limit
- `render_offline`: Whether to render locally using [Python-Markdown][] (Note: this is a work in progress)
- `out_filename`: The filename to write to, `<in_filename>.html` by default


#### create_app

Creates a Flask application you can use to render and serve the Readme files.
This is the same app used by `serve` and `export` and initializes the cache,
using the cached styles when available.

```python
create_app(path='file-or-directory', gfm=False, context=None, username=None, password=None, render_offline=False, render_inline=False)
```

- `path`: The filename to render, or the directory containing your Readme file
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `username`: The user to authenticate with GitHub to extend the API limit
- `password`: The password to authenticate with GitHub to extend the API limit
- `render_offline`: Whether to render locally using [Python-Markdown][] (Note: this is a work in progress)
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
render_page(text, filename=None, gfm=False, context=None, username=None, password=None, render_offline=False, style_urls=[], styles=[])
```

- `text`: The content to render
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `username`: The user to authenticate with GitHub to extend the API limit
- `password`: The password to authenticate with GitHub to extend the API limit
- `render_offline`: Whether to render offline using [Python-Markdown][] (Note: this is a work in progress)
- `style_urls`: A list of URLs that contain CSS to include in the rendered page
- `styles`: A list of style content strings to inline in the rendered page


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
[task-lists]: https://github.com/blog/1825-task-lists-in-all-markdown-documents
[rdd]: http://tom.preston-werner.com/2010/08/23/readme-driven-development.html
[gfm]: http://github.github.com/github-flavored-markdown
[python-markdown]: https://github.com/waylan/Python-Markdown
[authors.md]: AUTHORS.md
