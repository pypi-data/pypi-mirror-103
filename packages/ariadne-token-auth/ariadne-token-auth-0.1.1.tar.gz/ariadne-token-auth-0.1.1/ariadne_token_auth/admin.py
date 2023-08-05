from django.contrib import admin

from . import models


@admin.register(models.AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    readonly_fields = ("token_string",)
