from __future__ import annotations

from rest_framework_simplejwt.tokens import RefreshToken


class FilledRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user) -> RefreshToken:
        token: RefreshToken = super().for_user(user)
        token['telegram_id'] = user.telegram_id
        return token
