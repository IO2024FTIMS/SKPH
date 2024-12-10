from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    volunteer_id = mapped_column(ForeignKey("volunteer.id"))
    evaluation_id = mapped_column(ForeignKey("evaluation.id"))

    evaluation_ = relationship("Evaluation")
    volunteer = relationship("Volunteer", back_populates="tasks")

    def __repr__(self):
        return f'Task:(id={self.id!r}, name={self.name!r}, description={self.description!r}, volunteer_id={self.volunteer_id!r})'
