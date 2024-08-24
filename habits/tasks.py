from datetime import datetime, timedelta
from django.utils import timezone
from celery import shared_task
from habits.services import send_telegram_message
from habits.models import Habits


@shared_task
def send_information_about_habit(message, tg_chat_id):
    send_telegram_message(tg_chat_id, message)


@shared_task
def find_all_habits():
    print("find_all_habits")

    habit_time = timezone.now()  # Используем timezone.now() для корректного учета часового пояса
    current_weekday = habit_time.weekday()

    # Интервал в несколько минут
    start_time = habit_time - timedelta(minutes=1)
    end_time = habit_time + timedelta(minutes=1)

    # Фильтрация привычек по времени с учетом интервала
    habits = Habits.objects.filter(user__isnull=False, time__gte=start_time, time__lte=end_time)

    # Словарь для сопоставления дня недели и поля привычки
    day_mapping = {
        0: 'monday',
        1: 'tuesday',
        2: 'wednesday',
        3: 'thursday',
        4: 'friday',
        5: 'saturday',
        6: 'sunday',
    }

    for habit in habits:
        habit_weekday = (current_weekday + habit.weekday_offset) % 7
        day_field = day_mapping.get(habit_weekday)

        # Проверка, должна ли привычка выполняться в текущий день
        if getattr(habit, day_field, False):
            tg_chat_id = habit.user.tg_chat_id
            message = f"Я буду (действие): [{habit.action}] в (место): [{habit.place}] (время): [{habit.time}]"
            send_information_about_habit.delay(message, tg_chat_id)
