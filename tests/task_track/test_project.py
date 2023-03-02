import datetime
from types import NoneType

import pytest
from pytest_lazyfixture import lazy_fixture

from db import DB_SESSION
from task_track.project import Project
from task_track.db_models import Project as ProjectModel, TimeRecord


def test__save_to_db(project: Project):
    project.save_to_db()
    assert len(ProjectModel.query.all()) == 1
    assert ProjectModel.query.first().title == project.title
    projects = ProjectModel.__table__.delete()
    DB_SESSION.execute(projects)
    DB_SESSION.commit()


@pytest.mark.parametrize(
    "project_obj, expected_type",
    [
        (lazy_fixture("project"), ProjectModel),
        (lazy_fixture("unsaved_project"), NoneType),
    ],
)
def test__fetch_from_db(project_obj: Project, expected_type):
    if expected_type == ProjectModel:
        project_obj.save_to_db()
    function_result = project_obj.fetch_from_db()
    type_function_result = type(function_result)
    assert type_function_result == expected_type
    if type_function_result == ProjectModel:
        assert function_result.title == project_obj.title
    projects = ProjectModel.__table__.delete()
    DB_SESSION.execute(projects)
    DB_SESSION.commit()


@pytest.mark.parametrize(
    "project_obj, expected",
    [
        (lazy_fixture("project"), True),
        (lazy_fixture("unsaved_project"), False),
    ],
)
def test__is_created(project_obj: Project, expected: bool):
    if expected:
        project_obj.save_to_db()
    assert project_obj.is_created() == expected


def test__create_time_record_in_db(project: Project):
    count_minutes = 20
    project.save_to_db()
    project.create_time_record_in_db(count_minutes)
    assert len(TimeRecord.query.all()) == 1
    assert TimeRecord.query.first().count_minutes == count_minutes
    time_records = TimeRecord.__table__.delete()
    DB_SESSION.execute(time_records)
    DB_SESSION.commit()
    projects = ProjectModel.__table__.delete()
    DB_SESSION.execute(projects)
    DB_SESSION.commit()


@pytest.mark.parametrize(
    "date_from, date_to, expected",
    [
        (
            datetime.datetime.now() + datetime.timedelta(days=-1),
            datetime.datetime.now() + datetime.timedelta(days=1),
            [{"date": datetime.datetime.now().strftime("%d.%m"), "count_minutes": 20}],
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
):
    project.save_to_db()
    project.create_time_record_in_db(count_minutes=20)
    assert project.get_count_minutes_by_days(date_from, date_to) == expected
    time_records = TimeRecord.__table__.delete()
    DB_SESSION.execute(time_records)
    DB_SESSION.commit()
    projects = ProjectModel.__table__.delete()
    DB_SESSION.execute(projects)
    DB_SESSION.commit()
