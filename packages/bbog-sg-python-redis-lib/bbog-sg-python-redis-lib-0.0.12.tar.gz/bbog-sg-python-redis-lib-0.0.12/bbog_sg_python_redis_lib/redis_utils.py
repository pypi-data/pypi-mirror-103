"""class to handle Redis api for python client"""
import json
import uuid
import requests
from bbog_sg_python_redis_lib.models import TimeUnitEnum, HttpMethodEnum
from bbog_sg_python_redis_lib.utils.url_builder import UrlBuilder
from bbog_sg_python_redis_lib import config
from bbog_sg_python_redis_lib.utils import logging_utils
from bbog_sg_python_redis_lib.utils.url_builder_v1 import UrlBuilderV1

LOGGER = logging_utils.configure_logging(__name__)
APPLICATION_JSON = 'application/json'
RESPONSE_FORMATTER = 'Response status code: %s, and body: %s'


class RedisUtils:
    r"""Create a client to handle redis api."""

    @staticmethod
    def set_key(key: str, value: str or object, time: int or str, time_unit: str or TimeUnitEnum,
                rq_uid=str(uuid.uuid4())) -> bool:
        r""" save a key in redis and return a boolean if it was possible or not to save a key.
            :param str key: name of the key to save
            :param str or dict value: value of the key to save
            :param str or int time: key life time
            :param str or TimeUnitEnum time_unit: time unit of the key
            :param str or None rq_uid: unique request identifier
            :return bool that says if the save of the key was successful
            :rtype bool
            usage: redis_response = RedisUtils.set_key('hola','mundo',15, TimeUnitEnum.Minutes)"""
        method = HttpMethodEnum.POST.value
        parsed_time = RedisUtils.__handle_time(time)
        parsed_time_unit = RedisUtils.__handle_time_unit(time_unit)
        parsed_value = RedisUtils.__handle_value(value)
        headers = RedisUtils.__generate_default_headers()
        headers.__setitem__('X-Time', str(parsed_time))
        headers.__setitem__('X-TimeUnit', str(parsed_time_unit))
        headers.__setitem__('X-RqUID', rq_uid)
        url = UrlBuilder.get_url_for_key(key)
        LOGGER.info("Url obtained: %s for set key: %s value: %s", url, key, parsed_value)
        response = RedisUtils.__make_http_call(url=url,
                                               headers=headers,
                                               method=method,
                                               value=parsed_value)
        response_status_code = response.status_code
        response_as_string = response.text
        LOGGER.info(RESPONSE_FORMATTER, response_status_code,
                    response_as_string)
        return response_status_code == 200

    @staticmethod
    def set_key_v1(key: str, value: str or object, time: int or str, time_unit: str or TimeUnitEnum,
                   rq_uid=str(uuid.uuid4())) -> bool:
        r""" save a key in redis and return a boolean if it was possible or not to save a key.
            :param str key: name of the key to save
            :param str or dict value: value of the key to save
            :param str or int time: key life time
            :param str or TimeUnitEnum time_unit: time unit of the key
            :param str or None rq_uid: unique request identifier
            :return bool that says if the save of the key was successful
            :rtype bool
            usage: redis_response = RedisUtils.set_key('hola','mundo',15, TimeUnitEnum.Minutes)"""
        method = HttpMethodEnum.POST.value
        parsed_time = RedisUtils.__handle_time(time)
        parsed_time_unit = RedisUtils.__handle_time_unit(time_unit)
        parsed_value = RedisUtils.__handle_value(value)
        headers = RedisUtils.__generate_default_headers()
        headers.__setitem__('time', str(parsed_time))
        headers.__setitem__('time-unit', str(parsed_time_unit))
        headers.__setitem__('X-RqUID', rq_uid)
        url = UrlBuilderV1.get_url_for_set_key(key)
        LOGGER.info("Url obtained: %s for set key: %s value: %s", url, key, parsed_value)
        response = RedisUtils.__make_http_call(url=url,
                                               headers=headers,
                                               method=method,
                                               value=parsed_value)
        response_status_code = response.status_code
        response_as_string = response.text
        LOGGER.info(RESPONSE_FORMATTER, response_status_code,
                    response_as_string)
        return response_status_code == 200

    @staticmethod
    def get_key(key: str, rq_uid=str(uuid.uuid4())) -> str:
        r""" get a key saved in redis and return str if it was possible to get a key else return None.
            :param str key: name of the key to retrieve
            :return str with the value of the key or None
            :rtype None or str
            :usage: redis_response = RedisUtils.get_key('Key')"""
        method = HttpMethodEnum.GET.value
        url = UrlBuilder.get_url_for_key(key)
        headers = RedisUtils.__generate_default_headers()
        headers.__setitem__('X-RqUID', rq_uid)
        LOGGER.info('Url obtained: %s for get key: %s', url, key)
        response = RedisUtils.__make_http_call(url=url,
                                               method=method,
                                               headers=headers)
        response_status_code = response.status_code
        response_as_text = response.text
        LOGGER.info(RESPONSE_FORMATTER, response_status_code,
                    response_as_text)
        return response_as_text if response_status_code in (200, 201) else None

    @staticmethod
    def get_key_v1(key: str, rq_uid=str(uuid.uuid4())) -> str:
        r""" get a key saved in redis and return str if it was possible to get a key else return None.
            :param str key: name of the key to retrieve
            :return str with the value of the key or None
            :rtype None or str
            :usage: redis_response = RedisUtils.get_key('Key')"""
        method = HttpMethodEnum.GET.value
        url = UrlBuilderV1.get_url_for_get_key(key)
        headers = RedisUtils.__generate_default_headers()
        headers.__setitem__('X-RqUID', rq_uid)
        LOGGER.info('Url obtained: %s for get key: %s', url, key)
        response = RedisUtils.__make_http_call(url=url,
                                               method=method,
                                               headers=headers)
        response_status_code = response.status_code
        response_as_text = response.text
        LOGGER.info(RESPONSE_FORMATTER, response_status_code,
                    response_as_text)
        return response_as_text if response_status_code in (200, 201) else None

    @staticmethod
    def get_hash_key(key: str, hash_key: str, rq_uid=str(uuid.uuid4())) -> str:
        r""" get a key saved in redis and return str if it was possible get key
            :param str key: name of the key to retrieve
            :param str hash_key: name of the hash key to retrieve
            :param str or None rq_uid: unique request identifier
            :return str with the value of the key and hash key or None
            :rtype: None or str
            :usage: redis_response = RedisUtils.get_hash_key('Key', 'Hash_key')"""
        method = HttpMethodEnum.GET.value
        url = UrlBuilder.get_url_for_hash_key(key, hash_key)
        headers = RedisUtils.__generate_default_headers()
        headers.__setitem__('X-RqUID', rq_uid)
        LOGGER.info("Url obtained: %s for get hash key, key: %s hash key: %s", url, key, hash_key)
        response = RedisUtils.__make_http_call(url=url,
                                               method=method,
                                               rq_uid=rq_uid)
        response_status_code = response.status_code
        response_as_text = response.text
        LOGGER.info(RESPONSE_FORMATTER, response_status_code, response_as_text)
        return response_as_text if response_status_code in (200, 201) else None

    @staticmethod
    def get_hash_key_v1(key: str, hash_key: str, rq_uid=str(uuid.uuid4())) -> str:
        r""" get a key saved in redis and return str if it was possible get key
            :param str key: name of the key to retrieve
            :param str hash_key: name of the hash key to retrieve
            :param str or None rq_uid: unique request identifier
            :return str with the value of the key and hash key or None
            :rtype: None or str
            :usage: redis_response = RedisUtils.get_hash_key('Key', 'Hash_key')"""
        method = HttpMethodEnum.GET.value
        url = UrlBuilderV1.get_url_for_hash_key(key, hash_key)
        headers = RedisUtils.__generate_default_headers()
        headers.__setitem__('X-RqUID', rq_uid)
        LOGGER.info("Url obtained: %s for get hash key, key: %s hash key: %s", url, key, hash_key)
        response = RedisUtils.__make_http_call(url=url,
                                               method=method,
                                               rq_uid=rq_uid)
        response_status_code = response.status_code
        response_as_text = response.text
        LOGGER.info(RESPONSE_FORMATTER, response_status_code, response_as_text)
        return response_as_text if response_status_code in (200, 201) else None

    @staticmethod
    def set_hash_key(key: str, hash_key: str, value: object,
                     time: int or str, time_unit: str or TimeUnitEnum, rq_uid=str(uuid.uuid4())) -> bool:
        r""" save a hash key in redis and return a boolean if it was possible or not to save a key.
            :param str key: your redis key, must be str
            :param str hash_key: your hash key to save
            :param object value: your value to save
            :param int or str time: your time, must be int
            :param str or TimeUnitEnum time_unit: your unit time, must be str or TimeUnitEnum
            :param str or None rq_uid: unique request identifier
            :return: boolean that says if the save of the key is successful
            :rtype: bool
            usage:redis_response = RedisUtils.set_hash_key('key','hash_key','value', 15, 'MINUTES')"""
        method = HttpMethodEnum.POST.value
        parsed_time = RedisUtils.__handle_time(time)
        parsed_time_unit = RedisUtils.__handle_time_unit(time_unit)
        parsed_value = RedisUtils.__handle_value(value)
        url = UrlBuilder.get_url_for_hash_key(key, hash_key)
        LOGGER.info("Url obtained: %s for set hash key, key: %s hash key: %s and data: %s",
                    url, key, hash_key, value)
        headers = RedisUtils.__generate_default_headers()
        headers.__setitem__('X-Time', str(parsed_time))
        headers.__setitem__('X-TimeUnit', str(parsed_time_unit))
        headers.__setitem__('X-RqUID', rq_uid)
        response = RedisUtils.__make_http_call(url=url,
                                               method=method,
                                               value=parsed_value,
                                               headers=headers)
        response_status_code = response.status_code
        response_as_text = response.text
        LOGGER.info(RESPONSE_FORMATTER, response_status_code, response_as_text)
        return response_status_code in (200, 201)

    @staticmethod
    def set_hash_key_v1(key: str, hash_key: str, value: object,
                     time: int or str, time_unit: str or TimeUnitEnum, rq_uid=str(uuid.uuid4())) -> bool:
        r""" save a hash key in redis and return a boolean if it was possible or not to save a key.
            :param str key: your redis key, must be str
            :param str hash_key: your hash key to save
            :param object value: your value to save
            :param int or str time: your time, must be int
            :param str or TimeUnitEnum time_unit: your unit time, must be str or TimeUnitEnum
            :param str or None rq_uid: unique request identifier
            :return: boolean that says if the save of the key is successful
            :rtype: bool
            usage:redis_response = RedisUtils.set_hash_key('key','hash_key','value', 15, 'MINUTES')"""
        method = HttpMethodEnum.POST.value
        parsed_time = RedisUtils.__handle_time(time)
        parsed_time_unit = RedisUtils.__handle_time_unit(time_unit)
        parsed_value = RedisUtils.__handle_value(value)
        url = UrlBuilderV1.get_url_for_hash_key(key, hash_key)
        LOGGER.info("Url obtained: %s for set hash key, key: %s hash key: %s and data: %s",
                    url, key, hash_key, value)
        headers = RedisUtils.__generate_default_headers()
        headers.__setitem__('time', str(parsed_time))
        headers.__setitem__('time-unit', str(parsed_time_unit))
        headers.__setitem__('X-RqUID', rq_uid)
        response = RedisUtils.__make_http_call(url=url,
                                               method=method,
                                               value=parsed_value,
                                               headers=headers)
        response_status_code = response.status_code
        response_as_text = response.text
        LOGGER.info(RESPONSE_FORMATTER, response_status_code, response_as_text)
        return response_status_code in (200, 201)

    @staticmethod
    def set_complete_hash_key(key: str, value: object, time: int or str,
                              time_unit: str or TimeUnitEnum, rq_uid=str(uuid.uuid4())) -> bool:
        r""" save a complete hash key in redis and return a boolean if it was possible or not to save a key.
                :param str key: your redis key, must be str
                :param object or str value: your value to save, must be str or dict
                :param int or str time: your time, must be int
                :param str or TimeUnitEnum time_unit: your unit time, must be str or TimeUnitEnum
                :param str or None rq_uid: unique request identifier
                :return: boolean that says if the save of the key is successful
                :rtype: bool
                usage: redis_response = RedisUtils.set_key('key',object,15,TimeUnitEnum.MINUTES)"""
        method = HttpMethodEnum.POST.value
        parsed_time = RedisUtils.__handle_time(time)
        parsed_time_unit = RedisUtils.__handle_time_unit(time_unit)
        parsed_value = RedisUtils.__handle_value(value)
        url = UrlBuilder.get_url_for_all_hash_key(key)
        LOGGER.info("Url obtained: %s for set complete hash key, key: %s full hash data: %s",
                    url, key, value)
        headers = RedisUtils.__generate_default_headers()
        headers.__setitem__('X-Time', str(parsed_time))
        headers.__setitem__('X-TimeUnit', str(parsed_time_unit))
        headers.__setitem__('X-RqUID', rq_uid)
        response = RedisUtils.__make_http_call(url=url,
                                               method=method,
                                               value=parsed_value,
                                               headers=headers)
        response_status_code = response.status_code
        response_as_text = response.text
        LOGGER.info(RESPONSE_FORMATTER, response_status_code, response_as_text)
        return response_status_code in (200, 201)

    @staticmethod
    def delete_key(key: str, rq_uid=str(uuid.uuid4())) -> bool:
        r""" delete a key saved in redis and return true or false if it was possible to delete a key.
            :param str key: name of the key to retrieve
            :param str or None rq_uid: unique request identifier
            :return str with the value of the key or None
            :rtype None or str
            usage: redis_response = RedisUtils.delete_key('Key')"""
        method = HttpMethodEnum.DELETE.value
        url = UrlBuilder.get_url_for_key(key)
        headers = RedisUtils.__generate_default_headers()
        headers.__setitem__('X-RqUID', rq_uid)
        LOGGER.info("Url obtained: %s for delete key: %s", url, key)
        response = RedisUtils.__make_http_call(url=url,
                                               headers=headers,
                                               method=method)
        response_status_code = response.status_code
        response_as_text = response.text
        LOGGER.info(RESPONSE_FORMATTER, response_status_code,
                    response_as_text)
        return response_status_code in (200, 204)

    @staticmethod
    def delete_hash_key(key: str, hash_key: str, rq_uid=str(uuid.uuid4())) -> bool:
        r""" get a hash key saved in redis and return true if it was possible to delete a key else return None.
            :param str key: name of the key to retrieve
            :param str hash_key: name of the hash key to retrieve
            :param str or None rq_uid: unique request identifier
            :return str with the value of the key or None
            :rtype bool
            usage: redis_response = RedisUtils.delete_hash_key('Key','hash_key')"""
        method = HttpMethodEnum.DELETE.value
        url = UrlBuilder.get_url_for_hash_key(key, hash_key)
        headers = RedisUtils.__generate_default_headers()
        headers.__setitem__('X-RqUID', rq_uid)
        LOGGER.info("Url obtained: %s for delete hash key: %s and hash key: %s", url, key, hash_key)
        response = RedisUtils.__make_http_call(url=url,
                                               headers=headers,
                                               method=method)
        response_status_code = response.status_code
        response_as_text = response.text
        LOGGER.info(RESPONSE_FORMATTER, response_status_code,
                    response_as_text)
        return response_status_code in (200, 204)

    @staticmethod
    def __make_http_call(**kwargs) -> requests.api:
        """Make http call
            :keyword str method: Method to execute http call
            :keyword str url: Method url to execute http call
            :keyword str data: data to send to execute http call
            :return object with data of response
            :rtype: request.api
        """
        method = kwargs.get('method', None)
        url = kwargs.get('url', None)
        LOGGER.info("Making http call to url: %s", url)
        action = getattr(requests, method, None)
        value = kwargs.get('value', None)
        headers = kwargs.get('headers', RedisUtils.__generate_default_headers())
        LOGGER.info('Executing %s to %s with headers: %s, and body: %s',
                    method, url, headers, value)
        if value is not None:
            return action(url=url, headers=headers, data=value, timeout=int(config.DEFAULT_TIMEOUT))
        return action(url=url, headers=headers, timeout=int(config.DEFAULT_TIMEOUT))

    @staticmethod
    def __handle_time(time: int) -> int:
        """method to parse time
            :param int time: time to parse must be int but can be str
            :return parsed time int
            :rtype int
        """
        if isinstance(time, (int, float)):
            return time
        if isinstance(time, str):
            return int(float(time)) if '.' in time else int(time, 10)
        raise ValueError(f'Time must be a int you provided {time} and type {time.__class__.__name__}')

    @staticmethod
    def __handle_time_unit(time_unit) -> TimeUnitEnum:
        """method to parse time unit
        if time unit is none return minutes
            :param object time_unit: time unit to parse must be TimeUnitEnum or str
            :return parsed time unit
            :rtype TimeUnitEnum
        """
        if isinstance(time_unit, TimeUnitEnum):
            return time_unit.value
        if isinstance(time_unit, str) and TimeUnitEnum.has_value(time_unit):
            return TimeUnitEnum[time_unit.upper()].value
        raise ValueError(f'{time_unit} is not a valid time unit with type: {time_unit.__class__.__name__}')

    @staticmethod
    def __generate_default_headers() -> dict:
        """method to set default headers
        :return dict with default headers
        :rtype dict
        """
        default_headers = dict()
        default_headers.__setitem__('Content-Type', APPLICATION_JSON)
        default_headers.__setitem__('X-Name', config.APPLICATION_NAME)
        default_headers.__setitem__('x-api-key', config.API_KEY)
        return default_headers

    @staticmethod
    def __handle_value(value) -> str:
        """method to parse time
        :param object value: value to send as object
        :return parsed value as str
        :rtype str
        """
        posibles_types = (str, dict, int, list, float, tuple, bool)
        if isinstance(value, posibles_types):
            return json.dumps(value)
        if not isinstance(value, dict):
            return json.dumps(value.__dict__)
        raise TypeError(f'Object of type {value.__class__.__name__} is not JSON serializable')
