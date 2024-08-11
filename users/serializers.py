from rest_framework import serializers
from users.models import User
from users.validators import TimeOffsetValidator


class UserSerializer(serializers.ModelSerializer):
    validators = [TimeOffsetValidator(field="time_offset")]

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}


class UserLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "tg_nick", "tg_chat_id", "last_login",
                  "avatar", "date_joined", "is_superuser", "is_staff", "is_active", "time_offset")
