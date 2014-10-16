from __future__ import unicode_literals

from unittest.case import TestCase

try:
    import urlparse                         # python 2
except ImportError:
    from urllib import parse as urlparse    # python 3

import mock
from requests.models import Request

from brandstem.client import BrandStem, BrandStemResponse


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

    def test_compute_signature(self):
        signature = self.client.compute_signature('test_path', '1000')
        self.assertEqual(signature, '1476733a83d3ac14069afe99e2831e3fad56498132c718b8e97f3a77c4e87c26')

    def test_get(self):
        request = self.client.get('/category', 1, BrandStem.DEFAULT_PAGE_SIZE)
        self.assertTrue('X-Brandstem-Date' in request.headers)
        self.assertTrue('X-Brandstem-Access-Id' in request.headers)
        self.assertTrue('X-Brandstem-Signature' in request.headers)
        self.assertEqual(request.method, 'GET')

        parse_result = urlparse.urlparse(request.url)
        self.assertEqual(parse_result.scheme, 'https')
        self.assertEqual(parse_result.netloc, 'brandstem.ca')
        self.assertEqual(parse_result.path, '/api/v2/category')
        self.assertEqual(
            urlparse.parse_qs(parse_result.query),
            {'page': ['1'], 'page_size': ['100']}
        )

    @mock.patch('brandstem.client.Session')
    def test_send(self, mock_session_cls):
        request = Request('GET', 'http://example.com/', {})
        request = request.prepare()

        response = mock.MagicMock()
        response.content = b'{}'

        session = mock.MagicMock()
        mock_session_cls.return_value = session
        session.send.return_value = response

        response = self.client.send(request)
        self.assertEqual(type(response), BrandStemResponse)
        session.send.assert_called_once_with(request)
