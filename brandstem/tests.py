from __future__ import unicode_literals

from unittest.case import TestCase
from brandstem.client import BrandStem


class BrandStemClientTests(TestCase):

    access_id = 'test_access_id'
    access_secret = 'test_access_secret'

    def setUp(self):
        super(BrandStemClientTests, self).setUp()
        self.client = BrandStem(self.access_id, self.access_secret)

    def test_init(self):
        client = self.client
        self.assertEqual(client.access_id, self.access_id)
        self.assertEqual(client.access_secret, self.access_secret)

    def test_get_unix_date(self):
        self.assertEqual(type(self.client.get_unix_date()), int)
