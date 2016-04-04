"""Authorization handlers"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import json
from urllib.parse import quote

from tornado import web
from .. import orm
from ..utils import token_authenticated
from .base import APIHandler

import jwt


class TokenAPIHandler(APIHandler):
    @token_authenticated
    def get(self, token):
        orm_token = orm.APIToken.find(self.db, token)
        if orm_token is None:
            raise web.HTTPError(404)
        self.write(json.dumps(self.user_model(self.users[orm_token.user])))


class CookieAPIHandler(APIHandler):
    @token_authenticated
    def get(self, cookie_name, cookie_value=None):
        cookie_name = quote(cookie_name, safe='')
        if cookie_value is None:
            self.log.warn("Cookie values in request body is deprecated, use `/cookie_name/cookie_value`")
            cookie_value = self.request.body
        else:
            cookie_value = cookie_value.encode('utf8')
        user = self._user_for_cookie(cookie_name, cookie_value)
        if user is None:
            raise web.HTTPError(404)
        self.write(json.dumps(self.user_model(user)))


class JWTAPIHandler(APIHandler):
    SECRET = 'my secret'
    @token_authenticated
    def get(self):
        header = self.request.headers.get('Authorization', '')
        header = header.strip()
        if header:
            split_header = header.split(' ')
            if len(split_header) == 2 and split_header[0] == 'Bearer' and split_header[1]:
                try:
                    decoded_token = jwt.decode(split_header[1], self.SECRET, options={'verify_iat': False})
                    user = self._user_from_orm(decoded_token['sub'])
                    if user is None:
                        raise web.HTTPError(404)
                    else:
                        self.write(json.dumps(self.user_model(user)))
                except Exception:
                    raise web.HTTPError(401)


default_handlers = [
    (r"/api/authorizations/cookie/([^/]+)(?:/([^/]+))?", CookieAPIHandler),
    (r"/api/authorizations/token/([^/]+)", TokenAPIHandler),
    (r"/api/authorizations/jwt/([^/]+)", TokenAPIHandler)
]
