from os import environ
environ['SQLALCHEMY_DATABASE_URI'] = environ.get("TEST_DATABASE_URI")

from models.models import Campaign, CampaignActivation, User
from common.config import setup_config
from common.utils import generate_token
import json


class TestCampaign:
    @classmethod
    def setup_class(cls):
        cls.app = setup_config('test')
        from common.database import db_session

        cls.user1 = User(id=1)
        db_session.add(cls.user1)
        db_session.commit()

        cls.campaign = Campaign(description='some nice description2', image_url='some nice image url2', interests='some nice interests2', age_min=15, age_max=25, regions='Futog', sex='female', user_id=cls.user1.id)
        db_session.add(cls.campaign)
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


    def test_get_happy(cls):
        create_response = cls.client.get(f'/api/{cls.campaign.id}', headers={'Authorization': f'Bearer {cls.token_user1}'}).get_json()

        assert create_response['id'] == cls.campaign.id


    def test_get_sad(cls):
        create_response = cls.client.get(f'/api/{-1}', headers={'Authorization': f'Bearer {cls.token_user1}'})
        
        assert create_response.status_code == 404


    def test_get_agent_posts_happy(cls):
        get_response = cls.client.get(f'/api/profile/{cls.user1.id}?page=1&per_page=1', headers={'Authorization': f'Bearer {cls.token_user1}'}).get_json()
        
        assert len(get_response) == 1


    def test_get_agent_posts_sad(cls):
        get_response = cls.client.get(f'/api/profile/{2}', headers={'Authorization': f'Bearer {cls.token_user1}'})
        
        assert get_response.status_code == 404
