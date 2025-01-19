from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.volunteer import Volunteer

volunteer_campaign_association = Table(
    'volunteer_campaign_association',
    db.Model.metadata,
    db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteer.id')),
    db.Column('campaign_id', db.Integer, db.ForeignKey('organization_charity_campaign.id'))
)


class CharityCampaign(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    authority = relationship('Authorities')
    authorities_id = mapped_column(ForeignKey('authorities.id'), nullable=False)

    def __repr__(self):
        return f'CharityCampaign({self.id=}, {self.name=}, {self.description=}, {self.authority=})'


class OrganizationCharityCampaign(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    charity_campaign = relationship('CharityCampaign')
    organization = relationship('Organization')
    charity_campaign_id: Mapped[int] = mapped_column(ForeignKey('charity_campaign.id'), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organization.id'), nullable=False)
    volunteers: Mapped[list['Volunteer']] = (
        relationship('Volunteer', secondary=volunteer_campaign_association, back_populates='campaigns')
    )
