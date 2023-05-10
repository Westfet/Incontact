from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint
from rest_framework.exceptions import ValidationError


class UserNet(AbstractUser):
    # Custom user model
    GENDER = (
        ('male', 'male'),
        ('female', 'female')
    )
    first_login = models.DateTimeField(null=True)
    middle_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=14)
    avatar = models.ImageField(upload_to='user/avatar/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER, default='male')
    friends = models.ManyToManyField("UserNet", through="profiles.UserRelations")


class UserRelationsManager(models.Manager):

    def get_relations_short(self, user_id: int | str) -> list[str]:
        """Метод возвращает только список id друзей - переданного пользователя."""

        # Те, кому отправили заявки
        return UserRelations.objects.filter(
            Q(first_user=user_id) |
            Q(second_user=user_id)
        ).values_list("first_user", flat=True)

    def get_relations_full(self, user_id: int | str) -> models.QuerySet:
        """Возвращает QuerySet из отношений(UserRelations) переданного пользователя."""
        # Те,кому отправили заявки
        return UserRelations.objects.filter(
            Q(first_user=user_id) |
            Q(second_user=user_id)
        )

    def get_relation_or_none(self, user_one: str | UserNet, user_two: str | UserNet) -> \
            models.QuerySet:
        return UserRelations.objects.filter(Q(second_user=user_one, first_user=user_two) |
                                            Q(second_user=user_two, first_user=user_one))


class UserRelations(models.Model):
    # класс, согласно которому создается соотв. таблица
    first_user = models.ForeignKey(UserNet, on_delete=models.CASCADE, related_name="users_first")
    second_user = models.ForeignKey(UserNet, on_delete=models.CASCADE, related_name="users_seconds")

    accepted_at = models.DateTimeField(default=None, blank=True, null=True)
    viewed_at = models.DateTimeField(default=None, blank=True, null=True)

    objects = UserRelationsManager()

    def clean(self) -> None:
        """Метод используется для сложной валидации полей модели."""
        super().clean()
        # есть ли связь между юзерами
        if (self.objects.get_relation_or_none(self.first_user, self.second_user).exclude(
                id=self.id).exists()):
            raise ValidationError(
                f"Friendship already declared between {self.first_user} and {self.second_user}")
        if self.second_user == self.first_user:
            raise ValidationError("Can't declare friendship to yourself")

    class Meta:

        constraints = [
            UniqueConstraint(
                name="s_unique_relationships",
                fields=("first_user", "second_user"),
            ),
            CheckConstraint(
                name="s_prevent_self_follow",
                check=~models.Q(first_user=models.F("second_user")),
            ),
        ]

    def str(self) -> str:
        return f"{self.firstuser.str()}{self.second_user.str()}"
