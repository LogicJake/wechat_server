# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 20:04:12
# @Last Modified time: 2019-03-14 20:42:32
from flask import Blueprint, request
from app.main.operations import init_room, enter_room, update_room
from app.models.verify import Verify
from app.models.reply import Reply
import requests

bp = Blueprint('main', __name__)


@bp.route('/')
def test():
    return 'test'


@bp.route('/create_menu')
def create_menu():
    vertify = Verify()

    token = vertify.get_token()
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}'.format(
        token)
    data = {
        'button': [
            {
                'type': 'click',
                'name': '谁是卧底',
                'key': '"'play_shuishiwodi'"'
            },
        ]
    }

    headers = {
        'Content-Type': 'application/json',
        'encoding': 'utf-8'
    }
    r = requests.post(url, data=data, headers=headers)
    return r.text


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

            if ss[0] == 'new':
                reply_content = parse_new(message)
            elif ss[0] == 'enter':
                reply_content = parse_enter(message)
            elif ss[0] == 'change':
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

    user_name = uid

    try:
        num = int(ss[1])
    except ValueError:
        return '命令格式错误，人数只能是数字'

    if len(ss) > 2:
        if len(ss) == 3:
            try:
                white = int(ss[2])
                if white == 1:
                    return init_room(num, uid, user_name, white=True)
                else:
                    return '命令格式不正确'
            except ValueError:
                return '命令格式不正确'

        if len(ss) == 4:
            good_word = ss[2]
            bad_word = ss[3]
            return init_room(num, uid, user_name, good_word, bad_word)
        if len(ss) == 5:
            try:
                good_word = ss[2]
                bad_word = ss[3]
                white = int(ss[4])
                if white == 1:
                    return init_room(num, uid, user_name, good_word, bad_word, True)
                else:
                    return '命令格式不正确'
            except ValueError:
                return '命令格式不正确'
        else:
            return '你输这么多参数干嘛?'

    else:
        return init_room(num, uid, user_name)
