python-brandstem
================

Brandstem API Client written for Python 2.7.

To use this client you will need an Access ID and Access Secret provided by the BrandStem Team.

Installing
----------

    >pip install git+ssh://git@github.com/stjosephcontent/python-brandstem


Connecting
----------

Create a BrandSteam connection to the API:

    from PythonBrandStem.client import BrandStem

    access_id = '<access_id>'
    access_secret = '<access_secret>'
    connection = BrandStem(access_id, access_secret)

Use the BrandStem connection and its methods to make API calls:

    connection.get_category_list()

Calls
-----

The calls return a BrandStemResponse object. The available methods to call from a BrandStem connection are:

List all the root categories. endpoint: `/api/v2/category`

    get_category_list(page=1, page_size=DEFAULT_PAGE_SIZE)


List the children of a category. endpoint: `/api/v2/category/<category_id:int>/children`

    get_category_list(category_id, page=1, page_size=DEFAULT_PAGE_SIZE)


Return a category by ID. endpoint: `/api/v2/category/<category_id:int>`

    get_category(category_id, page=1, page_size=DEFAULT_PAGE_SIZE)


List the products in a category. endpoint: `/api/v2/category/<category_id:int>/products`

    get_category_product_list(category_id, page=1, page_size=DEFAULT_PAGE_SIZE)


Search categories by name (English and French). endpoint: `/api/v2/search/category?name=<name>`

    search_category(name, page=1, page_size=DEFAULT_PAGE_SIZE)


Return an product by ID. endpoint: `/api/v2/product/<product_id:int>`

    get_product(product_id, page=1, page_size=DEFAULT_PAGE_SIZE)


Search for products by name (English and French). endpoint: `/api/v2/search/product?name=<name>`

    search_product_by_name(name, page=1, page_size=DEFAULT_PAGE_SIZE)


Search for products by gtin. endpoint: `/api/v2/search/product?gtin=<gtin>`

    search_product_by_gtin(gtin, page=1, page_size=DEFAULT_PAGE_SIZE)


Returns all campaigns. endpoint: `/api/v2/campaign`

    get_campaign_list(page=1, page_size=DEFAULT_PAGE_SIZE)


Returns a campaign by ID. endpoint: `/api/v2/campaign/<campaign_id>`

    get_campaign(campaign_id, page=1, page_size=DEFAULT_PAGE_SIZE)


List the Active Qualified Listed products in a campaign. endpoint: `/api/v2/campaign/<campaign_id:int>/products`

    get_campaign_product_list(campaign_id, page=1, page_size=DEFAULT_PAGE_SIZE)

Full Example
------------

    from pythonbrandstem.client import BrandStem

    access_id = '<access_id>'
    access_secret = '<access_secret>'
    connection = BrandStem(access_id, access_secret)

    connection = BrandStem(access_id,access_secret)

    # search for all fo the root categories
    category_list = connection.get_category_list()

    # show the number of results returned
    print category_list.count

    # show the current page number of the results
    print category_list.page

    # show the total number of pages of this search
    print category_list.num_pages

    # show all of the objects returned on this page
    print category_list.object_list

    # loop through the results and show the names
    for object in category_list.object_list:
        print object['name_en']

    # show the response in its entirety
    print category_list.response

    # show page two of the categories list, paginated at 50 objects per page
    category_list = connection.get_category_list(page=2, page_size=50)

License
-------

Copyright 2014 St. Joseph Communications

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
