import datetime

import pytest

from task_track.daily_minutes import DailyMinutes
from task_track.project import Project
from task_track.utils import format_time, get_stats_by_days


@pytest.mark.parametrize(
    "minutes, expected",
    [
        (1, "1m"),
        (125, "2h 5m"),
    ],
)
def test__format_time(minutes: int, expected: str):
    assert format_time(minutes) == expected


def test__get_stats_by_days(project: Project, mock_objects):
    expected = [DailyMinutes(date=datetime.datetime.now().strftime("%d.%m"), count_minutes=20)]
    assert get_stats_by_days(project=project, statistic_days=5) == expected
