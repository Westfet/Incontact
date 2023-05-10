# from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from profiles.models import UserRelations
from profiles.models import UserNet


# TODO: исключить из выдачи password
class FriendSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя для вывода всех полей."""

    class Meta:
        fields = ["id", "email", "avatar", "first_name", "last_name"]
        model = UserNet



class FriendsListSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода модели отношений двух пользователей."""

    first_user = FriendSerializer()
    second_user = FriendSerializer()

    class Meta:
        model = UserRelations
        fields = ["first_user", "second_user", "accepted_at", "viewed_at"]


class FriendSubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для отправки запроса 'добавить в друзья' одного пользователя - другому."""

    class Meta:
        model = UserRelations
        fields = ["first_user", "second_user"]

    def validate(self, data: dict) -> dict:
        first_user = data["first_user"]
        second_user = data["second_user"]

        if (UserRelations.objects.get_relation_or_none(first_user, second_user).exists()):
            raise serializers.ValidationError(
                {"error": f"Friendship already declared between {first_user} and {second_user}"})
        if second_user == first_user:
            raise serializers.ValidationError({"error": "Can't declare friendship to yourself"})
        return data


class FriendAcceptDeclineSerializer(serializers.ModelSerializer):
    """Сериализатор принятия/отклонения запроса в друзья."""

    class Meta:
        model = UserRelations
        fields = ["accepted_at", "viewed_at"]