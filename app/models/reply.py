# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-03-13 20:07:16
# @Last Modified time: 2019-03-13 20:34:55
import time
from app.models.post import Post
from flask import make_response


class Reply(Post):

    def __init__(self, req):
        super(Reply, self).__init__(req)
        self.xml = '<xml><ToUserName><![CDATA[{}]]></ToUserName>' \
            '<FromUserName><![CDATA[{}]]></FromUserName>' \
            '<CreateTime>{}</CreateTime>'.format(
                self.from_user_name, self.to_user_name, str(int(time.time())))

    def text(self, Content):
        self.xml += '<MsgType><![CDATA[text]]></MsgType>' \
            '<Content><![CDATA[{}]]></Content></xml>'.format(Content)

    def image(self, MediaId):
        pass

    def voice(self, MediaId):
        pass

    def video(self, MediaId, Title, Description):
        pass

    def music(self, ThumbMediaId, Title='', Description='', MusicURL='', HQMusicUrl=''):
        pass

    def reply(self):
        response = make_response(self.xml)
        response.content_type = 'application/xml'
        return response
