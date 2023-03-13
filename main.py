import click

from db import DB_SESSION
from task_track.project import Project
from task_track.utils import print_stats, get_stats_by_days


def track(project_title: str, count_minutes: int) -> None:
    project = Project(title=project_title, db_session=DB_SESSION)
    if not project.is_created():
        project.save_to_db()
    project.create_time_record_in_db(count_minutes)


def print_statistic(project_title: str, statistic_days: int) -> None:
    project = Project(title=project_title, db_session=DB_SESSION)
    stats = get_stats_by_days(project, statistic_days)
    print_stats(stats)


@click.command()
@click.argument('command_name')
@click.option('--project', required=True, help='Tracked project')
@click.argument('count_minutes', type=int, required=False)
@click.option('--days', help='Statistics period', default=5, type=int, required=False)
def main(command_name: str, project: str, count_minutes: int, days: int):
    if command_name == 'track':
        track(project, count_minutes)
    elif command_name == 'stat':
        print_statistic(project, days)
    else:
        print('Введите корректную команду')


if __name__ == '__main__':
    main()
