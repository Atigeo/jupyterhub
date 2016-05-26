from jupyterhub.auth import Authenticator
from traitlets import (Unicode)

import jwt, requests, json
from tornado import gen


class JWTHeaderAuthenticator(Authenticator):
    """
    Authenticates the user based on an audience, a secret key and a JWT token from a header in the form
    'Authorization: Bearer <token_here>'
    """
    secret_key = Unicode('my secret',
                         config=True)

    token_service_url = Unicode('',
                                config=True)

    #audience = Unicode('#/connect', config=True)
    audience = ''

    def __init__(self, **kwargs):
        Authenticator.__init__(self, **kwargs)
        self.custom_html = '<br> <div style="text-align: center; background: black;"> <img src="http://atigeo.com/assets/imgs/xpatterns-logo.svg"> </div>'

    @gen.coroutine
    def authenticate(self, handler, token):
        """ Authenticate with the JWT token that i've received

        Return None in case of
        """
        try:
            self.log.info("I got the following data: " + str(token))
            print('Secret: ' + str(self.secret_key))
            if self.audience:
                decoded_token = jwt.decode(token, self.secret_key, options={'verify_iat': False}, audience=self.audience)
            else:
                decoded_token = jwt.decode(token, self.secret_key, options={'verify_iat': False, 'verify_aud': False})

            if self.token_service_url:
                try:
                    r = requests.post(self.token_service_url, headers={'Content-Type': 'application/json'},
                                  data=json.dumps({'token': token}))
                    if not r.ok:
                        self.log.error(str(r.content))
                    else:
                        self.log.info('Updated token service for user: ' + str(decoded_token['sub']))
                except Exception as e:
                    self.log.error('Error refreshing token in service ' + str(e))

            return decoded_token['sub']
        except Exception as e:
            self.log.error("Error parsing jwt token: " + str(e))
            return