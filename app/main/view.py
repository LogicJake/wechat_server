# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 20:04:12
# @Last Modified time: 2019-03-13 18:38:50
from flask import Blueprint, request
from app.main.operations import init_room, enter_room, update_room
from app.main.message import send_message

bp = Blueprint('main', __name__)


@bp.route('/')
def test():
    return 'test'


@bp.route('/message', methods=['POST'])
def message():
    data = request.get_json()

    if 'message' in data.keys():
        parse_message(data['message'])
    return 'ok'


def parse_message(message):
    content = message['text']
    uid = message['from']['id']

    if not content.startswith('/'):
        send_message(uid, '现在只能识别命令')
        return

    ss = content.split(' ')
    if ss[0] == '/new':
        parse_new(message)
    elif ss[0] == '/enter':
        parse_enter(message)
    elif ss[0] == '/change':
        parse_change(message)


def parse_change(message):
    content = message['text']
    uid = message['from']['id']

    ss = content.split(' ')
    if len(ss) > 1:
        if len(ss) != 3:
            send_message(uid, '命令格式错误，如果需要自定义词语，请输入两个词')
            return
        else:
            good_word = ss[1]
            bad_word = ss[2]
            update_room(uid, good_word, bad_word)
    else:
        update_room(uid)


def parse_enter(message):
    content = message['text']
    uid = message['from']['id']

    ss = content.split(' ')
    if len(ss) != 2:
        send_message(uid, '命令格式错误，需要指定房间号')
        return

    room_id = ss[1]

    try:
        room_id = int(room_id)
    except ValueError:
        send_message(uid, '命令格式错误，房间号只能为数字')
        return
    enter_room(room_id, uid)


def parse_new(message):
    content = message['text']
    uid = message['from']['id']

    ss = content.split(' ')
    if len(ss) < 2:
        send_message(uid, '命令格式错误，至少需要指定参与人数')
        return

    uid = message['from']['id']
    user_name = message['from']['username']

    try:
        num = int(ss[1])
    except ValueError:
        send_message(uid, '命令格式错误，人数只能是数字')
        return

    if len(ss) > 2:
        if len(ss) != 4:
            send_message(uid, '命令格式错误，如果需要自定义词语，请输入两个词')
            return
        else:
            good_word = ss[2]
            bad_word = ss[3]
            init_room(num, uid, user_name, good_word, bad_word)

    else:
        init_room(num, uid, user_name)
