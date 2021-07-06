from exception.exceptions import InvalidDataException, NotFoundException
from models.models import Campaign, CampaignActivation, User
from service import campaign_service, user_service
import pytest


def test_create_ok(mocker):
    user_data = {
        "id": 1
    }

    campaign_data = {
        "id": 1,
        "description": 'some nice description',
        "image_url": 'some nice image url',
        "interests": 'some nice interests',
        "age_min": 15,
        "age_max": 25,
        "regions": 'Novi Sad',
        "sex": 'male',
        "user_id": user_data['id'],
        "times": [1628244000000, 1628330400000, 1628416800000]
    }

    expected = Campaign(id=campaign_data['id'], description=campaign_data['description'], image_url=campaign_data['image_url'], interests=campaign_data['interests'], age_min=campaign_data['age_min'], age_max=campaign_data['age_max'], regions=campaign_data['regions'], sex=campaign_data['sex'], user_id=user_data['id'])
    campaign_activation = CampaignActivation(id=1, time=1628244000000, campaign_id=campaign_data['id'])
    
    mocker.patch('service.campaign_service.campaign_repository.save', return_value=expected)
    mocker.patch('service.campaign_service.campaign_activation_service.save', return_value=campaign_activation)

    actual = campaign_service.create(campaign_data, user_data)

    assert expected.get_dict() == actual


def test_create_missing_param():
    user_data = {
        "id": 1
    }

    campaign_data = {
        "description": "some nice description",
        "image_url": '',
        "interests": 'some nice interests',
        "age_min": 15,
        "age_max": 25,
        "regions": 'Novi Sad',
        "sex": 'male',
        "user_id": user_data['id'],
        "times": [1628244000000, 1628330400000, 1628416800000]
    }

    with pytest.raises(InvalidDataException):
        campaign_service.create(campaign_data, user_data)


def test_get_ok(mocker):
    user_data = {
        "id": 1
    }

    campaign_data = {
        "id": 1,
        "description": 'some nice description',
        "image_url": 'some nice image url',
        "interests": 'some nice interests',
        "age_min": 15,
        "age_max": 25,
        "regions": 'Novi Sad',
        "sex": 'male',
        "user_id": user_data['id']
    }

    expected = Campaign(id=campaign_data['id'], description=campaign_data['description'], image_url=campaign_data['image_url'], interests=campaign_data['interests'], age_min=campaign_data['age_min'], age_max=campaign_data['age_max'], regions=campaign_data['regions'], sex=campaign_data['sex'], user_id=user_data['id'])
    mocker.patch('service.campaign_service.campaign_repository.get', return_value=expected)

    actual = campaign_service.get(campaign_data['id'])

    assert expected.get_dict() == actual


def test_get_not_found(mocker):
    expected = None
    mocker.patch('service.campaign_service.campaign_repository.get', return_value=expected)

    with pytest.raises(NotFoundException):
        campaign_service.get(1)