#-*-coding:utf-8-*-
from flask import Flask
from flask_socketio import SocketIO
from datetime import timedelta

app = Flask(__name__)
app.config['KEY'] = 'oHdAssadiWbH' # 加密秘钥
app.config['SECRET_KEY']= "thisisadfsacoolpaltpalt" #设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=1) #设置session的保存时间。
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///../db/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

'''
数据库对象创建
'''
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
socketio = SocketIO(app)

'''
注册蓝图
'''
from .devices.websocketCilent import websocketClient
app.register_blueprint(websocketClient)