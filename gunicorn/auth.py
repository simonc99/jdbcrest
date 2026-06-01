from functools import wraps
from flask import request
from flask import Response

from config import (
    API_USERNAME,
    API_PASSWORD
)

def authenticate():

    auth = request.authorization

    if not auth:
        return False

    return (
        auth.username == API_USERNAME
        and auth.password == API_PASSWORD
    )

def requires_auth(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        if not authenticate():

            return Response(
                "Authentication required",
                401,
                {
                    "WWW-Authenticate":
                    'Basic realm="Login Required"'
                }
            )

        return f(*args, **kwargs)

    return decorated
