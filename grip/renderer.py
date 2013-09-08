from jinja2 import Environment, PackageLoader
from .github_renderer import render_content as github_render
from .offline_renderer import render_content as offline_render


# Get jinja templates
env = Environment(loader=PackageLoader('grip', 'templates'))
index_template = env.get_template('index.html')


def render_content(text, gfm=False, context=None, render_offline=False, username=None, password=None):
    if render_offline:
        return offline_render(text, gfm, context)
    return github_render(text, gfm, context, username, password)


def render_page(text, filename=None, gfm=False, context=None,
                render_offline=False, username=None, password=None, style_urls=[]):
    """Renders the specified markup text to an HTML page."""
    content = render_content(text, gfm, context, render_offline, username, password)
    return index_template.render(content=content, filename=filename, style_urls=style_urls)
