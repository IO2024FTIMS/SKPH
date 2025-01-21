from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped, foreign

from app.extensions import db


class ItemStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_type_id = db.Column(db.Integer, ForeignKey('donation_type.id'), nullable=False)
    campaign_id = db.Column(db.Integer, ForeignKey('charity_campaign.id'), nullable=False)
    amount = db.Column(db.Integer)

    campaign = relationship('CharityCampaign')

