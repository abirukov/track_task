import os
from typing import NamedTuple


class Config(NamedTuple):
    sqlalchemy_url: str


def get_config() -> Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    return Config(sqlalchemy_url='sqlite:///' + os.path.join(basedir, 'task_track.db'))
