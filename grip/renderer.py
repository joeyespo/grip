from .github_renderer import render_content as github_render
from .offline_renderer import render_content as offline_render


def render_app(app, route='/'):
    """
    Renders the markup at the specified app route.
    """
    with app.test_client() as c:
        response = c.get('/')
        encoding = response.charset
        return response.data.decode(encoding)


def render_content(text, user_content=False, context=None, username=None,
                   password=None, render_offline=False, api_url=None):
    """
    Renders the specified markup and returns the result.
    """
    if not render_offline and api_url is None:
        ValueError('Argument api_url is required when not rendering offline.')
    return (offline_render(text, user_content, context)
            if render_offline
            else github_render(text, api_url, user_content, context, username,
                               password))
