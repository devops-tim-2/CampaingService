# from os import environ
# environ['SQLALCHEMY_DATABASE_URI'] = environ.get("TEST_DATABASE_URI")

# from models.models import Block, Post, User
# from common.config import setup_config
# from common.utils import generate_token
# import json, pytest


# class TestPost:
#     @classmethod
#     def setup_class(cls):
#         cls.app = setup_config('test')
#         from common.database import db_session

#         cls.user1 = User(public=True)
#         db_session.add(cls.user1)
#         db_session.commit()

#         cls.user2 = User(public=True)
#         db_session.add(cls.user2)
#         db_session.commit()

#         block = Block(src=cls.user1.id, dst=cls.user2.id)
#         db_session.add(block)
#         db_session.commit()

#         user1_data = dict(id=cls.user1.id, username="milos", password="milos", role="user", age=18, sex="m", region="srb", interests="sport", bio="some bio", website="https://milos.com", phone="some phone", mail="milos@mail.com", profile_image_link="https://milos.com/profile.jpg", public=cls.user1.public, taggable=True)
#         user2_data = dict(id=cls.user2.id, username="milos2", password="milos2", role="user", age=18, sex="m", region="srb", interests="sport", bio="some bio", website="https://milos2.com", phone="some phone", mail="milos2@mail.com", profile_image_link="https://milos2.com/profile.jpg", public=cls.user2.public, taggable=True)

#         cls.token_user1 = generate_token(user1_data)
#         cls.token_user2 = generate_token(user2_data)

#         cls.post1 = Post(description='some nice description3', image_url='some nice image_url3', user_id=cls.user1.id)
#         db_session.add(cls.post1)
#         db_session.commit()

#         cls.post2 = Post(description='some nice description4', image_url='some nice image_url4', user_id=cls.user1.id)
#         db_session.add(cls.post2)
#         db_session.commit()

#         cls.client = cls.app.test_client()


#     def test_get_happy(cls):
#         get_response = cls.client.get(f'/api/{cls.post1.id}', headers={'Authorization': f'Bearer {cls.token_user1}', 'Content-Type': 'application/json'}).get_json()
#         assert get_response['id'] == cls.post1.id


#     def test_get_sad(cls):
#         get_response = cls.client.get(f'/api/{-1}', headers={'Authorization': f'Bearer {cls.token_user1}', 'Content-Type': 'application/json'})
#         assert get_response.status_code == 404


#     def test_get_users_posts_happy(cls):
#         get_response = cls.client.get(f'/api/profile/{cls.user1.id}?page=1&per_page=1', headers={'Authorization': f'Bearer {cls.token_user1}', 'Content-Type': 'application/json'}).get_json()
#         assert len(get_response) == 1


#     def test_get_users_posts_sad(cls):
#         get_response = cls.client.get(f'/api/profile/{cls.user2.id}', headers={'Authorization': f'Bearer {cls.token_user1}', 'Content-Type': 'application/json'})
#         assert get_response.status_code == 404


#     def test_create_happy(cls):
#         post_count_before = Post.query.count()

#         post_data = dict(description='some nice description', image_url='some nice image_url')
#         create_response = cls.client.post('/api', data=json.dumps(post_data), headers={'Authorization': f'Bearer {cls.token_user1}', 'Content-Type': 'application/json'}).get_json()
#         post_db = Post.query.get(create_response['id'])

#         post_count_after = Post.query.count()

#         assert post_count_after == post_count_before + 1
#         assert post_db.description == post_data['description']
#         assert post_db.image_url == post_data['image_url']
#         assert post_db.user_id == cls.user1.id


#     def test_create_sad(cls):
#         post_count_before = Post.query.count()

#         post_data = dict(description='some nice description 2', image_url='')
#         create_response = cls.client.post('/api', data=json.dumps(post_data), headers={'Authorization': f'Bearer {cls.token_user1}', 'Content-Type': 'application/json'}).get_json()
        
#         post_count_after = Post.query.count()

#         assert post_count_after == post_count_before


#     def test_delete_happy(cls):
#         post_count_before = Post.query.count()

#         delete_response = cls.client.delete(f'/api/{cls.post2.id}', headers={'Authorization': f'Bearer {cls.token_user1}', 'Content-Type': 'application/json'}).get_json()
        
#         post_count_after = Post.query.count()

#         assert post_count_after == post_count_before - 1


#     def test_delete_sad(cls):
#         delete_response = cls.client.delete(f'/api/{cls.post1.id}', headers={'Authorization': f'Bearer {cls.token_user2}', 'Content-Type': 'application/json'})
        
#         assert delete_response.status_code == 404
