"""HTTP Handlers for the hub server"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from tornado.escape import url_escape
from tornado import gen

from .base import BaseHandler


class LogoutHandler(BaseHandler):
    """Log a user out by clearing their login cookie."""
    def get(self):
        user = self.get_current_user()
        self.clear_login_cookie()
        if user:
            self.log.info("User logged out: %s", user.name)
            for name in user.other_user_cookies:
                self.clear_login_cookie(name)
            user.other_user_cookies = set([])
        self.redirect(self.hub.server.base_url, permanent=False)


class LoginHandler(BaseHandler):
    """Render the login page."""

    def _render(self, login_error=None, username=None):
        return self.render_template('login.html',
                next=url_escape(self.get_argument('next', default='')),
                username=username,
                login_error=login_error,
                custom_html=self.authenticator.custom_html,
                login_url=self.settings['login_url']
        )

    def get(self):
        next_url = self.get_argument('next', '')
        if not next_url.startswith('/'):
            # disallow non-absolute next URLs (e.g. full URLs)
            next_url = ''
        user = self.get_current_user()
        if user:
            if not next_url:
                if user.running:
                    next_url = user.url
                else:
                    next_url = self.hub.server.base_url
            # set new login cookie
            # because single-user cookie may have been cleared or incorrect
            self.set_login_cookie(self.get_current_user())
            self.redirect(next_url, permanent=False)
        else:
            username = self.get_argument('username', default='')
            self.finish(self._render(username=username))

    @gen.coroutine
    def post(self):
        # parse the arguments dict
        data = {}
        for arg in self.request.arguments:
            data[arg] = self.get_argument(arg)
        self.log.info('I am getting a post, proceeding to verify user... ')
        #self.log.info('I am currently receiving this: %s %s', data['username'], data['password'])
        username = yield self.authenticate(data)
        self.log.info('After auth, i got: ' + str(username) if username else 0)
        if username:
            user = self.user_from_username(username)
            already_running = False
            if user.spawner:
                status = yield user.spawner.poll()
                already_running = (status == None)
            if not already_running and not user.spawner.options_form:
                yield self.spawn_single_user(user)
            self.set_login_cookie(user)
            next_url = self.get_argument('next', default='')
            if not next_url.startswith('/'):
                next_url = ''
            next_url = next_url or self.hub.server.base_url
            self.redirect(next_url)
            self.log.info("User logged in: %s", username)
        else:
            self.log.debug("Failed login for %s", data.get('username', 'unknown user'))
            html = self._render(
                login_error='Invalid token for user',
                username=username,
            )
            self.finish(html)


class JWTLoginHandler(LoginHandler):

    def _render(self, login_error=None, username=None):
        return self.render_template('login.html',
                                    next=url_escape(self.get_argument('next', default='')),
                                    username=username,
                                    login_error=login_error,
                                    custom_html=self.authenticator.custom_html,
                                    login_url=self.settings['login_url'])

    @gen.coroutine
    def get(self):
        next_url = self.get_argument('next', '')
        if not next_url.startswith('/'):
            # disallow non-absolute next URLs (e.g. full URLs)
            next_url = ''
        user = self.get_current_user()
        print('Current user is: ' + (str(user) if user is not None else 'None'))
        if user:
            if not next_url:
                if user.running:
                    next_url = user.url
                else:
                    next_url = self.hub.server.base_url
            # set new login cookie
            # because single-user cookie may have been cleared or incorrect
            self.log.info('Passing to the next route, user is already authed... ')
            self.set_login_cookie(self.get_current_user())
            self.redirect(next_url, permanent=False)
        else:
            auth_header = self.request.headers.get('Authorization', '')
            split_token = auth_header.split(' ')

            if len(split_token) == 2 and split_token[0] == 'Bearer' and \
                    (split_token[1] is not '' or split_token[1] is not ' ') :
                token = split_token[1]
                self.log.info('Current bearer: ' + token)
                res = yield self._authenticate_with_jwt(token)
                if res['html']:
                    self.finish(res['html'])
                else:
                    self.redirect(res['next_url'])
            else:
                html = self._render(
                    login_error='Invalid token for user'
                )
                self.finish(html)

    @gen.coroutine
    def _authenticate_with_jwt(self, token):
        if token:
            username = yield self.authenticate(token)
            if username:
                self.log.info('User has just authenticated!')
                user = self.user_from_username(username)
                if user is not None:
                    user = self.update_users_token(username, token)
                already_running = False
                if user.spawner:
                    status = yield user.spawner.poll()
                    already_running = (status == None)
                if not already_running and not user.spawner.options_form:
                    yield self.spawn_single_user(user)
                self.set_login_cookie(user)
                next_url = self.get_argument('next', default='')
                if not next_url.startswith('/'):
                    next_url = ''
                next_url = next_url or self.hub.server.base_url
                self.log.info("User logged in: %s", username)
                print("NEXT URL: " + next_url)
                raise gen.Return({'html': '', 'next_url': next_url})
            else:
                self.log.warn("Failed login for token %s", token)
                html = self._render(
                    login_error='Invalid token for user',
                    username=username,
                )
                raise gen.Return({'html': html})
        else:
            self.log.warn('Token not provided by user!')
            html = self._render(login_error='You need to have a valid token!')
            raise gen.Return({'html': html})

    def update_users_token(self, username, token):
        self.log.info('Updating the user\'s JWT token')
        user = self.user_from_username(username)
        user.kerberos_token = token
        self.db.commit()
        return self.user_from_username(username)


# /login renders the login page or the "Login with..." link,
# so it should always be registered.
# /logout clears cookies.
default_handlers = [
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
]
