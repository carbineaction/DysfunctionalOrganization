from dataclasses import dataclass, field
from typing import Optional
from employee import Employee

CHILD_LEVEL = {"President": "VP", "VP": "Supervisor", "Supervisor": "Worker"}
CAPACITY = {"President": 1, "VP": 2, "Supervisor": 3, "Worker": 5}

@dataclass
class Position:
    """One fixed position in the organization. employee=None means vacant."""
    level: str
    employee: Optional[Employee] = None
    parent: Optional["Position"] = None
    children: list["Position"] = field(default_factory=list)

    def __post_init__(self):
        if self.level in CHILD_LEVEL and not self.children:
            child_level = CHILD_LEVEL[self.level]
            self.children = [Position(child_level, parent=self) for _ in range(CAPACITY[child_level])]

    @property
    def is_vacant(self):
        return self.employee is None
