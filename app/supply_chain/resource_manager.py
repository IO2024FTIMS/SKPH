from app.extensions import db

from app.models.assigned_resources import AssignedResourcesStock
from app.models.item_stock import ItemStock
from app.models.donation import DonationItem
from app.models.charity_campaign import CharityCampaign


class ResourceManager:
    # select * from donation_item d
    # join charity_campagin c on d.charity_campagin_id=c.id
    def get_all_donations_for_campagin(self, charity_campaign):
        item_donations = db.session.query(DonationItem).join(CharityCampaign) \
            .filter(DonationItem.charity_campaign_id == charity_campaign.id) \
            .all()
        return item_donations

    def get_all_stock_for_campaign(self, charity_campaign):
        item_donations = db.session.query(ItemStock).join(CharityCampaign) \
            .filter(ItemStock.campaign_id == charity_campaign.id) \
            .all()
        return item_donations

    def assign_resources_to_affected(self, dict_affected, resource_used_amount, resource):
        if resource_used_amount <= resource.amount:
            for key in dict_affected.items():
                assigned = AssignedResourcesStock(item_type_id=resource.item_type_id, campaign_id=resource.campaign_id,
                                                  amount=resource_used_amount, affected_id=key)
                db.session.add(assigned)
            if resource.amount == resource_used_amount:
                db.session.delete(resource)
            else:
                resource.amount = resource.amount - resource_used_amount
            db.session.commit()
        else:
            print('Not enough resouce')
