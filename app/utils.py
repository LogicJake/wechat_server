import json
import math
import os
from datetime import datetime, timedelta

import requests
from jinja2 import Environment, PackageLoader
from werkzeug.contrib.cache import SimpleCache

STANDARD_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+08:00'
fix_head_media = 'WvZIHWfBIDIy5AYZtBqmwfZYx2miG846tv1gh7wkUfo'


def update_competition():
    token = get_token()

    # 各平台比赛信息
    response = requests.get(
        'https://www.logicjake.xyz/MLCompetitionHub/all.json')
    plateforms = response.json()

    headers = {'Content-Type': 'application/json'}
    data = {"type": "news", "offset": 0, "count": 20}
    response = requests.post(
        'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={}'
        .format(token),
        data=json.dumps(data),
        headers=headers)
    response.encoding = 'utf-8'
    total_count = response.json()['total_count']

    news_list = []
    pages = math.ceil(total_count / 20)
    for p in range(pages):
        data = {"type": "news", "offset": p * 20, "count": 20}
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={}'
            .format(token),
            data=json.dumps(data),
            headers=headers)
        response.encoding = 'utf-8'
        news_list += response.json()['item']

    ids = []
    simle_news_list = {}
    for news in news_list:
        media_id = news['media_id']
        ids.append(media_id)
        title = news['content']['news_item'][0]['title']
        author = news['content']['news_item'][0]['author']
        content_source_url = news['content']['news_item'][0][
            'content_source_url']
        thumb_media_id = news['content']['news_item'][0]['thumb_media_id']
        show_cover_pic = news['content']['news_item'][0]['show_cover_pic']

        simle_news_list[title] = {
            'media_id': media_id,
            'author': author,
            'content_source_url': content_source_url,
            'thumb_media_id': thumb_media_id,
            'show_cover_pic': show_cover_pic
        }

    print('总素材数量: ', len(set(ids)))
    env = Environment(loader=PackageLoader('app'))
    template = env.get_template('plateform.j2')

    for plateform in plateforms:
        name = plateform['name']
        completions = plateform['competitions']
        update = datetime.utcnow() + timedelta(hours=8)
        update = update.strftime(STANDARD_TIME_FORMAT)
        content = template.render(competitions=completions,
                                  name=name,
                                  update=update)

        if '{}进行中的比赛'.format(name) not in simle_news_list.keys():
            data = {
                "articles": [{
                    "title":
                    '{}进行中的比赛'.format(name),
                    "thumb_media_id":
                    fix_head_media,
                    "author":
                    'LogicJake',
                    "show_cover_pic":
                    0,
                    "content":
                    content,
                    "content_source_url":
                    'https://www.logicjake.xyz/MLCompetitionHub/#/competition/{}'
                    .format(name.replace(' ', '_'))
                }]
            }
            response = requests.post(
                'https://api.weixin.qq.com/cgi-bin/material/add_news?access_token={}'
                .format(token),
                data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                headers=headers,
            )
            print(response.text)
        else:
            title = '{}进行中的比赛'.format(name)
            # 更新素材
            data = {
                'media_id': simle_news_list[title]['media_id'],
                "index": 0,
                "articles": {
                    "title":
                    title,
                    "thumb_media_id":
                    fix_head_media,
                    "author":
                    simle_news_list[title]['author'],
                    "show_cover_pic":
                    simle_news_list[title]['show_cover_pic'],
                    "content":
                    content,
                    "content_source_url":
                    simle_news_list[title]['content_source_url'],
                }
            }
            response = requests.post(
                ' https://api.weixin.qq.com/cgi-bin/material/update_news?access_token={}'
                .format(token),
                data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                headers=headers,
            )
            print('更新', response.text)
    print('更新各大平台结束')

    # 新上新比赛
    response = requests.get(
        'https://www.logicjake.xyz/MLCompetitionHub/new.json')
    new_completions = response.json()

    template = env.get_template('new_cp.j2')
    content = template.render(competitions=new_completions, update=update)
    if '新上线比赛' not in simle_news_list.keys():
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
            headers=headers,
        )
        print(response.text)
    else:
        title = '新上线比赛'
        data = {
            'media_id': simle_news_list[title]['media_id'],
            "index": 0,
            "articles": {
                "title": title,
                "thumb_media_id": fix_head_media,
                "author": simle_news_list[title]['author'],
                "show_cover_pic": simle_news_list[title]['show_cover_pic'],
                "content": content,
                "content_source_url":
                simle_news_list[title]['content_source_url'],
            }
        }
        response = requests.post(
            ' https://api.weixin.qq.com/cgi-bin/material/update_news?access_token={}'
            .format(token),
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers=headers,
        )
        print('更新', response.text)
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
