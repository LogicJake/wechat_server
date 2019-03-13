# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-03-12 13:32:00
# @Last Modified time: 2019-03-13 20:50:43
from .. import db
import time


class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey(
        'room.room_id', ondelete="CASCADE"))
    index = db.Column(db.Integer)
    uid = db.Column(db.String)
    enter_time = db.Column(db.Integer)

    def __init__(self, room_id, uid):
        self.room_id = room_id
        self.uid = uid

        now = int(time.time())
        self.enter_time = now
