import base64

from jwt import decode
from rest_framework_simplejwt.tokens import RefreshToken
from functools import wraps
from book_store.settings import SECRET_KEY


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'access token': str(refresh.access_token)}


def token_required(f):
    @wraps(f)
    def token_decode(request, *args, **kwargs):
        # short_token = request.headers.get('Token')
        print(request.META)
        _, short_token = request.META.get('HTTP_AUTHORIZATION').split(' ')
        if not short_token:
            short_token = request.query_params.get('token')
        if not short_token:
            return {'Error': 'Token is missing!', 'Status Code': 400}

        count = short_token.find('.')
        if count == -1:
            token = raw_token(short_token)
        else:
            token = short_token
        data = decode(token, SECRET_KEY, 'HS256')
        user_id = data['user_id']
        return f(request, user_id, *args, **kwargs)

    return token_decode


def modified_token(token):
    token_string_bytes = token.encode("ascii")
    base64_bytes = base64.b64encode(token_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


def raw_token(token_):
    base64_bytes = token_.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string
