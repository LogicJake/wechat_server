from flask import Blueprint, request
from werkzeug.contrib.cache import SimpleCache

from app.models.reply import Reply
from app.models.verify import Verify
from app.utils import update_competition

cache = SimpleCache()
bp = Blueprint('main', __name__)


@bp.route('/')
def test():
    return 'working'


@bp.route('/message', methods=['GET', 'POST'])
def message():
    news_welcome = {
        'title': '欢迎关注',
        'description': '本公众号主要分享个人博客和汇总各大数据竞赛平台比赛信息'
    }

    news_competition = {
        'title':
        '一站式显示各大平台竞赛信息',
        'description':
        '一站式显示各大平台竞赛信息',
        'url':
        'https://mp.weixin.qq.com/mp/homepage?__biz=MzU0MjE2MzcxMA==&hid=1&sn=71e111a995a23fa891deebc66663c94a'
    }

    if request.method == "GET":
        message = Verify(request)
        message.verify()
        return message.return_code
    else:
        message = Reply(request)
        if message.msg_type == 'text':
            if '竞赛' in message.content:
                message.news([news_competition])
                return message.reply()

            message.text(message.content)
            return message.reply()
        elif message.msg_type == 'event':
            if message.event == 'subscribe':
                message.news([news_welcome, news_competition])
                return message.reply()


@bp.route('/update_list', methods=['GET'])
def update_list():
    update_competition()
    return 'everything is ok'
