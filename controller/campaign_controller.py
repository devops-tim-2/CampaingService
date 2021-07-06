from exception.exceptions import InvalidAuthException, InvalidDataException, NotFoundException
from flask_restful import Resource, reqparse
from flask import request
from common.utils import auth
from service import campaign_service

campaign_parser = reqparse.RequestParser()
campaign_parser.add_argument('Authorization', type=str, location='headers', required=True)
campaign_parser.add_argument('description', type=str, help='Description for campaign')
campaign_parser.add_argument('image_url', type=str, help='Image url for campaign')
campaign_parser.add_argument('interests', type=str, help='Interests for campaign')
campaign_parser.add_argument('age_min', type=int, help='Min. age for campaign')
campaign_parser.add_argument('age_max', type=int, help='Max. age for campaign')
campaign_parser.add_argument('regions', type=str, help='Regions for campaign')
campaign_parser.add_argument('sex', type=str, help='Sex for age')
campaign_parser.add_argument('times', type=list, location='json', help='Activation times for campaign')

 
class CampaignResource(Resource):
    def __init__(self):
        # To be implemented.
        pass
 
    def get(self, campaign_id):        
        try:
            if not request.headers.has_key('Authorization'):
                return 'Forbidden, unauthorized atempt.', 403
            else:
                token = request.headers['Authorization'].split(' ')[1]
                auth(token)

                return campaign_service.get(campaign_id), 200
        except InvalidAuthException as e:
            return str(e), 401
        except NotFoundException as e:
            return str(e), 404

class PostCampaignResource(Resource):
    def __init__(self):
        # To be implemented.
        pass
 
    def post(self):
        args = campaign_parser.parse_args()
        token = args['Authorization'].split(' ')[1]
        del args['Authorization']

        try:
            user = auth(token)

            return campaign_service.create(args, user), 200
        except InvalidAuthException as e:
            return str(e), 401
        except InvalidDataException as e:
            return str(e), 400
 
class UserResource(Resource):
    def __init__(self):
        # To be implemented.
        pass
 
    def get(self, user_id):
        page = int(request.args.get('page')) if request.args.get('page') else 1
        per_page = int(request.args.get('per_page')) if request.args.get('per_page') else 10

        try:
            if not request.headers.has_key('Authorization'):
                return 'Forbidden, unauthorized atempt.', 403
            else:
                token = request.headers['Authorization'].split(' ')[1]
                auth(token)
                
                return campaign_service.get_with_user(user_id, page, per_page), 200
        except NotFoundException as e:
            return str(e), 404
 