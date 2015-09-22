# The common titles and supported extensions,
# as defined by https://github.com/github/markup
supported_titles = ['README', 'Home']
supported_extensions = ['.md', '.markdown']


# The default filenames when no file is provided
default_filenames = [title + ext
                     for title in supported_titles
                     for ext in supported_extensions]


# The default URL to serve static assets at
default_static_url_path = '/grip-static'
