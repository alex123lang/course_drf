from rest_framework import serializers

from habits.models import Habits
from habits.validators import HabitsDurationValidator, validate_related_or_prize, validate_related_is_nice, \
    validate_nice_not_prize_and_related, periodicity_is_often_then_once_a_week, HabitsPeriodicValidator


class HabitSerializer(serializers.ModelSerializer):
    validators = [HabitsDurationValidator(field="duration"), HabitsPeriodicValidator(field="periodicity")]

    class Meta:
        model = Habits
        fields = "__all__"

    def validate(self, data):

        message = validate_related_or_prize(data) + validate_related_is_nice(data)
        message += validate_nice_not_prize_and_related(data) + periodicity_is_often_then_once_a_week(data)

        if message:
            raise serializers.ValidationError(message)

        return data
