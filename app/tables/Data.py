from app import db
from datetime import datetime

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_sid = db.Column(db.String(500))
    user_avatar = db.Column(db.String(2000))
    durtime = db.Column(db.Integer)
    add_time = db.Column(db.Text)

    def __init__(self, user_sid,user_avatar):
        self.user_avatar = user_avatar
        self.user_sid = user_sid
        self.add_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Messages(db.Model):
    __tablename__ = 'msg_detail'
    id = db.Column(db.Integer, primary_key=True)
    user_sid = db.Column(db.String(500))
    ip = db.Column(db.String(255))
    message = db.Column(db.Text)
    add_time = db.Column(db.Text)

    def __init__(self, user_sid,message,ip):
        self.user_sid = user_sid
        self.message = message
        self.ip = ip
        self.add_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class PageConfig(db.Model):
    __tablename__ = 'page_config'
    id = db.Column(db.Integer, primary_key=True)
    music_url = db.Column(db.String(1000))
    background_url = db.Column(db.String(1000))
    status = db.Column(db.Integer)
