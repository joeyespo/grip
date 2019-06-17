from __future__ import print_function, unicode_literals

import json
import sys
from abc import ABCMeta, abstractmethod

import requests

try:
    import markdown
    from .vendor.mdx_urlize import UrlizeExtension
except ImportError:
    markdown = None
    UrlizeExtension = None

from .constants import DEFAULT_API_URL
from .patcher import patch
from .vendor.six import add_metaclass


@add_metaclass(ABCMeta)
class ReadmeRenderer(object):
    """
    Renders the Readme.
    """
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
    def __init__(self, user_content=None, context=None, api_url=None,
                 raw=None):
        if api_url is None:
            api_url = DEFAULT_API_URL
        super(GitHubRenderer, self).__init__(user_content, context)
        self.api_url = api_url
        self.raw = raw

    def render(self, text, auth=None):
        """
        Renders the specified markdown content and embedded styles.

        Raises TypeError if text is not a Unicode string.
        Raises requests.HTTPError if the request fails.
        """
        # Ensure text is Unicode
        expected = str if sys.version_info[0] >= 3 else unicode  # noqa
        if not isinstance(text, expected):
            raise TypeError(
                'Expected a Unicode string, got {!r}.'.format(text))

        if self.user_content:
            url = '{0}/markdown'.format(self.api_url)
            data = {'text': text, 'mode': 'gfm'}
            if self.context:
                data['context'] = self.context
            data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            headers = {'content-type': 'application/json; charset=UTF-8'}
        else:
            url = '{0}/markdown/raw'.format(self.api_url)
            data = text.encode('utf-8')
            headers = {'content-type': 'text/x-markdown; charset=UTF-8'}

        r = requests.post(url, headers=headers, data=data, auth=auth)
        r.raise_for_status()

        # FUTURE: Remove this once GitHub API properly handles Unicode markdown
        r.encoding = 'utf-8'

        return r.text if self.raw else patch(r.text)


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
