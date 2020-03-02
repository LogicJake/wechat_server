from lxml import etree


class Post():
    def __init__(self, req):
        self.xml = etree.fromstring(req.stream.read())
        self.msg_type = self.xml.find("MsgType").text
        self.to_user_name = self.xml.find("ToUserName").text
        self.from_user_name = self.xml.find("FromUserName").text
        self.create_time = self.xml.find("CreateTime").text
        self.msg_id = self.xml.find("MsgId").text

        hash_table = {
            'text': ['Content'],
            'image': ['PicUrl', 'MediaId'],
            'voice': ['MediaId', 'Format'],
            'video': ['MediaId', 'ThumbMediaId'],
            'shortvideo': ['MediaId', 'ThumbMediaId'],
            'location': ['Location_X', 'Location_Y', 'Scale', 'Label'],
            'link': ['Title', 'Description', 'Url'],
            'event': ['Event']
        }

        attributes = hash_table[self.msg_type]
        self.content = self.xml.find(
            "Content").text if 'Content' in attributes else '抱歉，暂未支持此消息。'
        self.pic_url = self.xml.find(
            "PicUrl").text if 'PicUrl' in attributes else '抱歉，暂未支持此消息。'
        self.media_id = self.xml.find(
            "MediaId").text if 'MediaId' in attributes else '抱歉，暂未支持此消息。'
        self.format = self.xml.find(
            "Format").text if 'Format' in attributes else '抱歉，暂未支持此消息。'
        self.thumb_media_id = self.xml.find(
            "ThumbMediaId"
        ).text if 'ThumbMediaId' in attributes else '抱歉，暂未支持此消息。'
        self.location_x = self.xml.find(
            "Location_X").text if 'Location_X' in attributes else '抱歉，暂未支持此消息。'
        self.location_y = self.xml.find(
            "Location_Y").text if 'Location_Y' in attributes else '抱歉，暂未支持此消息。'
        self.scale = self.xml.find(
            "Scale").text if 'Scale' in attributes else '抱歉，暂未支持此消息。'
        self.label = self.xml.find(
            "Label").text if 'Label' in attributes else '抱歉，暂未支持此消息。'
        self.title = self.xml.find(
            "Title").text if 'Title' in attributes else '抱歉，暂未支持此消息。'
        self.description = self.xml.find(
            "Description"
        ).text if 'Description' in attributes else '抱歉，暂未支持此消息。'
        self.url = self.xml.find(
            "Url").text if 'Url' in attributes else '抱歉，暂未支持此消息。'
        self.recognition = self.xml.find(
            "Recognition"
        ).text if 'Recognition' in attributes else '抱歉，暂未支持此消息。'
        self.event = self.xml.find(
            "Event").text if 'Event' in attributes else '抱歉，暂未支持此消息。'
