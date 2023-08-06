"""Http method enum"""
from enum import Enum


class HttpMethodEnum(Enum):
    """enum to handle time unit"""
    POST = 'post'
    GET = 'get'
    OPTIONS = 'options'
    DELETE = 'delete'
    PUT = 'put'
    PATCH = 'patch'
