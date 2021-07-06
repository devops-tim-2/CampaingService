from os import environ
from flask_cors import CORS
from flask.app import Flask
from flask_wtf import CSRFProtect
from flask_restful import Api
from apscheduler.schedulers.background import BackgroundScheduler
from broker.producer import publish
from datetime import datetime

config = {
    'test': 'TEST_DATABASE_URI',
    'dev': 'DEV_DATABASE_URI'
}

def setup_config(cfg_name: str):
    environ['SQLALCHEMY_DATABASE_URI'] = environ.get(config[cfg_name])
    
    app = Flask(__name__)
    if environ.get('ENABLE_CSRF') == 1:
        app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
        app.config['WTF_CSRF_SECRET_KEY'] = environ.get('WTF_CSRF_SECRET_KEY')
        csrf = CSRFProtect()
        csrf.init_app(app)
        
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "send_wildcard": "False"}})
    api = Api(app)


    # This import must be postponed because importing common.database has side-effects
    from common.database import init_db
    init_db()


    
    # This import must be postponed after init_db has been called
    from controller.campaign_controller import CampaignResource, PostCampaignResource, UserResource
    api.add_resource(CampaignResource, '/api/<campaign_id>')
    api.add_resource(PostCampaignResource, '/api')
    api.add_resource(UserResource, '/api/profile/<user_id>')


    # This import must be postponed after init_db has been called
    from models.models import Campaign, CampaignActivation, User
    if cfg_name == 'test':
        CampaignActivation.query.delete()
        Campaign.query.delete()
        User.query.delete()
    
    global global_scheduler
    global_scheduler = BackgroundScheduler()

    campaign_activations = CampaignActivation.query.all()

    for campaign_activation in campaign_activations:
        if datetime.now() < datetime.fromtimestamp(campaign_activation.time/1000.0):
            global_scheduler.add_job(publish, run_date=datetime.fromtimestamp(campaign_activation.time/1000.0), id=str(campaign_activation.id), kwargs={'method': 'campaign.published', 'body': campaign_activation.get_dict()})

    global_scheduler.start()

    return app
