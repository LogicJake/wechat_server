import time

from flask import make_response
from jinja2 import Environment, PackageLoader

from app.models.post import Post


class Reply(Post):
    def __init__(self, req):
        super(Reply, self).__init__(req)
        self.xml = '<xml><ToUserName><![CDATA[{}]]></ToUserName>' \
            '<FromUserName><![CDATA[{}]]></FromUserName>' \
            '<CreateTime>{}</CreateTime>'.format(
                self.from_user_name, self.to_user_name, str(int(time.time())))

    def text(self, content):
        env = Environment(loader=PackageLoader('app'))
        template = env.get_template('reply_text.j2')
        text_xml = template.render(content=content)

        self.xml += text_xml

    def image(self, MediaId):
        pass

    def voice(self, MediaId):
        pass

    def video(self, MediaId, Title, Description):
        pass

    def music(self,
              ThumbMediaId,
              Title='',
              Description='',
              MusicURL='',
              HQMusicUrl=''):
        pass

    def news(self, newss):
        env = Environment(loader=PackageLoader('app'))
        template = env.get_template('reply_news.j2')
        news_xml = template.render(newss=newss)
        self.xml += news_xml

    def reply(self):
        response = make_response(self.xml)
        response.content_type = 'application/xml'
        return response
