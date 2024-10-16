from __future__ import annotations

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from losb.api.v1.serializers import UserSerializer
from losb.models import User


@extend_schema_view(
    get=extend_schema(
        responses={
            200: UserSerializer,
        },
        summary='Профиль пользователя',
        description='Возвращает профиль пользователя',
    ),
)
class UserRetrieveVew(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        obj = User.objects.get(telegram_id=self.request.user.telegram_id)
        return obj