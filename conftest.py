import pytest
from task_track.project import Project


@pytest.fixture
def project():
    return Project('test_project')


@pytest.fixture
def unsaved_project():
    return Project('unsaved_project')
