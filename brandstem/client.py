import time
import hashlib
import hmac
import json
import collections

from requests.models import Request
from requests.sessions import Session


class BrandStemResponse(collections.Sequence):

    def __init__(self, response):
        self.response = response.content
        response = json.loads(response.content)
        self.count = response.get('count')
        self.page = response.get('page')
        self.num_pages = response.get('num_pages')
        self.object_list = response.get('object_list')

    def __len__(self):
        if self.object_list:
            return len(self.object_list)
        else:
            return None

    def __getitem__(self, index):
        if self.object_list:
            return self.object_list[index]
        else:
            return None


class BrandStem(object):

    SCHEME = 'https'
    HOST = 'brandstem.ca'
    DEFAULT_PAGE_SIZE = 100

    def __init__(self, access_id, access_secret):
        self.access_id = access_id
        self.access_secret = access_secret

    @staticmethod
    def get_unix_date():
        return int(time.time())

    def compute_signature(self, path, unix_date):
        key = str(unix_date) + self.access_secret
        signature_computed = hmac.new(key=str(key), msg=path, digestmod=hashlib.sha256).hexdigest()
        return signature_computed

    def get(self, endpoint, page, page_size, params=None):
        params = params or {}
        params.update({
            'page': page,
            'page_size': page_size,
        })

        url = '{scheme}://{host}/api/v2{endpoint}'.format(scheme=self.SCHEME, host=self.HOST, endpoint=endpoint)

        request = Request('GET', url, params=params)
        request = request.prepare()

        unix_date = self.get_unix_date()
        signature = self.compute_signature(request.path_url, unix_date)

        request.headers.update({
            'X-Brandstem-Date': unix_date,
            'X-Brandstem-Access-Id': self.access_id,
            'X-Brandstem-Signature': signature,
        })

        return request

    def send(self, request):
        session = Session()
        response = session.send(request)
        return BrandStemResponse(response)

    def get_category_list(self, category_id=None, page=1, page_size=DEFAULT_PAGE_SIZE):
        if category_id:
            endpoint = '/category/{}/children'.format(category_id)
        else:
            endpoint = '/category'
        return self.send(self.get(endpoint, page, page_size))

    def get_category(self, category_id, page=1, page_size=DEFAULT_PAGE_SIZE):
        endpoint = '/category/{}'.format(category_id)
        return self.send(self.get(endpoint, page, page_size))

    def get_category_product_list(self, category_id, page=1, page_size=DEFAULT_PAGE_SIZE):
        endpoint = '/category/{}/products'.format(category_id)
        return self.send(self.get(endpoint, page, page_size))

    def get_category_product_list_all(self, category_id, page=1, page_size=DEFAULT_PAGE_SIZE):
        endpoint = '/category/{}/products?type=all'.format(category_id)
        return self.send(self.get(endpoint, page, page_size))

    def search_category(self, name, page=1, page_size=DEFAULT_PAGE_SIZE):
        endpoint = '/search/category'
        return self.send(self.get(endpoint, page, page_size, {'name': name}))

    def get_product(self, product_id, page=1, page_size=DEFAULT_PAGE_SIZE):
        endpoint = '/product/{}'.format(product_id)
        return self.send(self.get(endpoint, page, page_size))

    def search_product_by_name(self, name, page=1, page_size=DEFAULT_PAGE_SIZE):
        endpoint = '/search/product'
        return self.send(self.get(endpoint, page, page_size, {'name': name}))

    def search_product_by_gtin(self, gtin, page=1, page_size=DEFAULT_PAGE_SIZE):
        endpoint = '/search/product'
        return self.send(self.get(endpoint, page, page_size, {'gtin': gtin}))

    def get_campaign_list(self, page=1, page_size=DEFAULT_PAGE_SIZE):
        endpoint = '/campaign'
        return self.send(self.get(endpoint, page, page_size))

    def get_campaign(self, campaign_id, page=1, page_size=DEFAULT_PAGE_SIZE):
        endpoint = '/campaign/{}'.format(campaign_id)
        return self.send(self.get(endpoint, page, page_size))

    def get_campaign_product_list(self, campaign_id, page=1, page_size=DEFAULT_PAGE_SIZE):
        endpoint = '/campaign/{}/products'.format(campaign_id)
        return self.send(self.get(endpoint, page, page_size))

    def get_category_descendants_list(self, category_id, page=1, page_size=DEFAULT_PAGE_SIZE):
        endpoint = '/category/{}/descendants'.format(category_id)
        return self.send(self.get(endpoint, page, page_size))

    def get_flyer(self):
        endpoint = '/flyer'
        # flyers are not paginated
        return self.send(self.get(endpoint, 1, 100))

    def get_flyer_items(self, flyer_id):
        endpoint = '/flyer/{}'.format(flyer_id)
        # flyers are not paginated
        return self.send(self.get(endpoint, 1, 100))

    def get_flyer_items_by_zone(self, flyer_id, flyer_zone):
        endpoint = '/flyer/{}'.format(flyer_id)
        # flyers are not paginated
        return self.send(self.get(endpoint, 1, 100, {'flyer_zone': flyer_zone}))

    def get_flyer_items_by_page(self, flyer_id, flyer_page):
        endpoint = '/flyer/{}'.format(flyer_id)
        # flyers are not paginated
        return self.send(self.get(endpoint, 1, 100, {'flyer_page': flyer_page}))

    def get_flyer_zones(self, flyer_id):
        endpoint = '/flyer/{}/zones'.format(flyer_id)
        # flyers are not paginated
        return self.send(self.get(endpoint, 1, 100))

    def get_offers(self, offer_id):
        endpoint = '/offer/{}'.format(offer_id)
        # flyers are not paginated
        return self.send(self.get(endpoint, 1, 100))
