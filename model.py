from dataclasses import dataclass

# MODEL CLASS: : OOP


@dataclass
class ItemsModel:
    id: int
    student_number: str
    name: str
    description: str
    date: str
    location: str
    contact: str
    status: str
    updated: str
    archived: int
