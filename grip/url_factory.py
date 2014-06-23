class UrlFactory(object):
    def build_github_url(self, use_flavored=True):
        return 'https://api.github.com/markdown' + ((not use_flavored) * "/raw")
