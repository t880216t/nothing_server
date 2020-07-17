import json, requests
from flask import Blueprint, request
from .. import socketio
from logzero import logger
from app.tables.Data import *
from app import db

websocketClient = Blueprint('websocketClient', __name__)

@socketio.on('connect', namespace='/ws')
def client_connect():
    logger.info(str(request.sid) + '=> Client Connected ')
    configData = PageConfig.query.filter_by(status=1).first()
    content = {
        'musicUrl': None,
        'backgroundUrl': None,
        'sid': request.sid,
    }
    if configData:
        content['musicUrl'] = configData.music_url
        content['backgroundUrl'] = configData.background_url

    socketio.emit('server_response',
                  json.dumps({'code': 0, 'command': 'set_config', 'content': content}),
                  namespace='/ws')

@socketio.on('disconnect', namespace='/ws')
def client_disconnect():
    logger.warning(str(request.sid) + '=> Client Disconnected ')

def getUserAvatar(sid):
    rowData = Users.query.filter_by(user_sid=sid).first()
    if rowData:
        return rowData.user_avatar
    return ''

@socketio.on('send_message', namespace='/ws')
def send_message(data):
    user_sid = data['user_sid']
    message = data['message']
    if request.headers.getlist("X-Forwarded-For"):
        ips = request.headers.getlist("X-Forwarded-For")
        ip = ips[0]
    elif request.headers.getlist("X-Real-IP"):
        ip = request.headers.getlist("X-Real-IP")[0]
    else:
        ip = request.remote_addr
    user_avatar = getUserAvatar(user_sid)
    data = Messages(user_sid,message,ip)
    db.session.add(data)
    db.session.commit()
    content = {
        'id': data.id,
        'message': message,
        'avatar': user_avatar,
    }
    if data.id:
        socketio.emit('server_response', json.dumps({'code': 0, 'command': 'push_message', 'content': content}),
                      namespace='/ws')

@socketio.on('add_user', namespace='/ws')
def add_user(data):
    user_id = data['user_id']
    res = requests.get('https://api.uomg.com/api/rand.avatar?format=json')
    resp = res.json()
    content = {
        'user_sid': user_id,
        'imgurl': ''
    }
    if resp['code'] == 1:
        rowData = Users.query.filter_by(user_sid = user_id).first()
        if not rowData:
            data = Users(user_id, resp['imgurl'])
            db.session.add(data)
            db.session.commit()
        content = {
            'user_sid': user_id,
            'imgurl': resp['imgurl']
        }
    return content