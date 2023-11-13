from datetime import date
from calendar import monthrange


def define_next_date(current_date: date) -> date:
    next_day: int = current_date.day
    next_month: int = current_date.month + 1
    next_year: int = current_date.year

    if next_month == 13:
        next_month = 1
        next_year += 1

    if (next_day > 29) or ((next_day == 29) and (next_month == 2)):
        next_day = monthrange(next_year, next_month)[1]

    return date(day=next_day, month=next_month, year=next_year)
