# The common titles and supported extensions,
# as defined by https://github.com/github/markup
SUPPORTED_TITLES = ['README', 'Readme', 'readme', 'Home']
SUPPORTED_EXTENSIONS = ['.md', '.markdown']


# The default filenames when no file is provided
DEFAULT_FILENAMES = [title + ext
                     for title in SUPPORTED_TITLES
                     for ext in SUPPORTED_EXTENSIONS]
DEFAULT_FILENAME = DEFAULT_FILENAMES[0]


# The default directory to load Grip settings from
DEFAULT_GRIPHOME = '~/.grip'


# The default URL of the Grip server
DEFAULT_GRIPURL = '/__/grip'


# The public GitHub API
DEFAULT_API_URL = 'https://api.github.com'


# Style parsing
STYLE_URLS_SOURCE = 'https://github.com/joeyespo/grip'
STYLE_URLS_RE = (
    r'''<link.+href=['"]?([^'" >]+)['"]?.+media=['"]?(?:screen|all)['"]?.'''
    r'''+rel=['"]?stylesheet['"]?.+/>''')
STYLE_ASSET_URLS_RE = (
    r'''url\(['"]?(/static/fonts/octicons/[^'" \)]+)['"]?\)''')
STYLE_ASSET_URLS_SUB_FORMAT = r'url("{0}\1")'
STYLE_ASSET_URLS_INLINE_FORMAT = (
    r'''url\(['"]?((?:/static|{0})/[^'" \)]+)['"]?\)''')
