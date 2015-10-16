import requests
from flask import abort, json


def render_content(text, api_url, user_content=False, context=None,
                   username=None, password=None):
    """
    Renders the specified markup using the GitHub API.
    """
    if user_content:
        url = '{}/markdown'.format(api_url)
        data = {'text': text, 'mode': 'gfm'}
        if context:
            data['context'] = context
        data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        headers = {'content-type': 'application/json; charset=UTF-8'}
    else:
        url = '{}/markdown/raw'.format(api_url)
        data = text.encode('utf-8')
        headers = {'content-type': 'text/x-markdown; charset=UTF-8'}

    auth = (username, password) if username or password else None
    r = requests.post(url, headers=headers, data=data, auth=auth)

    # Relay HTTP errors
    if r.status_code != 200:
        try:
            message = r.json()['message']
        except Exception:
            message = r.text
        abort(r.status_code, message)

    return r.text
