from dataclasses import dataclass, asdict

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base(name='Model')

@dataclass
class Campaign(Model):
    __tablename__ = 'campaign'
    id: int
    description: str
    image_url: str
    interests: str
    age_min: int
    age_max: int
    regions: str
    sex: str
    user_id: int

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    image_url = Column(String(100), nullable=False)
    interests = Column(String(200), nullable=False)
    age_min = Column(Integer, nullable=False)
    age_max = Column(Integer, nullable=False)
    regions = Column(String(200), nullable=False)
    sex = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('userprofile.id'), nullable=False)


    def get_dict(self):
        return asdict(self)


    def __str__(self) -> str:
        return f'Campaign: id={self.id}, description={self.description}, image_url={self.image_url}, interests={self.interests}, age_min={self.age_min}, age_max={self.age_max}, regions={self.regions}, sex={self.sex}, user_id={self.user_id}'


@dataclass
class CampaignActivation(Model):
    __tablename__ = 'campaignactivation'
    id: int
    time: int
    campaign_id: int

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(Integer, nullable=False)
    campaign_id = Column(Integer, ForeignKey('campaign.id'), nullable=False)


    def get_dict(self):
        return asdict(self)


    def __str__(self) -> str:
        return f'CampaignActivation: id={self.id}, time={self.time}, campaign_id={self.campaign_id}'


@dataclass
class User(Model):
    __tablename__ = 'userprofile'
    id: int

    id = Column(Integer, primary_key=True)
    

    def get_dict(self):
        return asdict(self)


    def __str__(self) -> str:
        return f'User: id={self.id}'
