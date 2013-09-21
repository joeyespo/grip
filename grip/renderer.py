from jinja2 import Environment, PackageLoader
from .github_renderer import render_content as github_render
from .offline_renderer import render_content as offline_render
from flask import make_response


# Get jinja templates
env = Environment(loader=PackageLoader('grip', 'templates'))


def render_content(text, gfm=False, context=None, render_offline=False,
                   username=None, password=None):
    """Renders the specified markup and returns the result."""
    if render_offline:
        return offline_render(text, gfm, context)
    return github_render(text, gfm, context, username, password)


def render_page(text, filename=None, gfm=False, context=None, render_offline=False,
                username=None, password=None, style_urls=[], style_url_contents=None):
    """Renders the specified markup text to an HTML page."""
    if style_url_contents:
        index_template = env.get_template('index_export.html')
    else:
        index_template = env.get_template('index.html')
        
    content = render_content(text, gfm, context, render_offline, username, password)
    return index_template.render(content=content, filename=filename,
                                 style_urls=style_urls,
                                 style_url_contents=style_url_contents)

def render_image(image_data, content_type):
    """Renders the specified image data with the given Content-Type."""
    response = make_response(image_data)
    response.headers['Content-Type'] = content_type
    return response
