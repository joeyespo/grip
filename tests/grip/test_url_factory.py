import sys
sys.path.append('../../grip/')

import unittest
from url_factory import UrlFactory

class TestUrlFactory(unittest.TestCase):

    def setUp(self):
        self.factory = UrlFactory()

    def test_Given_want_github_flavored_markdown_When_url_is_built_Then_url_is_github_markdown(self):
        # Given
        want_github_flavored_markdown = True

        # When
        url = self.factory.build_github_url(want_github_flavored_markdown)

        # Then
        self.assertEqual('https://api.github.com/markdown', url)

    def test_Given_dont_want_github_flavored_markdown_When_url_is_built_Then_url_is_github_markdown_raw(self):
        # Given
        want_github_flavored_markdown = False

        # When
        url = self.factory.build_github_url(want_github_flavored_markdown)

        # Then
        self.assertEqual('https://api.github.com/markdown/raw', url)

    def test_Given_nothing_is_specified_When_url_is_built_Then_url_is_github_markdown(self):
        # Given/When
        url = self.factory.build_github_url()

        # Then
        self.assertEqual('https://api.github.com/markdown', url)


if __name__ == '__main__':
    unittest.main()
