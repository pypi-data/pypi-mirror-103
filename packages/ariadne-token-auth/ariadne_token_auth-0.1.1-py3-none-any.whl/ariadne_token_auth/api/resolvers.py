from ariadne_token_auth import models
from django.contrib.auth import authenticate, get_user_model

type_defs = """
    type AuthToken {
        token: String
    }
    type AuthTokenPayload {
        auth: AuthToken
        error: String
    }
    type DeleteTokenPayload {
        status: Boolean
        error: String
    }
"""

UserModel = get_user_model()


def get_auth_token(self, info, password, *args, **kwargs):
    username_field = kwargs.get("identifier")
    user = authenticate(
        info.context.get("request"), username=username_field, password=password
    )
    if user is None:
        return {"auth": None, "error": "The credentials you provided were invalid"}
    try:
        token_obj = models.AuthToken.objects.get(user=user)
    except models.AuthToken.DoesNotExist:
        token_obj = models.AuthToken.objects.create(user=user)
    return {"auth": {"token": token_obj.token_string}}


def delete_auth_token(self, info, token, *args, **kwargs):
    status = False
    error = None
    try:
        models.AuthToken.objects.get(token_string=token).delete()
        status = True
    except models.AuthToken.DoesNotExist:
        error = "The token you provided was invalid"
    return {"status": status, "error": error}
