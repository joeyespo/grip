from __future__ import print_function, unicode_literals

import json
import re
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


# Regular expression to match code blocks and inline code so that
# wikilinks inside them are not converted.
CODE_BLOCK_RE = re.compile(r'(?s)(```.*?```|~~~.*?~~~|``.*?``|`[^`\n]+`)')

# Matches wikilinks: [[target]] or [[target|label]]
WIKILINK_RE = re.compile(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')

# List of typical image extensions
IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.ico', '.tiff')


def preprocess_wikilinks(text):
    """
    Finds wikilinks like [[Page Name]] or [[images/photo.png|Alt text]] in text
    and converts them to standard markdown image/link equivalents,
    ignoring any wikilinks inside code blocks or code spans.
    """
    expected = str if sys.version_info[0] >= 3 else unicode  # noqa
    if not isinstance(text, expected):
        return text

    def replace_wikilink(match):
        target = match.group(1).strip()
        if not target:
            return match.group(0)

        label = match.group(2).strip() if match.group(2) is not None else None

        # Check if the target is an image based on its extension
        # (ignoring query parameters or anchors if any)
        clean_target = target.split('?')[0].split('#')[0]
        is_image = clean_target.lower().endswith(IMAGE_EXTS)

        if is_image:
            url = target.replace(' ', '%20')
            if label is not None:
                return '![{0}]({1})'.format(label, url)
            else:
                return '![]({0})'.format(url)
        else:
            if '://' not in target:
                slug = target.replace(' ', '-')
            else:
                slug = target

            if label is not None:
                return '[{0}]({1})'.format(label, slug)
            else:
                return '[{0}]({1})'.format(target, slug)

    parts = CODE_BLOCK_RE.split(text)
    for i in range(0, len(parts), 2):
        parts[i] = WIKILINK_RE.sub(replace_wikilink, parts[i])

    return ''.join(parts)


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

        text = preprocess_wikilinks(text)

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
        # Ensure text is Unicode
        expected = str if sys.version_info[0] >= 3 else unicode  # noqa
        if not isinstance(text, expected):
            raise TypeError(
                'Expected a Unicode string, got {!r}.'.format(text))

        text = preprocess_wikilinks(text)

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
