from email.utils import formatdate
import hashlib
import hmac
from requests.models import Request
from requests.sessions import Session


class BrandStem(object):

    HOST = 'localhost:8000'
    DEFAULT_PAGE_SIZE = 100

    def __init__(self, access_id, access_secret):
        self.access_id = access_id
        self.access_secret = access_secret

    @staticmethod
    def get_rfc_date():
        return formatdate(usegmt=True)

    def compute_signature(self, path, rfc_date):
        key = rfc_date + self.access_secret
        signature_computed = hmac.new(key=key, msg=path, digestmod=hashlib.sha256).hexdigest()
        return signature_computed

    def get(self, path, params=None):
        session = Session()
        url = 'http://{}{}'.format(self.HOST, path)

        request = Request('GET', url, params=params)
        request = request.prepare()

        rfc_date = self.get_rfc_date()
        signature = self.compute_signature(request.path_url, rfc_date)

        request.headers.update({
            'X-Brandstem-Date': rfc_date,
            'X-Brandstem-Access-Id': self.access_id,
            'X-Brandstem-Signature': signature,
        })

        # TODO: DQ remember to add cert and timeout
        response = session.send(request)
        return response

    def get_category_list(self, page=1, page_size=DEFAULT_PAGE_SIZE, category_id=None):
        if category_id:
            path = '/api/v2/category/{}/children'.format(category_id)
        else:
            path = '/api/v2/category'

        response = self.get(path, {
            'page': page,
            'page_size': page_size,
        })
        return response.json()
