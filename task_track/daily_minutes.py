import dataclasses


@dataclasses.dataclass
class DailyMinutes:
    def __init__(self, date: str, count_minutes: int):
        self.count_minutes = count_minutes
        self.date = date
