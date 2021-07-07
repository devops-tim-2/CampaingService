from models.models import CampaignActivation
from repository import campaign_activation_repository


def save(campaign_activation: CampaignActivation):
    return campaign_activation_repository.save(campaign_activation)


def delete(campaign_activation_id: int):
    campaign_activation_repository.delete(campaign_activation_id)


def get_with_campaign(campaign_id: int):
    return campaign_activation_repository.get_with_campaign(campaign_id)