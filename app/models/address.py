from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class Address(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str]
    street_number: Mapped[str]
    city: Mapped[str]
    voivodeship: Mapped[str]

    def __repr__(self):
        return f'Address:(id={self.id!r}, street={self.street!r}, street_number={self.street_number!r}\
                 city={self.city!r}, voivodeship={self.voivodeship!r})'
