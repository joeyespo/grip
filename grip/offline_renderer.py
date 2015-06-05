import markdown
from .mdx_urlize import UrlizeExtension


def render_content(text, gfm=False, context=None):
    """
    Renders the specified markup locally.
    """
    return markdown.markdown(text, extensions=[
        'fenced_code',
        'codehilite(css_class=highlight)',
        'toc',
        'tables',
        UrlizeExtension(),
    ])
