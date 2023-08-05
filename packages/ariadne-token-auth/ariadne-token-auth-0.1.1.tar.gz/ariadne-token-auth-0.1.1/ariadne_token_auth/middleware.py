from django import http
from django.contrib import auth
from django.core import exceptions

from . import utils


class AuthTokenMiddleware:
    """
    Middleware that authenticates against a token in the HTTP authorization header.
    """

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        if not self.get_response:
            return exceptions.ImproperlyConfigured(
                "Middleware called without proper initialization"
            )
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        auth_header = request.headers.get("AUTHORIZATION", "").split()
        if not auth_header:
            return None
        if auth_header[0].lower() != utils.TOKEN_NAME.lower():
            return None

        # If they specified an invalid token, let them know.
        if not auth_header[1]:
            return http.HttpResponseBadRequest("Improperly formatted token")

        user = auth.authenticate(token_string=auth_header[1])
        if user:
            request.user = user
