from datetime import datetime
import sqlalchemy

from dataclasses import dataclass
from sqlalchemy.orm import scoped_session

from task_track.daily_minutes import DailyMinutes
from task_track.db_models import Project as ProjectModel, TimeRecord


@dataclass
class Project:
    title: str
    db_session: scoped_session

    def save_to_db(self) -> None:
        self.db_session.add(ProjectModel(title=self.title))
        self.db_session.commit()

    def fetch_from_db(self) -> ProjectModel | None:
        return ProjectModel.query.filter(ProjectModel.title == self.title).first()

    def is_created(self) -> bool:
        return self.fetch_from_db() is not None

    def create_time_record_in_db(self, count_minutes: int) -> None:
        project = self.fetch_from_db()
        if project is not None:
            self.db_session.add(TimeRecord(count_minutes=count_minutes, project_id=project.id))
            self.db_session.commit()

    def get_count_minutes_by_days(self, date_from: datetime, date_to: datetime) -> list[DailyMinutes]:
        project = self.fetch_from_db()
        if not project:
            raise ValueError("Такой проект не найден")
        db_result = self.db_session.query(
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
            count_minutes_by_date.append(
                DailyMinutes(
                    date=day_and_count_minutes[0],
                    count_minutes=day_and_count_minutes[1],
                ),
            )
        return count_minutes_by_date
