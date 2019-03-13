# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-03-04 13:33:50
# @Last Modified time: 2019-03-13 11:17:45
from .. import db
import time


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, unique=True)
    num = db.Column(db.Integer)
    good_word = db.Column(db.String)
    bad_word = db.Column(db.String)
    bad_number = db.Column(db.String)
    owner_name = db.Column(db.String)
    owner_id = db.Column(db.Integer)
    update = db.Column(db.Integer)

    def __init__(self, room_id, num, good_word, bad_word, bad_number, owner_name, owner_id):
        self.room_id = room_id
        self.num = num
        self.good_word = good_word
        self.bad_word = bad_word
        self.bad_number = bad_number
        self.owner_name = owner_name
        self.owner_id = owner_id

        now = int(time.time())
        self.update = now
