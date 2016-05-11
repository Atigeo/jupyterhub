from jupyterhub.auth import Authenticator
from traitlets import (Unicode)

import jwt
from tornado import gen


class JWTHeaderAuthenticator(Authenticator):
    """
    Authenticates the user based on an audience, a secret key and a JWT token from a header in the form
    'Authorization: Bearer <token_here>'
    """
    secret_key = Unicode('my secret',
                         config=True)

    #audience = Unicode('#/connect', config=True)
    audience = Unicode('', config=True)

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
                decoded_token = jwt.decode(token, self.secret_key, options={'verify_iat': False})

            return decoded_token['sub']
        except Exception as e:
            self.log.error("Error parsing jwt token: " + str(e))
            return