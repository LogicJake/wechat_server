from gevent import monkey
monkey.patch_all()
import gevent

import os

import leancloud

from run import app
from cloud import engine
dotenv_path = '.env'
if os.path.exists(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)

APP_ID = os.environ['LEANCLOUD_APP_ID']
APP_KEY = os.environ['LEANCLOUD_APP_KEY']
MASTER_KEY = os.environ['LEANCLOUD_APP_MASTER_KEY']
PORT = int(os.environ['LEANCLOUD_APP_PORT'])

leancloud.init(APP_ID, app_key=APP_KEY, master_key=MASTER_KEY)
leancloud.use_master_key(False)

application = engine

if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    from gevent.pywsgi import WSGIServer
    from werkzeug.serving import run_with_reloader
    from werkzeug.debug import DebuggedApplication

    @run_with_reloader
    def run():
        global application
        app.debug = True
        application = DebuggedApplication(application, evalex=True)
        server = WSGIServer(('0.0.0.0', PORT), application)
        server.serve_forever()

    run()
