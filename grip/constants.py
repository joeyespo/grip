# The supported extensions, as defined by https://github.com/github/markup
supported_extensions = ['.md', '.markdown']

# The default filenames when no file is provided
default_filenames = map(lambda ext: 'README' + ext, supported_extensions)
