from models.models import Campaign
from common.database import db_session


def save(campaign: Campaign):
    db_session.add(campaign)
    db_session.commit()

    return campaign


def delete(campaign_id: int):
    Campaign.query.filter_by(id=campaign_id).delete()
    db_session.commit()


def get(campaign_id: int) -> Campaign:
    return Campaign.query.get(campaign_id)