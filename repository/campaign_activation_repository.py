from models.models import CampaignActivation
from common.database import db_session


def save(campaign_activation: CampaignActivation):
    db_session.add(campaign_activation)
    db_session.commit()

    return campaign_activation


def delete(campaign_id: int):
    CampaignActivation.query.filter_by(id=campaign_id).delete()
    db_session.commit()