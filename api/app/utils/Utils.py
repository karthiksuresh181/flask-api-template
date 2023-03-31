from functools import wraps as function_wraps
from .JsonUtils import read_json, write_json
from os.path import join
from flask import current_app, _request_ctx_stack
from os import environ


def singleton(cls):
    """
    - Decorate your class with this decorator
    - If you happen to create another instance of the same class, it will return the previously created one
    - Supports creation of multiple instances of same class with different args/Kwargs
    - Works for multiple classes
    Use: 
        >>> from Utils import singleton
        >>>
        >>> @singleton
        ... class A:
        ...     def __init__(self, *args, **kwargs):
        ...         pass
        ...
        >>>
        >>> a = A(name='MY_NAME')
        >>> b = A(name='MY_NAME', lname='MY_NAME')
        >>> c = A(name='MY_NAME', lname='MY_NAME')
        >>> a is b  # has to be different
        False
        >>> b is c  # has to be same
        True
        >>>
    """
    previous_instances = {}

    @function_wraps(cls)
    def wrapper(*args, **kwargs):
        if cls in previous_instances and previous_instances.get(cls, None).get('args') == (args, kwargs):
            return previous_instances[cls].get('instance')
        else:
            previous_instances[cls] = {
                'args': (args, kwargs),
                'instance': cls(*args, **kwargs)
            }
            return previous_instances[cls].get('instance')
    return wrapper


@singleton
class AppUtils():
    def __get_app_config(self):
        with current_app.app.app_context():
            return current_app.config

    def get_temp_path(self):
        return f"{self.__get_app_config()['TEMP_PATH']}/{_request_ctx_stack.top.current_user['oid']}"

    def get_oid(self):
        return _request_ctx_stack.top.current_user['oid']

    def get_app_path(self):
        return current_app.root_path

    def get_cachefile_name(self):
        return self.__get_app_config()['CACHEFILE_NAME']

    def get_cache_folder(self):
        return self.__get_app_config()['CACHE_FOLDER']

    def get_session_folder(self):
        return self.__get_app_config()['SESSION_FILE_DIR']
