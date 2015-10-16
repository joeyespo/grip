from __future__ import print_function, unicode_literals

import json
from abc import ABCMeta, abstractmethod

import requests
try:
    import markdown
    from .mdx_urlize import UrlizeExtension
except ImportError:
    markdown = None
    UrlizeExtension = None


class ReadmeRenderer(object):
    """
    Renders the Readme.
    """
    __metaclass__ = ABCMeta

    def __init__(self, user_content=None, context=None):
        if user_content is None:
            user_content = False
        super(ReadmeRenderer, self).__init__()
        self.user_content = user_content
        self.context = context

    @abstractmethod
    def render(self, text, auth=None):
        """
        Renders the specified markdown content and embedded styles.
        """
        pass


class GitHubRenderer(ReadmeRenderer):
    """
    Renders the specified Readme using the GitHub Markdown API.
    """
    def __init__(self, user_content=None, context=None, api_url=None):
        super(GitHubRenderer, self).__init__(user_content, context)
        self.api_url = api_url

    def render(self, text, auth=None):
        """
        Renders the specified markdown content and embedded styles.

        Raises requests.HTTPError if the request fails.
        """
        if self.user_content:
            url = '{}/markdown'.format(self.api_url)
            data = {'text': text, 'mode': 'gfm'}
            if self.context:
                data['context'] = self.context
            data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            headers = {'content-type': 'application/json; charset=UTF-8'}
        else:
            url = '{}/markdown/raw'.format(self.api_url)
            data = text.encode('utf-8')
            headers = {'content-type': 'text/x-markdown; charset=UTF-8'}

        r = requests.post(url, headers=headers, data=data, auth=auth)
        r.raise_for_status()
        return r.text


class OfflineRenderer(ReadmeRenderer):
    """
    Renders the specified Readme locally using pure Python.

    Note: This is currently an incomplete feature.
    """
    def __init__(self, user_content=None, context=None):
        super(OfflineRenderer, self).__init__(user_content, context)

    def render(self, text, auth=None):
        """
        Renders the specified markdown content and embedded styles.
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
