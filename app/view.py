import requests
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

    news_keyword = {
        'title': '关键词回复',
        'description': '回复 竞赛 查看各大竞赛平台竞赛信息,回复 新竞赛 查看今日上新竞赛'
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
            if '关键词' == message.content:
                message.news([news_keyword])
                return message.reply()
            elif '新竞赛' == message.content:
                response = requests.get(
                    'https://www.logicjake.xyz/MLCompetitionHub/new.json')
                new_completions = response.json()
                if len(new_completions) == 0:
                    news_blank = {
                        'title':
                        '暂无新比赛上线',
                        'description':
                        '暂无新比赛上线',
                        'url':
                        'https://www.logicjake.xyz/MLCompetitionHub/#/new_competition'
                    }
                    message.news([news_blank])
                    return message.reply()
                else:
                    ns = []
                    for c in new_completions:
                        ns.append({
                            'title': c['name'],
                            'description': c['description'],
                            'url': c['url']
                        })
                    message.news(ns)
                    return message.reply()
            elif '竞赛' == message.content:
                message.news([news_competition])
                return message.reply()

            message.text('我不明白')
            return message.reply()
        elif message.msg_type == 'event':
            if message.event == 'subscribe':
                message.news([news_welcome, news_keyword, news_competition])
                return message.reply()


@bp.route('/update_list', methods=['GET'])
def update_list():
    update_competition()
    return 'everything is ok'
