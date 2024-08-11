from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35, **NULLABLE, verbose_name="Телефон", help_text="Укажите телефон"
    )
    city = models.CharField(
        max_length=150,
        **NULLABLE,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )
    tg_nick = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name="Tg name",
        help_text="Укажите telegram-ник",
    )

    tg_chat_id = models.CharField(
        max_length=50,
        verbose_name="Телеграм chat-id",
        help_text="Укажите телеграм chat-id",
    )
    time_offset = models.IntegerField(
        default=3,
        verbose_name="Смещение часового пояса",
        help_text="От -12 до +14, по умолчанию UTC+3 (Московское время)"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"{self.email}"
