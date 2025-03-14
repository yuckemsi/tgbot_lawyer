import datetime
import asyncio

async def get_times_and_dates():
    now = datetime.datetime.now()
    current_hour = now.hour
    current_minute = now.minute

    # Define the time slots for weekdays and Saturday
    weekday_slots = [(hour, minute) for hour in range(9, 19) for minute in (0, 30)]
    saturday_slots = [(hour, minute) for hour in range(11, 15) for minute in (0, 30)]

    def get_next_day_slots(day):
        if day.weekday() == 5:  # Saturday
            return saturday_slots
        elif day.weekday() == 6:  # Sunday
            return []  # Sunday is a day off
        else:
            return weekday_slots

    # Adjust the current time if it's past the working hours
    if current_hour >= 19 or (now.weekday() == 6) or (now.weekday() == 5 and current_hour >= 15):
        now += datetime.timedelta(days=1)
        now = now.replace(hour=9, minute=0, second=0, microsecond=0)
        current_hour = now.hour
        current_minute = now.minute

    # Generate the time slots for today and the next 4 days
    days = {}
    for i in range(5):
        day = now + datetime.timedelta(days=i)
        slots = get_next_day_slots(day)
        if i == 0:  # Filter out past time slots for today
            slots = [(hour, minute) for hour, minute in slots if hour > current_hour or (hour == current_hour and minute > current_minute)]
        if slots:
            day_slots = [f"{hour:02d}:{minute:02d}" for hour, minute in slots]
            days[day.strftime('%d.%m.%Y')] = day_slots

    return days