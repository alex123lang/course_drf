from rest_framework import serializers


class HabitsDurationValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        duration = dict(value).get(self.field)
        if duration > 120:
            raise serializers.ValidationError("Длительность привычки не может быть больше 120 минут")


class HabitsPeriodicValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        periodicity = dict(value).get(self.field)
        if 7 < periodicity or periodicity < 1:
            raise serializers.ValidationError("Привычка должна иметь период повторения от 1 дня до 7 дней.")


def validate_related_or_prize(data):
    message = "Может быть выбрана либо связанная привычка либо вознаграждение. "
    if data.get("related") and data.get("prize"):
        return message
    else:
        return ""


def validate_related_is_nice(data):
    message = "Связанные привычки должны быть приятными. "
    if data.get("related") and (not data.get("related").is_nice):
        return message
    else:
        return ""


def validate_nice_not_prize_and_related(data):
    message = "У приятной привычки не может быть связанной привычки или вознаграждения. "
    if data.get("is_nice"):
        if data.get("related") or data.get("prize"):
            return message
    else:
        return ""


def periodicity_is_often_then_once_a_week(data):
    message = "Периодичность привычки не мене 1 раза в 7 дней. Хотя бы один день в неделю должен быть выбран! "

    if (data.get("sunday") is False and data.get("monday") is False and data.get(
            "tuesday") is False and data.get("thursday") is False and data.get(
            "friday") is False and data.get("saturday") is False and data.get("wednesday") is False):
        return message
    else:
        return ""
