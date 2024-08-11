from datetime import datetime
from django.utils import timezone
from celery import shared_task
from habits.services import send_telegram_message
from habits.models import Habits


@shared_task
def send_information_about_habit(message, tg_chat_id):
    send_telegram_message(message, tg_chat_id)


@shared_task
def find_all_habits():
    print("find_all_habits")

    habit_time = datetime.now().replace(second=0, microsecond=0)
    current_weekday = timezone.now().weekday()

    # Фильтрация привычек по времени
    habits = Habits.objects.filter(user__isnull=False, utc_time=habit_time)

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
