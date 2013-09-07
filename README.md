Grip -- Github Readme Instant Preview
=====================================

Render local readme files before sending off to Github.

Grip is a command-line server application written in Python that uses the
[Github markdown API][markdown] to render a local readme file. The styles also
come directly from Github, so you'll know exactly how it will appear.


Motivation
----------

Sometimes you just want to see the exact readme
result before committing and pushing to Github.

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

GitHub-Flavored Markdown is also supported:

```bash
$ grip --gfm --context=joeyespo/grip
 * Running on http://localhost:5000/
```

For more details, see the help:

```bash
$ grip -h
```


API
---

You can access the API directly with Python, using it in your own projects:

```python
from grip import serve

serve(port=8080)
 * Running on http://localhost:80/
```

### Documentation

#### serve

Runs a local server and renders the Readme file located
at `path` when visited in the browser.

```python
serve(path='file-or-directory', host='localhost', port=5000, gfm=False, context=None, render_offline=False)
```

- `path`: The filename to render, or the directory containing your Readme file
- `host`: The host to serve on
- `port`: The port to serve on
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `render_offline`: Whether to render locally using [Python-Markdown][]


#### render_content

Renders the specified markdown text.

```python
render_content(text, gfm=False, context=None)
```

- `text`: The content to render
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `render_offline`: Whether to render locally using [Python-Markdown][]

#### render_page

Renders the specified markdown text and outputs an HTML page that resembles
the GitHub Readme view.

```python
render_page(text, filename=None, gfm=False, context=None, render_offline=False, style_urls=[])
```

- `text`: The content to render
- `gfm`: Whether to render using [GitHub Flavored Markdown][gfm]
- `context`: The project context to use when `gfm` is true, which
             takes the form of `username/project`
- `render_offline`: Whether to render offline using [Python-Markdown][]
- `style_urls`: A list of URLs that contain CSS to include in the
                rendered page

#### default_filenames

This constant contains the names Grip looks for when no file is given to.

```python
default_filenames = ['README.md', 'README.markdown']
```


Contributing
------------

1. Check the open issues or open a new issue to start a discussion around
   your feature idea or the bug you found
2. Fork the repository, make your changes, and add yourself to [Authors.md][]
3. Send a pull request


[markdown]: http://developer.github.com/v3/markdown
[rdd]: http://tom.preston-werner.com/2010/08/23/readme-driven-development.html
[gfm]: http://github.github.com/github-flavored-markdown
[python-markdown]: https://github.com/waylan/Python-Markdown
[authors.md]: AUTHORS.md
