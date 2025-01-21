from app.extensions import db

from datetime import datetime


from app.models.volunteer import Volunteer
from app.models.organization import Organization
from app.models.address import Address
from app.models.affected import Affected
from app.models.donation import DonationItem
from app.models.donation import DonationMoney
from app.models.donor import Donor
from app.models.user import User
from app.models.charity_campaign import CharityCampaign
from app.models.charity_campaign import OrganizationCharityCampaign


class ResourceManager:
    def init(self):
        self.test = 'test'

    # select * from donation_item d
    # join charity_campagin c on d.charity_campagin_id=c.id 

    def get_all_donations_for_campagin(self, charity_campaign):
        item_donations = db.session.query(DonationItem).join(CharityCampaign) \
        .filter(DonationItem.charity_campaign_id == charity_campaign.id) \
        .all()
        return item_donations

