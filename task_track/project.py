import datetime
import sqlalchemy

from dataclasses import dataclass

from db import db_session
from task_track.db_models import Project as ProjectModel, TimeRecord


@dataclass
class Project:
    title: str

    def create(self) -> None:
        db_session.add(ProjectModel(title=self.title))
        db_session.commit()

    def fetch_from_db(self) -> ProjectModel | None:
        return ProjectModel.query.filter(ProjectModel.title == self.title).first()

    def is_created(self) -> bool:
        return self.fetch_from_db() is not None

    def create_time_record_in_db(self, count_minutes: int) -> None:
        db_session.add(TimeRecord(count_minutes=count_minutes, project_id=self.fetch_from_db().id))
        db_session.commit()

    def get_time_by_days(self, date_from: datetime, date_to: datetime) -> list[tuple[str, int]] | list[None]:
        project = self.fetch_from_db()
        return db_session.query(
            sqlalchemy.func.strftime("%d.%m", TimeRecord.datetime),
            sqlalchemy.func.sum(TimeRecord.count_minutes),
        ).filter(
            TimeRecord.datetime >= date_from,
            TimeRecord.datetime <= date_to,
        ).filter(
            TimeRecord.project_id == project.id
        ).order_by(
            TimeRecord.datetime.asc()
        ).group_by(
            sqlalchemy.func.strftime("%d.%m.%Y", TimeRecord.datetime)
        ).all()
