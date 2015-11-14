try:
    import markdown
    from .mdx_urlize import UrlizeExtension
except ImportError:
    markdown = None
    UrlizeExtension = None


def render_content(text, user_content=False, context=None):
    """
    Renders the specified markup locally.
    """
    if markdown is None:
        import markdown
    if UrlizeExtension is None:
        from .mdx_urlize import UrlizeExtension
    return markdown.markdown(text, extensions=[
        'fenced_code',
        'codehilite(css_class=highlight)',
        'toc',
        'tables',
        'sane_lists',
        UrlizeExtension(),
    ])
