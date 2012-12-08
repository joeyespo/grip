from jinja2 import Environment, PackageLoader
import requests

json = None
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        pass


# Get jinja templates
env = Environment(loader=PackageLoader('grip', 'templates'))
index_template = env.get_template('index.html')


def render_content(text, gfm=None, context=None):
    """Renders the specified markup."""
    if gfm:
        url = 'https://api.github.com/markdown'
        data = {'text': text, 'mode': 'gfm', 'context': context}
        if context:
            data['context'] = context
        data = json.dumps(data)
    else:
        url = 'https://api.github.com/markdown/raw'
        data = text
    headers = {'content-type': 'text/plain'}
    r = requests.post(url, headers=headers, data=data)
    return r.text


def render_page(text, filename=None, gfm=None, context=None, style_urls=[]):
    """Renders the specified markup text to an HTML page."""
    return index_template.render(content=render_content(text, gfm, context), filename=filename, style_urls=style_urls)
