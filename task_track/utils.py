import datetime
from task_track.project import Project


def format_time(minutes: int) -> str:
    formatted_time = f"{minutes % 60}m"
    hours = minutes // 60
    if hours:
        formatted_time = f"{hours}h {formatted_time}"
    return formatted_time


def print_stats(stats: list[dict | None]) -> None:
    if not stats:
        print("Записей не найдено")
        return
    for daily_date_and_stat in stats:
        print(f"{daily_date_and_stat['date']} {format_time(daily_date_and_stat['count_minutes'])}")


def get_stats_by_days(project: Project, statistic_days: int) -> list[dict | None]:
    date_from = datetime.datetime.today() + datetime.timedelta(days=-statistic_days)
    date_to = datetime.datetime.today()
    return project.get_count_minutes_by_days(date_from, date_to)
