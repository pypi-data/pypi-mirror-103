"""builder for redis url requests V1"""
from requests.utils import quote
from bbog_sg_python_redis_lib import config
from bbog_sg_python_redis_lib.utils import logging_utils

LOGGER = logging_utils.configure_logging(__name__)

API_URL = config.REDIS_API_URL
API_PATH = config.REDIS_API_PATH


class UrlBuilder:
    """create urls to access redis resources"""

    @staticmethod
    def __get_base_url() -> str:
        api_url = UrlBuilder.format_url(API_URL)
        api_path = UrlBuilder.format_url(API_PATH)
        return '{}/{}'.format(api_url, api_path)

    @staticmethod
    def get_url_for_key(key: str) -> str:
        r"""return url for single key
            :param str key: key name
            :return str formatted with path and key name
            :rtype: str: formed url
            """
        base_url = UrlBuilder.__get_base_url()
        return '{}/{}'.format(base_url, quote(key))

    @staticmethod
    def get_url_for_hash_key(key: str, hash_key: str) -> str:
        """return url for get key"""
        base_url = UrlBuilder.__get_base_url()
        return '{}/{}/{}'.format(base_url, quote(key), quote(hash_key))

    @staticmethod
    def get_url_for_all_hash_key(key) -> str:
        """return url for get key"""
        base_url = UrlBuilder.__get_base_url()
        return '{}/{}/{}'.format(base_url, quote(key), 'fields')

    @staticmethod
    def format_url(url) -> str:
        formed_url = url[1:] if url.startswith('/') else url
        return formed_url[:-1] if formed_url.endswith('/') else formed_url
