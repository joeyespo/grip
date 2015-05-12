from .github_renderer import render_content as github_render
from .offline_renderer import render_content as offline_render


def render_app(app, route='/'):
    """Renders the markup at the specified app route."""
    with app.test_client() as c:
        response = c.get('/')
        encoding = response.charset
        return response.data.decode(encoding)


def render_content(text, gfm=False, context=None,
                   username=None, password=None, api_url=None,
                   render_offline=False):
    """Renders the specified markup and returns the result."""
    return (offline_render(text, gfm, context) if render_offline
        else github_render(text, api_url, gfm, context, username, password))
