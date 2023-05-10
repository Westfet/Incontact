# Create your views here.
from typing import Any

from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins, serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from profiles.models import UserRelations
from profiles.pagination import CommonPagination
from profiles.serializers import (
    FriendAcceptDeclineSerializer,
    FriendSerializer,
    FriendsListSerializer,
    FriendSubscribeSerializer,
)
from profiles.models import UserNet
from profiles.time import now_tz


@extend_schema(tags=["friends"])
class RetrieveMyFriendsView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset для методов получения списка профилей и конкретного профиля по id."""

    queryset = UserRelations.objects.all()
    serializer_class = FriendsListSerializer

    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination

    def get_queryset(self) -> Any:
        return UserRelations.objects.get_relations_full(self.request.user.id)


@extend_schema(tags=["friends"])
class RetrieveFriendsByUserIdView(
    generics.ListAPIView
):
    """Viewset для методов получения списка профилей и конкретного профиля по id."""

    queryset = UserNet.objects.all()
    serializer_class = FriendSerializer

    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination

    def get_queryset(self) -> Any:
        related_users = UserRelations.objects.get_relations_full(self.kwargs["pk"])
        return super().get_queryset().filter(id__in=related_users)

@extend_schema(tags=["friends"])
class SubscribeToUserView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
    ):
    """Viewset для методов получения списка профилей и конкретного профиля по id."""

    serializer_class = None
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination
    def create(self, request, args, **kwargs) -> Response:
        serializer = FriendSubscribeSerializer(
        data={"first_user": self.request.user.id, "second_user": self.kwargs.get("pk")})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data=None, status=status.HTTP_201_CREATED, headers=headers)

@extend_schema(tags=["friends"])
class AcceptUserView(
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet,
    ):
    """Viewset для методов получения списка профилей и конкретного профиля по id."""

    serializer_class = None

    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination
    def update(self, request, args, **kwargs) -> Response:
        try:
            instance = UserRelations.objects.get(
                first_user=self.kwargs.get("pk"), second_user=self.request.user.id)
            if instance.accepted_at:
                raise serializers.ValidationError({"error": "Request already accepted."})
        except UserRelations.DoesNotExist:
            raise serializers.ValidationError(
            {"error": "Relation does not exist or you cant accept this request."})
            serializer = FriendAcceptDeclineSerializer(
                instance=instance,
                data={"viewed_at": now_tz(), "accepted_at": now_tz(),
                    "first_user": self.kwargs.get(
                    "pk"), "second_user": self.request.user.id},
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(data=None, status=status.HTTP_200_OK)


@extend_schema(tags=["friends"])
class DeclineUserView(
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet,
        ):
    """Viewset для методов получения списка профилей и конкретного профиля по id."""
                # TODO: исключить администраторов и модераторов из выдачи
    serializer_class = None
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination
    def update(self, request, *args, **kwargs) -> Response:
        try:
            instance = UserRelations.objects.get(
            first_user=self.kwargs.get("pk"), second_user=self.request.user.id)
            if not instance.accepted_at and instance.viewed_at:
                raise serializers.ValidationError(
                    {"error": "Request already declined."})
        except UserRelations.DoesNotExist:
            raise serializers.ValidationError(
                    {"error": "Relation does not exist or you cant decline this request."})
            serializer = FriendAcceptDeclineSerializer(
            instance=instance,
            data={
                "viewed_at": now_tz(),
                "accepted_at": None,
                "first_user": self.kwargs.get("pk"),
                "second_user": self.request.user.id},
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(data=None, status=status.HTTP_200_OK)

@extend_schema(tags=["friends"])
class DeleteRelationView( mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Viewset для методов получения списка профилей и конкретного профиля по id."""

    serializer_class = None

    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination

    def destroy(self, request, *args, **kwargs) -> Response:
        try:
            instance = UserRelations.objects.get(
                Q(first_user=self.kwargs.get("pk"),
                second_user=self.request.user.id) |
                Q(first_user=self.request.user.id,
                second_user=self.kwargs.get("pk"))
            )
        except UserRelations.DoesNotExist:
            raise serializers.ValidationError({"error": "Relation does not exist."})
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
