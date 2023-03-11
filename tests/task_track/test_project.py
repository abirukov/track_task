import datetime
from types import NoneType

import pytest

from task_track.daily_minutes import DailyMinutes
from task_track.project import Project
from task_track.db_models import Project as ProjectModel, TimeRecord


def test__save_to_db(project: Project, mock_objects):
    assert len(ProjectModel.query.all()) == 1
    assert ProjectModel.query.first().title == project.title


def test__fetch_from_db_saved_project(project: Project, mock_objects):
    function_result = project.fetch_from_db()
    type_function_result = type(function_result)
    assert type_function_result == ProjectModel
    assert function_result.title == project.title


def test__fetch_from_db_not_saved_project(unsaved_project: Project, mock_objects):
    function_result = unsaved_project.fetch_from_db()
    type_function_result = type(function_result)
    assert type_function_result is NoneType


def test__is_created(project: Project, mock_objects):
    assert project.is_created() is True


def test__is_not_created(unsaved_project: Project, mock_objects):
    assert unsaved_project.is_created() is False


def test__create_time_record_in_db(project: Project, mock_objects):
    count_minutes = 20
    assert len(TimeRecord.query.all()) == 1
    assert TimeRecord.query.first().count_minutes == count_minutes


@pytest.mark.parametrize(
    "date_from, date_to, expected",
    [
        (
            datetime.datetime.now() + datetime.timedelta(days=-1),
            datetime.datetime.now() + datetime.timedelta(days=1),
            [DailyMinutes(date=datetime.datetime.now().strftime("%d.%m"), count_minutes=20)],
        ),
        (
            datetime.datetime.now() + datetime.timedelta(days=-2),
            datetime.datetime.now() + datetime.timedelta(days=-1),
            [],
        ),
    ],
)
def test__get_count_minutes_by_days(
    project: Project,
    date_from: datetime.datetime,
    date_to: datetime.datetime,
    expected,
    mock_objects,
):
    assert project.get_count_minutes_by_days(date_from, date_to) == expected
