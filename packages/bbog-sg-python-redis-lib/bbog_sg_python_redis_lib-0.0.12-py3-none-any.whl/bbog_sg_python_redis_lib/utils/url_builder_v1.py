"""builder for redis url requests"""
from requests.utils import quote
from bbog_sg_python_redis_lib import config
from bbog_sg_python_redis_lib.utils import logging_utils
from bbog_sg_python_redis_lib.utils.url_builder import UrlBuilder

LOGGER = logging_utils.configure_logging(__name__)

API_URL = config.REDIS_API_URL


class UrlBuilderV1:
    """create urls to access redis resources"""

    @staticmethod
    def get_url_for_set_key(key: str) -> str:
        r"""return url for single key
            :param str key: key name
            :return str formatted with path and key name
            :rtype: str: formed url
            """
        api_url = UrlBuilder.format_url(API_URL)
        return '{}/{}/{}'.format(api_url, 'set', quote(key))

    @staticmethod
    def get_url_for_get_key(key: str) -> str:
        r"""return url for single key
            :param str key: key name
            :return str formatted with path and key name
            :rtype: str: formed url
            """
        api_url = UrlBuilder.format_url(API_URL)
        return '{}/{}/{}'.format(api_url, 'get', quote(key))

    @staticmethod
    def get_url_for_hash_key(key: str, hash_key: str) -> str:
        """return url for get key"""
        api_url = UrlBuilder.format_url(API_URL)
        return '{}/{}/{}'.format(api_url, 'hash', quote(key), quote(hash_key))
