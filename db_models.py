from typing import List

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    time_records: Mapped[List["TimeRecord"]] = relationship(back_populates="project")

    def __repr__(self) -> str:
        return f"Project {self.id} {self.title}"


class TimeRecord(Base):
    __tablename__ = "time_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(back_populates="time_record")

    def __repr__(self) -> str:
        return f"TimeRecord {self.id} {self.project_id}"
