from __future__ import annotations

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

BOOKING_TIME_ZONE = ZoneInfo("Asia/Tashkent")
BOOKING_OPEN_TIME = time(10, 0)
BOOKING_CLOSE_TIME = time(23, 0)
BOOKING_STEP_MINUTES = 15


def _round_up(minutes: int) -> int:
    step = BOOKING_STEP_MINUTES
    return ((minutes + step - 1) // step) * step


def _minutes(value: time) -> int:
    return value.hour * 60 + value.minute


def _time_from_minutes(value: int) -> time:
    return time(value // 60, value % 60)


def booking_window(now: datetime | None = None) -> dict[str, str]:
    current = now.astimezone(BOOKING_TIME_ZONE) if now else datetime.now(BOOKING_TIME_ZONE)
    min_date = current.date()
    min_time = BOOKING_OPEN_TIME
    now_minutes = _minutes(current.time().replace(second=0, microsecond=0))
    open_minutes = _minutes(BOOKING_OPEN_TIME)
    close_minutes = _minutes(BOOKING_CLOSE_TIME)

    if now_minutes > close_minutes:
        min_date = min_date + timedelta(days=1)
    elif now_minutes > open_minutes:
        rounded = _round_up(now_minutes)
        if rounded > close_minutes:
            min_date = min_date + timedelta(days=1)
        else:
            min_time = _time_from_minutes(rounded)

    return {
        "min_date": min_date.isoformat(),
        "min_time": min_time.strftime("%H:%M"),
        "max_time": BOOKING_CLOSE_TIME.strftime("%H:%M"),
    }


def is_bookable(booking_date: date, booking_time: time) -> bool:
    window = booking_window()
    date_value = booking_date.isoformat()
    time_value = booking_time.strftime("%H:%M")
    return date_value > window["min_date"] or (
        date_value == window["min_date"] and time_value >= window["min_time"]
    )
