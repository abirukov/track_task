from dataclasses import dataclass
import datetime
from typing import Mapping

from db import db_session
from db_models import Project as ProjectModel, TimeRecord


@dataclass
class Project:
    title: str

    def add(self) -> None:
        db_session.add(ProjectModel(title=self.title))
        db_session.commit()

    def get(self) -> ProjectModel:
        return ProjectModel.query.filter(ProjectModel.title == self.title).first()

    def is_set(self) -> bool:
        return self.get() is not None

    def add_time_record(self, count_minutes: int) -> None:
        db_session.add(TimeRecord(count_minutes=count_minutes, project_id=self.get().id))
        db_session.commit()

    def get_time_records(self, statistic_days: int) -> list[TimeRecord | None]:
        project = self.get()
        from_date = datetime.datetime.today() + datetime.timedelta(days=-statistic_days)
        return TimeRecord.query.filter(TimeRecord.datetime > from_date) \
            .filter(TimeRecord.project_id == project.id) \
            .order_by(TimeRecord.datetime.asc()) \
            .all()

    @staticmethod
    def format_time(minutes: int) -> str:
        formatted_time = f"{minutes % 60}m"
        hours = minutes // 60
        if hours != 0:
            formatted_time = f"{hours}h {formatted_time}"
        return formatted_time

    def print_stats(self, statistic_days: int) -> None:
        time_records = self.get_time_records(statistic_days)
        if not time_records:
            print("Записей не найдено")
            return
        stats_by_days = self.prepare_stats_by_days(time_records)
        for daily_stat in stats_by_days:
            print(f"{daily_stat} {self.format_time(stats_by_days[daily_stat])}")

    @staticmethod
    def prepare_stats_by_days(time_records: list[TimeRecord]) -> Mapping[str, int]:
        prepared_stats = {}
        for time_record in time_records:
            formatted_day = time_record.datetime.strftime("%d.%m")
            if formatted_day in prepared_stats.keys():
                prepared_stats[formatted_day] += time_record.count_minutes
            else:
                prepared_stats[formatted_day] = time_record.count_minutes
        return prepared_stats
