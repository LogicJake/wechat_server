import hashlib
import os


class Message(object):
    def __init__(self, req):
        self.request = req
        self.token = os.getenv('TOKEN')
        self.app_id = os.getenv('APP_ID')
        self.app_secret = os.getenv('APP_SECRET')


class Verify(Message):
    def __init__(self, req):
        super(Verify, self).__init__(req)
        self.signature = req.args.get('signature')
        self.timestamp = req.args.get('timestamp')
        self.nonce = req.args.get('nonce')
        self.echostr = req.args.get('echostr')
        self.return_code = 'Invalid'

    def verify(self):
        data = sorted([self.token, self.timestamp, self.nonce])
        string = ''.join(data).encode('utf-8')
        hashcode = hashlib.sha1(string).hexdigest()
        if self.signature == hashcode:
            self.return_code = self.echostr
