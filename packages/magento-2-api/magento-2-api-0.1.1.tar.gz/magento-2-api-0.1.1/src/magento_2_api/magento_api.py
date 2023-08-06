import requests


class MagentoApi:

    rest_path = '/rest/default/V1'

    def __init__(self, url, access_token):
        self.url = url
        self.headers = {"Authorization": "Bearer " + access_token}

    def product_api(self, sku):
        """Makes a call to a Magento 2 REST API at
        /rest/default/V1/products/{sku}

        Args:
            sku (str): The product SKU to query.

        Returns:
            Response: Information on product with given SKU.
        """
        endpoint = self.rest_path + '/products/' + str(sku)
        return self.__call_api(endpoint)

    def product_media_api(self, sku):
        """Makes a call to a Magento 2 REST API at
        /rest/default/V1/products/{sku}/media/

        Args:
            sku (str): The product SKU to query.

        Returns:
            Response: Information on product media for given SKU.
        """
        endpoint = self.rest_path + '/products/' + str(sku) + '/media/'
        return self.__call_api(endpoint)

    def categories_api(self):
        """Makes a call to a Magento 2 REST API at
        /rest/default/V1/categories/

        Returns:
            Response: Information on categories for the website.
        """
        endpoint = self.rest_path + '/categories/'
        return self.__call_api(endpoint)

    def categories_products_api(self, category_id):
        """Makes a call to a Magento 2 REST API at
        /rest/default/V1/categories/{category_id}/products/

        Args:
            category_id (int): The category ID to query.

        Returns:
            Response: Information on products in the given category.
        """
        endpoint = (self.rest_path + '/categories/' + str(category_id)
                    + '/products/')
        return self.__call_api(endpoint)

    def __call_api(self, endpoint):
        return requests.get(self.url + endpoint, headers=self.headers)
