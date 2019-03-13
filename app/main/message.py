# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-03-12 12:13:01
# @Last Modified time: 2019-03-12 12:25:42
import os
import requests


def send_message(chat_id, text):
    token = os.getenv('TOKEN')

    url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(
        token, chat_id, text)

    requests.get(url)
