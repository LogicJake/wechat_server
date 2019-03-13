# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-03-13 20:07:16
# @Last Modified time: 2019-03-13 20:09:05
from app.models.post import Post


class Reply(Post):

    def __init__(self, req):
        self.xml = f'<xml><ToUserName><![CDATA[{self.FromUserName}]]></ToUserName>' \
            f'<FromUserName><![CDATA[{self.ToUserName}]]></FromUserName>' \
            f'<CreateTime>{str(int(time.time()))}</CreateTime>'

    def text(self, Content):
        self.xml += f'<MsgType><![CDATA[text]]></MsgType>' \
            f'<Content><![CDATA[{Content}]]></Content></xml>'

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
