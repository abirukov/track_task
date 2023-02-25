import click

from project import Project


def track(project_title: str, count_minutes: int) -> None:
    project = Project(title=project_title)
    if not project.is_set():
        project.add()
    project.add_time_record(count_minutes)


def stat(project_title: str, statistic_days: int) -> None:
    project = Project(title=project_title)
    project.print_stats(statistic_days)


@click.command()
@click.argument('command_name')
@click.option('--project', required=True, help='Tracked project')
@click.argument('count_minutes', type=int, required=False)
@click.option('--days', help='Statistics period', default=5, type=int, required=False)
def main(command_name: str, project: str, count_minutes: int, days: int):
    if command_name == 'track':
        track(project, count_minutes)
    elif command_name == 'stat':
        stat(project, days)
    else:
        print('Введите корректную команду')


if __name__ == '__main__':
    main()

# Залогировать 15 минут на проект learn
# $ python track.py track --project=learn 15

# показать статистику по проекту learn за последние 5 дней
# $ python track.py stat --project=learn --days=5
