from unittest import mock
import uuid
from bbog_sg_python_redis_lib import TimeUnitEnum
from test.mocks import requests_mocks
from bbog_sg_python_redis_lib.redis_utils import RedisUtils


class TestRedisUtils():

    @mock.patch('requests.get', side_effect=requests_mocks.mocked_requests_get_success)
    def test_get_key_success(self, mock_get):
        with mock_get:
            response = RedisUtils.get_key('key')
        assert response == requests_mocks.mocked_requests_get_success().text

    @mock.patch('requests.get', side_effect=requests_mocks.mocked_requests_get_success)
    def test_get_key_success_v1(self, mock_get):
        with mock_get:
            response = RedisUtils.get_key_v1('key')
        assert response == requests_mocks.mocked_requests_get_success().text

    @mock.patch('requests.get', side_effect=requests_mocks.mocked_requests_get_success)
    def test_get_hash_key_success(self, mock_get):
        with mock_get:
            response = RedisUtils.get_hash_key('key', 'hash_key')
        assert response == requests_mocks.mocked_requests_get_success().text

    @mock.patch('requests.get', side_effect=requests_mocks.mocked_requests_get_success)
    def test_get_hash_key_success_v1(self, mock_get):
        with mock_get:
            response = RedisUtils.get_hash_key_v1('key', 'hash_key')
        assert response == requests_mocks.mocked_requests_get_success().text

    @mock.patch('requests.post', side_effect=requests_mocks.mocked_requests_post_success_200)
    def test_set_key_success(self, mock_post):
        with mock_post:
            response = RedisUtils.set_key('key', 'value', 15, TimeUnitEnum.MINUTES, str(uuid.uuid4()))
        assert response is True

    @mock.patch('requests.post', side_effect=requests_mocks.mocked_requests_post_success_200)
    def test_set_key_success_v1(self, mock_post):
        with mock_post:
            response = RedisUtils.set_key_v1('key', 'value', 15, TimeUnitEnum.MINUTES, str(uuid.uuid4()))
        assert response is True

    @mock.patch('requests.post', side_effect=requests_mocks.mocked_requests_post_success_200)
    def test_set_key_success_with_str_and_float(self, mock_post):
        with mock_post:
            response = RedisUtils.set_key('key', 'value', '15.2', TimeUnitEnum.MINUTES)
        assert response is True

    @mock.patch('requests.post', side_effect=requests_mocks.mocked_requests_post_success_200)
    def test_set_key_success_with_bad_value(self, mock_post):
        with mock_post:
            try:
                RedisUtils.set_key('key', 'Value', {}, TimeUnitEnum.MINUTES)
            except ValueError as exception:
                print(str(exception))
                assert str(exception) == "Time must be a int you provided {} and type dict"

    @mock.patch('requests.post', side_effect=requests_mocks.mocked_requests_post_success_201)
    def test_set_hash_key_success(self, mock_post):
        class ValueTest:
            def __init__(self):
                self.hola = 'hola'
                self.mundo = 'mundo'

        with mock_post:
            response = RedisUtils.set_hash_key('key', 'hash', ValueTest(), 15, 'HOURS')
        assert response is True

    @mock.patch('requests.post', side_effect=requests_mocks.mocked_requests_post_success_201)
    def test_set_hash_key_success_v1(self, mock_post):
        class ValueTest:
            def __init__(self):
                self.hola = 'hola'
                self.mundo = 'mundo'

        with mock_post:
            response = RedisUtils.set_hash_key_v1('key', 'hash', ValueTest(), 15, 'HOURS')
        assert response is True

    @mock.patch('requests.post', side_effect=requests_mocks.mocked_requests_post_success_201)
    def test_set_complete_hash_key_success(self, mock_post):
        class ValueTest:
            def __init__(self):
                self.hola = 'hola'
                self.mundo = 'mundo'

        with mock_post:
            response = RedisUtils.set_complete_hash_key('key', ValueTest(), '15', TimeUnitEnum.MINUTES)
        assert response is True

    @mock.patch('requests.post', side_effect=requests_mocks.mocked_requests_post_success_201)
    def test_set_complete_hash_key_fail(self, mock_post):
        class ValueTest:
            def __init__(self):
                self.hola = 'hola'
                self.mundo = 'mundo'

        with mock_post:
            try:
                response = RedisUtils.set_complete_hash_key('key', ValueTest(), '15', 'holiwis')
            except ValueError as e:
                assert str(e) == 'holiwis is not a valid time unit with type: str'

    @mock.patch('requests.delete', side_effect=requests_mocks.mocked_requests_delete_success_200)
    def test_delete_key_success(self, mock_delete):
        with mock_delete:
            response = RedisUtils.delete_key('key')
        assert response is True

    @mock.patch('requests.delete', side_effect=requests_mocks.mocked_requests_delete_success_204)
    def test_delete_hash_key_not_exists_success(self, mock_delete):
        with mock_delete:
            response = RedisUtils.delete_hash_key('key', 'hash_key')
        assert response is True
