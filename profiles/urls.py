from django.urls import path

from profiles.views import (
    AcceptUserView,
    DeclineUserView,
    DeleteRelationView,
    RetrieveFriendsByUserIdView,
    RetrieveMyFriendsView,
    SubscribeToUserView,
)


# from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token  # type: ignore


app_name = "profiles"


urlpatterns = [
    path(
        "friends/me/friends/",
        RetrieveMyFriendsView.as_view({"get": "list"}),
        name="my-friends",
    ),
    path("friends/<str:pk>/", RetrieveFriendsByUserIdView.as_view(), name="user-friends"),
    path("friends/<str:pk>/subscribe/", SubscribeToUserView.as_view({"post": "create"}), name="friend-subscribe"),
    path("friends/<str:pk>/accept/", AcceptUserView.as_view({"post": "update"}), name="friend-accept"),
    path("friends/<str:pk>/decline/", DeclineUserView.as_view({"post": "update"}), name="friend-decline"),
    path("friends/<str:pk>/delete/", DeleteRelationView.as_view({"post": "destroy"}), name="friend-delete"),

]