import pytest

from db import DB_SESSION
from task_track.db_models import Project as ProjectModel, TimeRecord
from task_track.project import Project


@pytest.fixture
def project():
    return Project('test_project', db_session=DB_SESSION)


@pytest.fixture
def unsaved_project():
    return Project('unsaved_project', db_session=DB_SESSION)


@pytest.fixture
def mock_objects(project):
    project.save_to_db()
    project.create_time_record_in_db(count_minutes=20)
    time_records = TimeRecord.__table__.delete()
    DB_SESSION.execute(time_records)
    DB_SESSION.commit()
    projects = ProjectModel.__table__.delete()
    DB_SESSION.execute(projects)
    DB_SESSION.commit()
