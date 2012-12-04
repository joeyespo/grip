Grip -- Github Readme Instant Preview
=====================================

Render local readme files before sending off to Github.

Grip is a command-line server application written in Python that uses the
Github [markup API][markdown] to render a local readme file. The styles also
come directly from Github, so you'll know exactly how it will appear.


Motivation
----------

Sometimes you just want to see the exact readme
result before committing and pushing to Github.

Especially when doing [Readme-driven development][rdd].


Installation
------------

To install grip, simply:

    $ pip install grip


Usage
-----

To render the readme of a repository:

    $ cd myrepo
    $ grip [port]

Now open a browser and visit [http://localhost:5000](http://localhost:5000/).


API
---

You can access the API directly with Python, using it in your own projects:

    from grip import serve
    
    serve(directory='path-to-your-file', port=8080)

Other functions include: `find_readme`, `render_content`, and `render_page`


Contributing
------------

1. Check the open issues or open a new issue to start a discussion around
   your feature idea or the bug you found
2. Fork the repository
3. Send a pull request


[markdown]: http://developer.github.com/v3/markdown/
[rdd]: http://tom.preston-werner.com/2010/08/23/readme-driven-development.html
