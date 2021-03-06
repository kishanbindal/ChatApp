import jwt
import logging

logging.basicConfig(level=logging.DEBUG)


class Generatetoken:

    secret_key = 'secret_key'

    def registration_token(self, username, email):
        payload = {
            "username": username,
            "email": email
        }
        return self._encode(payload)

    def login_token(self, user_id):
        payload = {
            "id": user_id
        }
        return self._encode(payload)

    def _encode(self, payload):
        token = jwt.encode(payload, self.secret_key, algorithm='HS256').decode('utf-8')
        # token = "".join(chr(x) for x in bytearray(token))
        return token

    def decode_token(self,  token):
        logging.info(f'Token for decoding : {token}')
        return jwt.decode(token, self.secret_key, algorithms='HS256')
