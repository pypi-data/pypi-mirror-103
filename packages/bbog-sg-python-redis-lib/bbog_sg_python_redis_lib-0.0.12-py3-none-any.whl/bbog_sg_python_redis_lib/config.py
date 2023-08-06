"""default config for redis api"""
import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'QA')
VPCE_ID = os.getenv('VPCE_ID', None)
API_KEY = os.getenv('REDIS_API_KEY', None)
OLD_ACCOUNT = os.getenv('OLD_ACCOUNT', 'true')
REDIS_API_URL = os.getenv('REDIS_API_URL', 'https://api-redis.labdigbdbdevredis.com')
REDIS_API_PATH = os.getenv('REDIS_API_PATH', 'V2/Utilities/redis-cache')
APPLICATION_NAME = os.getenv('APPLICATION_NAME', 'Vehiculos')
DEFAULT_TIMEOUT = os.getenv('DEFAULT_TIMEOUT', '5')