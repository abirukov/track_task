from datetime import datetime
import sqlalchemy

from dataclasses import dataclass

from db import DB_SESSION
from task_track.db_models import Project as ProjectModel, TimeRecord


@dataclass
class Project:
    title: str

    def save_to_db(self) -> None:
        DB_SESSION.add(ProjectModel(title=self.title))
        DB_SESSION.commit()

    def fetch_from_db(self) -> ProjectModel | None:
        return ProjectModel.query.filter(ProjectModel.title == self.title).first()

    def is_created(self) -> bool:
        return self.fetch_from_db() is not None

    def create_time_record_in_db(self, count_minutes: int) -> None:
        if self.fetch_from_db():
            DB_SESSION.add(TimeRecord(count_minutes=count_minutes, project_id=self.fetch_from_db().id))
            DB_SESSION.commit()

    def get_count_minutes_by_days(self, date_from: datetime, date_to: datetime) -> list[dict | None]:
        project = self.fetch_from_db()
        if not project:
            raise ValueError("Такой проект не найден")
        db_result = DB_SESSION.query(
            sqlalchemy.func.strftime("%d.%m", TimeRecord.datetime),
            sqlalchemy.func.sum(TimeRecord.count_minutes),
        ).filter(
            TimeRecord.datetime >= date_from,
            TimeRecord.datetime <= date_to,
            TimeRecord.project_id == project.id,
        ).order_by(
            TimeRecord.datetime.asc(),
        ).group_by(
            sqlalchemy.func.strftime("%d.%m.%Y", TimeRecord.datetime),
        ).all()
        count_minutes_by_date = []
        for day_and_count_minutes in db_result:
            count_minutes_by_date.append(dict(zip(['date', 'count_minutes'], day_and_count_minutes)))
        return count_minutes_by_date
