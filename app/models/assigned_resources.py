
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped, foreign

from app.extensions import db

class AssignedResourcesStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_type_id = db.Column(db.Integer, ForeignKey('donation_type.id'), nullable=False)
    campaign_id = db.Column(db.Integer, ForeignKey('charity_campaign.id'), nullable=False)
    affected_id = db.Column(db.Integer, ForeignKey('affected.id'), nullable=False)
    amount = db.Column(db.Integer)


    def __repr__(self):
        return f'ItemStock(id={self.id}, amount={self.amount})'