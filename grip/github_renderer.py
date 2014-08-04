from flask import abort, json
import requests


def render_content(text, gfm=False, context=None,
                   username=None, password=None):
    """Renders the specified markup using the GitHub API."""
    if gfm:
        url = 'https://api.github.com/markdown'
        data = {'text': text, 'mode': 'gfm'}
        if context:
            data['context'] = context
        data = json.dumps(data)
        headers = {'content-type': 'application/json'}
    else:
        url = 'https://api.github.com/markdown/raw'
        data = text
        headers = {'content-type': 'text/x-markdown'}

    auth = (username, password) if username or password else None
    r = requests.post(url, headers=headers, data=data, auth=auth)

    # Relay HTTP errors
    if r.status_code != 200:
        try:
            message = r.json()['message']
        except:
            message = r.text
        abort(r.status_code, message)

    return r.text
