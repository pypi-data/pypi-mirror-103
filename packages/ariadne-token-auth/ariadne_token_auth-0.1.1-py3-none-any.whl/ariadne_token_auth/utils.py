from django.conf import settings


def get_settings_or_default(setting_name):
    ariadne_token_auth_settings = getattr(
        settings,
        "ARIADNE_TOKEN_AUTH",
        # The default settings start here
        {"TOKEN_NAME": "Token", "TOKEN_LENGTH": 35}
        # The default settings end here
    )
    return ariadne_token_auth_settings.get(setting_name)


TOKEN_NAME = get_settings_or_default("TOKEN_NAME")
TOKEN_LENGTH = get_settings_or_default("TOKEN_LENGTH")
