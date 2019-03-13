# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 20:04:12
# @Last Modified time: 2019-03-13 20:16:03
from flask import Blueprint, request
from app.main.operations import init_room, enter_room, update_room
from app.models.verify import Verify
from app.models.post import Reply

bp = Blueprint('main', __name__)


@bp.route('/')
def test():
    return 'test'


@bp.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == "GET":
        message = Verify(request)
        message.verify()
        return message.return_code

    elif request.method == "POST":
        message = Reply(request)

        if message.msg_type == 'text':
            content = message.content
            ss = content.split(' ')

            if ss[0] == '/new':
                reply_content = parse_new(message)
            elif ss[0] == '/enter':
                reply_content = parse_enter(message)
            elif ss[0] == '/change':
                reply_content = parse_change(message)
            else:
                reply_content = '???????'

            message.text(reply_content)
            return message.reply()


def parse_change(message):
    content = message.content
    uid = message.from_user_name

    ss = content.split(' ')
    if len(ss) > 1:
        if len(ss) != 3:
            return '命令格式错误，如果需要自定义词语，请输入两个词'
        else:
            good_word = ss[1]
            bad_word = ss[2]
            return update_room(uid, good_word, bad_word)
    else:
        return update_room(uid)


def parse_enter(message):
    content = message.content
    uid = message.from_user_name

    ss = content.split(' ')
    if len(ss) != 2:
        return '命令格式错误，需要指定房间号'

    room_id = ss[1]

    try:
        room_id = int(room_id)
    except ValueError:
        return '命令格式错误，房间号只能为数字'

    return enter_room(room_id, uid)


def parse_new(message):
    content = message.content
    uid = message.from_user_name

    ss = content.split(' ')
    if len(ss) < 2:
        return '命令格式错误，至少需要指定参与人数'

    uid = message['from']['id']
    user_name = message['from']['username']

    try:
        num = int(ss[1])
    except ValueError:
        return '命令格式错误，人数只能是数字'

    if len(ss) > 2:
        if len(ss) != 4:
            return '命令格式错误，如果需要自定义词语，请输入两个词'

        else:
            good_word = ss[2]
            bad_word = ss[3]
            return init_room(num, uid, user_name, good_word, bad_word)

    else:
        return init_room(num, uid, user_name)
