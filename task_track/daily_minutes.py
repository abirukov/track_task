import dataclasses


@dataclasses.dataclass
class DailyMinutes:
    date: str
    count_minutes: int
