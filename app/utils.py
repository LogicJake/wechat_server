import json
import math
import os
from datetime import datetime, timedelta

import requests
from jinja2 import Environment, PackageLoader
from werkzeug.contrib.cache import SimpleCache

STANDARD_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+08:00'
fix_head_media = 'WvZIHWfBIDIy5AYZtBqmwfZYx2miG846tv1gh7wkUfo'
HEADERS = {'Content-Type': 'application/json'}


def get_all_exist_twsc(token):
    data = {"type": "news", "offset": 0, "count": 20}
    response = requests.post(
        'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={}'
        .format(token),
        data=json.dumps(data),
        headers=HEADERS)
    response.encoding = 'utf-8'
    total_count = response.json()['total_count']

    material_list = []
    pages = math.ceil(total_count / 20)
    for p in range(pages):
        data = {"type": "news", "offset": p * 20, "count": 20}
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={}'
            .format(token),
            data=json.dumps(data),
            headers=HEADERS)
        response.encoding = 'utf-8'
        material_list += response.json()['item']

    twsc_list = {}
    for material in material_list:
        media_id = material['media_id']
        title = material['content']['news_item'][0]['title']
        author = material['content']['news_item'][0]['author']
        content_source_url = material['content']['news_item'][0][
            'content_source_url']
        thumb_media_id = material['content']['news_item'][0]['thumb_media_id']
        show_cover_pic = material['content']['news_item'][0]['show_cover_pic']

        twsc_list[title] = {
            'media_id': media_id,
            'author': author,
            'content_source_url': content_source_url,
            'thumb_media_id': thumb_media_id,
            'show_cover_pic': show_cover_pic
        }

    return twsc_list

def get_all_exist_cgx(token):
    response = requests.post(
        'https://api.weixin.qq.com/cgi-bin/draft/count?access_token={}'
        .format(token),
        headers=HEADERS)
    response.encoding = 'utf-8'
    total_count = response.json()['total_count']

    draft_list = []
    pages = math.ceil(total_count / 20)
    for p in range(pages):
        data = {"offset": p * 20, "count": 20}
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={}'
            .format(token),
            data=json.dumps(data),
            headers=HEADERS)
        response.encoding = 'utf-8'
        draft_list += response.json()['item']

    cgx_list = {}
    for draft in draft_list:
        media_id = draft['media_id']
        title = draft['content']['news_item'][0]['title']
        author = draft['content']['news_item'][0]['author']
        content_source_url = draft['content']['news_item'][0][
            'content_source_url']
        thumb_media_id = draft['content']['news_item'][0]['thumb_media_id']
        show_cover_pic = draft['content']['news_item'][0]['show_cover_pic']

        cgx_list[title] = {
            'media_id': media_id,
            'author': author,
            'content_source_url': content_source_url,
            'thumb_media_id': thumb_media_id,
            'show_cover_pic': show_cover_pic
        }

    return cgx_list

def update_twsc_new(twsc_list, content, token):
    if '新上线比赛' not in twsc_list.keys():
        data = {
            "articles": [{
                "title":
                '新上线比赛',
                "thumb_media_id":
                fix_head_media,
                "author":
                'LogicJake',
                "show_cover_pic":
                0,
                "content":
                content,
                "content_source_url":
                'https://www.logicjake.xyz/MLCompetitionHub/#/new_competition'
            }]
        }
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/material/add_news?access_token={}'
            .format(token),
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers=HEADERS,
        )
        print(response.text)
    else:
        title = '新上线比赛'
        data = {
            'media_id': twsc_list[title]['media_id'],
            "index": 0,
            "articles": {
                "title": title,
                "thumb_media_id": fix_head_media,
                "author": twsc_list[title]['author'],
                "show_cover_pic": twsc_list[title]['show_cover_pic'],
                "content": content,
                "content_source_url":
                twsc_list[title]['content_source_url'],
            }
        }
        response = requests.post(
            ' https://api.weixin.qq.com/cgi-bin/material/update_news?access_token={}'
            .format(token),
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers=HEADERS,
        )
        print('更新', response.text)

def update_cgx_new(cgx_list, content, token):
    if '新上线比赛' not in cgx_list.keys():
        data = {
            "articles": [{
                "title":
                '新上线比赛',
                "thumb_media_id":
                fix_head_media,
                "author":
                'LogicJake',
                "content":
                content,
                "content_source_url":
                'https://www.logicjake.xyz/MLCompetitionHub/#/new_competition'
            }]
        }
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={}'
            .format(token),
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers=HEADERS,
        )
        print(response.text)
    else:
        title = '新上线比赛'
        data = {
            'media_id': cgx_list[title]['media_id'],
            "index": 0,
            "articles": {
                "title": title,
                "thumb_media_id": fix_head_media,
                "author": cgx_list[title]['author'],
                "show_cover_pic": cgx_list[title]['show_cover_pic'],
                "content": content,
                "content_source_url":
                cgx_list[title]['content_source_url'],
            }
        }
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/draft/update?access_token={}'
            .format(token),
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers=HEADERS,
        )
        print('更新', response.text)


def update_competition():
    token = get_token()
    env = Environment(loader=PackageLoader('app'))

    twsc_list = get_all_exist_twsc(token)
    cgx_list = get_all_exist_cgx(token)

    # 新上新比赛
    response = requests.get(
        'https://www.logicjake.xyz/MLCompetitionHub/new.json')
    new_completions = response.json()

    template = env.get_template('new_cp.j2')
    update = datetime.utcnow() + timedelta(hours=8)
    update = update.strftime(STANDARD_TIME_FORMAT)
    content = template.render(competitions=new_completions, update=update)
    
    update_twsc_new(twsc_list, content, token)
    update_twsc_new(cgx_list, content, token)

    print('更新新上线比赛结束')


def get_token():
    app_id = os.getenv('APP_ID')
    app_secret = os.getenv('APP_SECRET')
    cache = SimpleCache()

    token = cache.get('token')

    if token is None:
        print('没获取到token')

        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(
            app_id, app_secret)
        result = requests.get(url).text
        token = json.loads(result).get('access_token')
        cache.set('token', token, timeout=7000)

    return token
