import datetime
from task_track.project import Project


def format_time(minutes: int) -> str:
    formatted_time = f"{minutes % 60}m"
    hours = minutes // 60
    if hours != 0:
        formatted_time = f"{hours}h {formatted_time}"
    return formatted_time


def print_stats(project: Project, statistic_days: int) -> None:
    date_from = datetime.datetime.today() + datetime.timedelta(days=-statistic_days)
    date_to = datetime.datetime.today()
    time_by_days = project.get_time_by_days(date_from, date_to)
    if not time_by_days:
        print("Записей не найдено")
        return
    for daily_date_and_stat in time_by_days:
        print(f"{daily_date_and_stat[0]} {format_time(daily_date_and_stat[1])}")
