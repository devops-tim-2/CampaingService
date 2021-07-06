from exception.exceptions import InvalidAuthException, InvalidDataException, NotFoundException
from models.models import Campaign, CampaignActivation
from common.utils import check
from repository import campaign_repository
from service import campaign_activation_service, user_service
from broker.producer import publish
from datetime import datetime
from common import config


def create(campaign_data: dict, user: dict) -> dict:
    if check(campaign_data):
        raise InvalidDataException('Some of the values are None, empty value or non-positive value')
    elif any(datetime.now() > datetime.fromtimestamp(time/1000.0) for time in campaign_data['times']):
        raise InvalidDataException('Campaign cannot be activated in the past.')
    elif campaign_data['age_min'] < 0 or campaign_data['age_min'] > campaign_data['age_max']:
        raise InvalidDataException('Invalid value for min. age or max. age.')
    elif not user_service.get(user['id']):
        raise InvalidAuthException('Your are not allowed to create new campaign.')

    campaign = Campaign(description=campaign_data['description'], image_url=campaign_data['image_url'], interests=campaign_data['interests'], age_min=campaign_data['age_min'], age_max=campaign_data['age_max'], regions=campaign_data['regions'], sex=campaign_data['sex'], user_id=user['id'])
    campaign = campaign_repository.save(campaign)
    
    for time in campaign_data['times']:
        campaign_activation = CampaignActivation(time=time/1000.0, campaign_id=campaign.id)
        campaign_activation = campaign_activation_service.save(campaign_activation)
        config.global_scheduler.add_job(publish, run_date=datetime.fromtimestamp(time/1000.0), id=str(campaign_activation.id), kwargs={'method': 'campaign.published', 'body': campaign_activation.get_dict()})
        
    publish('campaign.created', campaign.get_dict())
    
    return campaign.get_dict()


def get(campaign_id: int) -> dict:
    campaign = campaign_repository.get(campaign_id)

    if not campaign:
        raise NotFoundException(f'Campaign with id {campaign_id} not found.')

    return campaign.get_dict()


def get_with_user(user_id: int, page: int, per_page: int) -> list:
    if not user_service.get(user_id):
        raise NotFoundException(f'User with id {user_id} not found.')

    campaigns = campaign_repository.get_with_user(user_id)

    return [campaign.get_dict() for campaign in campaigns][(page-1)*per_page : page*per_page]
