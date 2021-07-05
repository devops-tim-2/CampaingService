# from exception.exceptions import InvalidAuthException
import time
from os import environ
from datetime import datetime
import jwt


def check(obj: dict) -> bool:
    return not obj or any(value is None or ((type(value) is list or (type(value) is str and key != 'description')) and len(value) == 0) or ((type(value) is int or type(value) is float) and value < 1) for key, value in obj.items())


# def auth(token: str):
#     try:
#         payload = jwt.decode(token, environ.get('JWT_SECRET'), environ.get('JWT_ALGORITHM'))
#     except Exception:
#         raise InvalidAuthException('Forbidden, invalid authentication.')

#     exp = payload['exp']
#     if datetime.now() > datetime.fromtimestamp(exp / 1000.0):
#         raise InvalidAuthException('Forbidden, authorization token has expired.')

#     return payload


# def generate_token(user: dict):
#     user["iat"] = round(time.time() * 1000)
#     user["exp"] = round(time.time() * 1000) + 3600000 * 24 * 365 #1 year from now
#     encoded_jwt = jwt.encode(user, environ.get('JWT_SECRET'), algorithm=environ.get('JWT_ALGORITHM'))
#     return encoded_jwt
