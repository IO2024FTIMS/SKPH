from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.models.request import Request
from app.extensions import db


class Affected(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    needs = db.Column(db.Text)
    address = relationship('Address')
    address_id = mapped_column(ForeignKey('address.id'))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Add the missing relationship
    requests = relationship('app.models.request.Request', back_populates='affected')

    def __repr__(self):
        return f'Affected(id={self.id}, needs={self.needs})'