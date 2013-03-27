import misaka
from misaka import (HTML_ESCAPE, HTML_SAFELINK, EXT_FENCED_CODE,
                    EXT_NO_INTRA_EMPHASIS, EXT_TABLES, EXT_AUTOLINK,
                    EXT_SPACE_HEADERS, EXT_STRIKETHROUGH, EXT_SUPERSCRIPT)

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

def _get_lexer_or_default(lang):
    try:
        return get_lexer_by_name(lang, stripall=True)
    except ClassNotFound:
        return get_lexer_by_name('text', stripall=True)

class HighlightingRenderer(misaka.HtmlRenderer, misaka.SmartyPants):
    def block_code(self, text, lang):
        lexer = _get_lexer_or_default(lang)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

def render_content(text, gfm=False, context=None):
    renderer_flags = HTML_ESCAPE | HTML_SAFELINK
    extensions = (EXT_FENCED_CODE | EXT_NO_INTRA_EMPHASIS | EXT_TABLES
                | EXT_AUTOLINK | EXT_SPACE_HEADERS | EXT_STRIKETHROUGH
                | EXT_SUPERSCRIPT)
    renderer = HighlightingRenderer(flags=renderer_flags)
    return misaka.Markdown(renderer, extensions=extensions).render(text)
