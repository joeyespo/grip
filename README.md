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
$ grip CHANGES.md
 * Running on http://localhost:5000/
```

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

serve(path='file-or-directory', host='localhost', port=5000, gfm=False, context=None)
```

Other functions include: `find_readme`, `render_content`, and `render_page`


Contributing
------------

1. Check the open issues or open a new issue to start a discussion around
   your feature idea or the bug you found
2. Fork the repository
3. Send a pull request


[markdown]: http://developer.github.com/v3/markdown
[rdd]: http://tom.preston-werner.com/2010/08/23/readme-driven-development.html
