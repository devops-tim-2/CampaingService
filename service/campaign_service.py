from exception.exceptions import InvalidDataException
from models.models import Campaign, CampaignActivation
from common.utils import check
from repository import campaign_repository
from service import campaign_activation_service
from broker.producer import publish


def create(campaign_data: dict, user: dict) -> Campaign:
    if check(campaign_data):
        raise InvalidDataException('Some of the values are None, empty value or non-positive value')

    campaign = Campaign(description=campaign_data['description'], image_url=campaign_data['image_url'], interests=campaign_data['interests'], age_min=campaign_data['age_min'], age_max=campaign_data['age_max'], regions=campaign_data['regions'], sex=campaign_data['sex'], user_id=user['id'])
    campaign = campaign_repository.save(campaign)
    
    for time in campaign_data['times']:
        campaign_activation = CampaignActivation(time=time, campaign_id=campaign.id)
        campaign_activation_service.save(campaign_activation)

    publish('campaign.created', campaign.get_dict())

    return campaign.get_dict()
