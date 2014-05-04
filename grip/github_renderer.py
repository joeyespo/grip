from flask import abort
import requests
from url_factory import UrlFactory
from request_context_factory import RequestContextFactory


def render_content(text, gfm=False, context=None, username=None, password=None):
    """Renders the specified markup using the GitHub API."""
    url = UrlFactory().build_github_url(gfm)

    request_context = RequestContextFactory().\
        using_auth(username, password).\
        use_github_markdown(gfm).\
        from_text(text).\
        from_context(context).\
        build_json_context()

    r = requests.post(url, **request_context)

    # Relay HTTP errors
    if r.status_code != 200:
        try:
            message = r.json()['message']
        except:
            message = r.text
        abort(r.status_code, message)

    return r.text
