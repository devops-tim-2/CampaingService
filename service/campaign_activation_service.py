from models.models import CampaignActivation
from repository import campaign_activation_repository


def save(campaign_activation: CampaignActivation):
    return campaign_activation_repository.save(campaign_activation)