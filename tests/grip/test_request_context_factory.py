import sys
sys.path.append('../../grip/')

import unittest
from request_context_factory import RequestContextFactory

class TestRequestContextFactory(unittest.TestCase):

    def setUp(self):
        self.factory = RequestContextFactory()

    def test_Given_falsy_username_When_context_is_built_Then_it_has_no_auth_under_its_auth_key(self):
        # Given
        self.factory.using_auth(False, 'some password')

        # When
        context = self.factory.build_context()

        # Then
        self.assertEqual(None, context['auth'])

    def test_Given_falsy_password_When_context_is_built_Then_it_has_no_auth_under_its_auth_key(self):
        # Given
        self.factory.using_auth('some user', '')

        # When
        context = self.factory.build_context()

        # Then
        self.assertEqual(None, context['auth'])

    def test_Given_falsy_password_and_username_When_context_is_built_Then_it_has_no_auth_under_its_auth_key(self):
        # Given
        self.factory.using_auth(False, None)

        # When
        context = self.factory.build_context()

        # Then
        self.assertEqual(None, context['auth'])

    def test_Given_string_password_and_username_When_context_is_built_Then_it_has_user_and_pass_tuple_under_its_auth_key(self):
        # Given
        self.factory.using_auth('spam', 'eggs')

        # When
        context = self.factory.build_context()

        # Then
        self.assertEqual(('spam', 'eggs'), context['auth'])

    def test_headers_key_always_indicates_plain_text(self):
        context = self.factory.build_context()

        self.assertEqual('text/plain', context['headers']['content-type'])

    def test_Given_text_and_context_and_the_fact_we_want_gfm_When_context_is_built_Then_its_data_contains_the_passed_text_value(self):
        # Given
        self.factory.use_github_markdown(True).\
                     from_text('foobar').\
                     from_context('spameggs')

        # When
        context = self.factory.build_context()

        # Then
        self.assertEqual('foobar', context['data']['text'])

    def test_Given_text_and_context_and_the_fact_we_want_gfm_When_context_is_built_Then_its_data_contains_the_passed_context_value(self):
        # Given
        self.factory.use_github_markdown(True).\
                     from_text('foobar').\
                     from_context('spameggs')

        # When
        context = self.factory.build_context()

        # Then
        self.assertEqual('spameggs', context['data']['context'])

    def test_Given_text_and_context_and_the_fact_we_want_gfm_When_context_is_built_Then_its_data_contains_a_value_indicating_the_gfm_mode(self):
        # Given
        self.factory.use_github_markdown(True).\
                     from_text('foobar').\
                     from_context('spameggs')

        # When
        context = self.factory.build_context()

        # Then
        self.assertEqual('gfm', context['data']['mode'])

    def test_Given_text_and_context_and_the_fact_we_dont_want_gfm_When_context_is_built_Then_its_data_is_just_the_passed_text(self):
        # Given
        self.factory.use_github_markdown(False).\
                     from_text('foobar').\
                     from_context('spameggs')

        # When
        context = self.factory.build_context()

        # Then
        self.assertEqual('foobar', context['data'])

    def test_Given_text_and_context_and_the_fact_we_want_gfm_When_json_data_context_is_built_Then_its_data_is_expected_json(self):
        # Given
        self.factory.use_github_markdown(True).\
                     from_text('foobar').\
                     from_context('spameggs')

        # When
        context = self.factory.build_json_context()

        # Then
        self.assertEqual('{"context": "spameggs", "mode": "gfm", "text": "foobar"}', context['data'])
    
    def test_Given_text_and_context_and_the_fact_we_dont_want_gfm_When_json_data_context_is_built_Then_its_data_is_just_the_passed_text(self):
        # Given
        self.factory.use_github_markdown(False).\
                     from_text('foobar').\
                     from_context('spameggs')

        # When
        context = self.factory.build_json_context()

        # Then
        self.assertEqual('foobar', context['data'])

if __name__ == '__main__':
    unittest.main()
