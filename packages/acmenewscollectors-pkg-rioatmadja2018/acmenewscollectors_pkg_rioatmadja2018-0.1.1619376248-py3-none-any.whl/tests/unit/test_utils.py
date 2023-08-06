import pytest
from unittest import TestCase
from acme_news.utils.tools import get_synonyms
import os

class TestUtils(TestCase):
    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_get_synonyms(self):
        response = get_synonyms(word='eat')
        print(response)
        return self.assertEqual(31, response.__len__())