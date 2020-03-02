from leancloud import Engine

from app.utils import update_competition
from run import app

engine = Engine(app)


@engine.define
def func_update_competition():
    update_competition()
