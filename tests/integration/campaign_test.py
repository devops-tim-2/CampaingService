from os import environ
environ['SQLALCHEMY_DATABASE_URI'] = environ.get("TEST_DATABASE_URI")

from models.models import Campaign, CampaignActivation, User
from common.config import setup_config
from common.utils import generate_token
import json, pytest


class TestCampaign:
    @classmethod
    def setup_class(cls):
        cls.app = setup_config('test')
        from common.database import db_session

        cls.user1 = User(id=1)
        db_session.add(cls.user1)
        db_session.commit()

        user1_data = dict(id=cls.user1.id)

        cls.token_user1 = generate_token(user1_data)

        cls.client = cls.app.test_client()


    def test_create_happy(cls):
        campaign_count_before = Campaign.query.count()
        campaign_activation_count_before = CampaignActivation.query.count()

        campaign_data = dict(description='some nice description', image_url='some nice image url', interests='some nice interests', age_min=15, age_max=25, regions='Novi Sad', sex='male', times=[1628244000000, 1628330400000, 1628416800000])
        create_response = cls.client.post('/api', data=json.dumps(campaign_data), headers={'Authorization': f'Bearer {cls.token_user1}', 'Content-Type': 'application/json'}).get_json()
        campaign_db: Campaign = Campaign.query.get(create_response['id'])

        campaign_count_after = Campaign.query.count()
        campaign_activation_count_after = CampaignActivation.query.count()

        assert campaign_count_after == campaign_count_before + 1
        assert campaign_activation_count_after == campaign_activation_count_before + len(campaign_data['times'])
        assert campaign_db.description == campaign_data['description']
        assert campaign_db.image_url == campaign_data['image_url']
        assert campaign_db.interests == campaign_data['interests']
        assert campaign_db.age_min == campaign_data['age_min']
        assert campaign_db.age_max == campaign_data['age_max']
        assert campaign_db.regions == campaign_data['regions']
        assert campaign_db.sex == campaign_data['sex']
        assert campaign_db.user_id == cls.user1.id


    def test_create_sad(cls):
        campaign_count_before = Campaign.query.count()
        campaign_activation_count_before = CampaignActivation.query.count()

        campaign_data = dict(description='some nice description', image_url='', interests='some nice interests', age_min=15, age_max=25, regions='Novi Sad', sex='male', times=[1628244000000, 1628330400000, 1628416800000])
        create_response = cls.client.post('/api', data=json.dumps(campaign_data), headers={'Authorization': f'Bearer {cls.token_user1}', 'Content-Type': 'application/json'}).get_json()
        
        campaign_count_after = Campaign.query.count()
        campaign_activation_count_after = CampaignActivation.query.count()

        assert campaign_count_after == campaign_count_before
        assert campaign_activation_count_after == campaign_activation_count_before
