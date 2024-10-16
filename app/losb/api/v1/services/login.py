from __future__ import annotations

from allauth.account.auth_backends import AuthenticationBackend
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from losb.api.v1.services.tokens import FilledRefreshToken
from losb.api.v1.services.transfers import AuthToken, ExpectedCredentials

User = get_user_model()


def authenticate_and_obtain_token(
    request: Request,
    **credentials: ExpectedCredentials,
):
    """
    Авторизация пользователя на платформе
    """
    backend = AuthenticationBackend()
    user = backend.authenticate(request, **credentials)
    if not user:
        raise AuthenticationFailed

    refresh_token = FilledRefreshToken.for_user(user)
    return AuthToken(str(refresh_token.access_token), str(refresh_token))
