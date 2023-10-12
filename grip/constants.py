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


# default URL for loading MathJax
DEFAULT_MATH_JAX_URL = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-chtml.min.js'

# script tag parsing
SCRIPT_URLS_SOURCE = 'https://github.com/joeyespo/grip'
SCRIPT_FILENAMES_RES = [
   r'''/wp-runtime-[0-9a-zA-Z]*\.js$''',
   r'''/element-registry-[0-9a-zA-Z]*\.js$'''
]
SCRIPT_URLS_RES = [
    r'''\"(https://github.githubassets.com/assets/wp-runtime-[0-9a-zA-Z]*\.js)\"''',
    r'''\"(https://github.githubassets.com/assets/element-registry-[0-9a-zA-Z]*\.js)\"'''
]

# Style parsing
STYLE_URLS_SOURCE = 'https://github.com/joeyespo/grip'
# Note: Using a list in case the implementation limitation is a problem
# https://docs.python.org/3/library/re.html#re.findall
STYLE_URLS_RES = [
    r'''<link\b[^>]+\bhref=['"]?([^'" >]+)['"]?\brel=['"]?stylesheet['"]?[^>]+[^>]*(?=>)''',
    r'''<link\b[^>]+\brel=['"]?stylesheet['"]?[^>]+\bhref=['"]?([^'" >]+)['"]?[^>]*(?=>)''',
]
STYLE_ASSET_URLS_RE = (
    r'''url\(['"]?(/static/fonts/octicons/[^'" \)]+)['"]?\)''')
STYLE_ASSET_URLS_SUB_FORMAT = r'url("{0}\1")'
STYLE_ASSET_URLS_INLINE_FORMAT = (
    r'''url\(['"]?((?:/static|{0})/[^'" \)]+)['"]?\)''')
