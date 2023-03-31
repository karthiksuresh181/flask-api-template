import uuid
from flask import Flask, request, make_response
from flask_cors import CORS
from flask_session import Session
from flask_caching import Cache
from werkzeug.middleware.proxy_fix import ProxyFix
from json import load
from os import environ, path, makedirs, listdir, remove, stat
from datetime import datetime
import time

from .blueprints import blueprint as deadpool_api_blueprint
from .utils.JsonUtils import read_json, write_json
from .utils.Utils import AppUtils


def _with_config(app: Flask):
    app.config.from_file("config.json", load=load)
    DEFAULT_ENV_VALUE = ""
    client_id = environ.get('CLIENT_ID', DEFAULT_ENV_VALUE)
    tenant_id = environ.get('TENANT_ID', DEFAULT_ENV_VALUE)
    if client_id != DEFAULT_ENV_VALUE and client_id != app.config.get("CLIENT_ID"):
        app.config.update(CLIENT_ID=client_id.strip())
    if tenant_id != DEFAULT_ENV_VALUE and tenant_id != app.config.get("TENANT_ID"):
        app.config.update(CLIENT_ID=tenant_id.strip())


def read_cache_file(cache_file_path):
    if not path.exists(cache_file_path):
        write_json(cache_file_path, {})
    return read_json(cache_file_path)


def write_cache_file(cache_file_path, user_sessions):
    write_json(cache_file_path, user_sessions)


def remove_expired_cache_files():
    SESSION_FOLER = AppUtils().get_session_folder()
    current_time = time.time()
    for filename in listdir(SESSION_FOLER):
        file_path = path.join(SESSION_FOLER, filename)
        if stat(file_path).st_mtime < current_time - app.permanent_session_lifetime.total_seconds():
            remove(file_path)


def handle_cookie(oid, cookie, cache_file_path):
    if cookie:
        user_sessions = read_cache_file(cache_file_path)
        if oid in user_sessions:
            user_cookies = user_sessions[oid].get('cookies', [])
            if user_cookies:
                for user_cookie in user_cookies:
                    if user_cookie["id"] == cookie:
                        user_cookie.update(
                            {'id': cookie, 'created_at': datetime.utcnow().isoformat()})
                        break
            else:
                user_cookies.append(
                    {'id': cookie, 'created_at': datetime.utcnow().isoformat()})

            user_cookies = [user_cookie for user_cookie in user_cookies if datetime.utcnow(
            ) - datetime.fromisoformat(user_cookie['created_at'] < app.permanent_session_lifetime)]
            if not user_cookies:
                print('All cookies expired')
            else:
                user_sessions[oid]['cookies'] = user_cookies
        else:
            user_cookies.append(
                {'id': cookie, 'created_at': datetime.utcnow().isoformat()})
            user_sessions[oid]['cookies'] = user_cookies
    else:
        user_sessions[oid] = {'cookies': [
            {'id': cookie, 'created_at': datetime.utcnow().isoformat()}]}
    write_cache_file(cache_file_path, user_sessions)


def init_app():

    app = Flask(__name__)
    _with_config(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.secret_key = uuid.uuid4().hex
    Session(app)
    CORS(app, origins='*', supports_credentials=True)
    config = {
        "DEBUG": app.config.get("CLEAR_DEBUG", False),
        "CACHE_TYPE": app.config.get("CACHE_TYPE", "FileSystemCache"),
        "CACHE_DEFAULT_TIMEOUT": app.config.get("CACHE_DEFAULT_TIMEOUT", 30),
        "CACHE_THRESHOLD": app.config.get("CACHE_THRESHOLD", 100),
        "CACHE_IGNORE_ERRORS": app.config.get("CACHE_IGNORE_ERRORS", True),
        "CACHE_DIR": app.config.get("CACHE_DIR")
    }
    app.cache = Cache(config=config, app=app)
    app.register_blueprint(deadpool_api_blueprint, url_prefix='/api/v1')

    @app.before_request
    def before_req():
        pass

    @app.after_request
    def after_request(response):
        if request.method == "OPTIONS":
            response.status_code = 200
        return response
    return app


app = init_app()
