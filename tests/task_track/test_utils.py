import datetime

import pytest

from db import DB_SESSION
from task_track.project import Project
from task_track.utils import format_time, get_stats_by_days
from task_track.db_models import Project as ProjectModel, TimeRecord


@pytest.mark.parametrize(
    "minutes, expected",
    [
        (1, "1m"),
        (125, "2h 5m"),
    ],
)
def test__format_time(minutes: int, expected: str):
    assert format_time(minutes) == expected


def test__get_stats_by_days(project: Project):
    expected = [{"date": datetime.datetime.now().strftime("%d.%m"), "count_minutes": 20}]
    project.save_to_db()
    project.create_time_record_in_db(count_minutes=20)
    assert get_stats_by_days(project=project, statistic_days=5) == expected
    time_records = TimeRecord.__table__.delete()
    DB_SESSION.execute(time_records)
    DB_SESSION.commit()
    projects = ProjectModel.__table__.delete()
    DB_SESSION.execute(projects)
    DB_SESSION.commit()
