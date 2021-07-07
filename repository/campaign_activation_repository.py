from models.models import CampaignActivation
from common.database import db_session


def save(campaign_activation: CampaignActivation):
    db_session.add(campaign_activation)
    db_session.commit()

    return campaign_activation


def delete(campaign_activation_id: int):
    CampaignActivation.query.filter_by(id=campaign_activation_id).delete()
    db_session.commit()


def get_with_campaign(campaign_id: int):
    return CampaignActivation.query.filter_by(campaign_id=campaign_id).all()