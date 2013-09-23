from jinja2 import Environment, PackageLoader
from flask import make_response
from .github_renderer import render_content as github_render
from .offline_renderer import render_content as offline_render


# Get jinja templates
env = Environment(loader=PackageLoader('grip', 'templates'))
index_template = env.get_template('index.html')


def render_app(app, route='/'):
    """Renders the markup at the specified app route."""
    with app.test_client() as c:
        response = c.get('/')
        encoding = response.charset
        return response.data.decode(encoding)


def render_content(text, gfm=False, context=None,
                   username=None, password=None, render_offline=False):
    """Renders the specified markup and returns the result."""
    if render_offline:
        return offline_render(text, gfm, context)
    return github_render(text, gfm, context, username, password)


def render_page(text, filename=None, gfm=False, context=None,
                username=None, password=None, render_offline=False,
                style_urls=[], styles=[]):
    """Renders the specified markup text to an HTML page."""
    content = render_content(text, gfm, context, username, password, render_offline)
    return index_template.render(content=content, filename=filename,
                                 style_urls=style_urls, styles=styles)


def render_image(image_data, content_type):
    """Renders the specified image data with the given Content-Type."""
    response = make_response(image_data)
    response.headers['Content-Type'] = content_type
    return response
