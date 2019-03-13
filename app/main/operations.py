# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-03-09 15:47:02
# @Last Modified time: 2019-03-13 17:07:46
from app import db
import time
from app.models.room import Room
from app.models.member import Member
import os
from random import choice, sample
from app.main.message import send_message


def init_room(num, uid, user_name, good_word=None, bad_word=None):
    delete_room()
    if num < 4:
        send_message(uid, '不能少于4个人')
        return
    elif num > 13:
        send_message(uid, '不能多于13个人')
        return

    exist_room = Room.query.filter_by(owner_id=uid).all()

    if len(exist_room) != 0:
        for room in exist_room:
            db.session.delete(room)
            db.session.commit()

    if good_word is None and bad_word is None:
        words_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'words.txt')

        with open(words_path, 'r') as f:
            lines = f.readlines()
            line_sample = sample(lines, 1)[0].strip()
            good_word, bad_word = line_sample.split(' ')

    records = Room.query.all()

    exist_room_ids = [record.room_id for record in records]
    rows = int(os.getenv('ROWS'))
    all_room_ids = range(rows)
    ok_room_ids = list(set(all_room_ids) - set(exist_room_ids))
    room_id = choice(ok_room_ids)

    bad_num = 0
    if num < 7:
        bad_num = 1
    elif num >= 7:
        bad_num = 2

    bad_number = sample(range(num), bad_num)
    bad_number = [str(n + 1) for n in bad_number]
    str_bad_number = ','.join(bad_number)

    new_room = Room(room_id, num, good_word, bad_word,
                    str_bad_number, user_name, uid)
    db.session.add(new_room)
    db.session.commit()

    message = wrap_new_message(room_id, bad_num, num,
                               bad_word, good_word, bad_number)
    send_message(uid, message)


def enter_room(room_id, uid):
    delete_room()
    exist_room = Room.query.filter_by(room_id=room_id).first()
    if exist_room is None:
        send_message(uid, '房间不存在，请法官重新建房。')
        return

    room_owner = exist_room.owner_name
    owner_id = exist_room.owner_id
    num = exist_room.num
    bad_number = exist_room.bad_number
    bad_number = bad_number.split(',')
    bad_num = len(bad_number)
    good_word = exist_room.good_word
    bad_word = exist_room.bad_word

    if uid == owner_id:
        send_message(uid, '法官凑什么热闹。')
        return

    has_come = Member.query.filter_by(room_id=room_id, uid=uid).first()
    if has_come is not None:
        your_number = has_come.index
        if str(your_number) in bad_number:
            word = bad_word
        else:
            word = good_word
        message = wrap_enter_message(
            room_id, room_owner, word, has_come.index, bad_num, num)
        send_message(uid, message)
        return

    member = Member(room_id, uid)
    db.session.add(member)
    db.session.commit()

    room_members = Member.query.filter_by(room_id=room_id).all()
    room_members = sorted(room_members, key=lambda x: x.enter_time)

    index = -1
    for i, m in enumerate(room_members):
        if m.uid == uid:
            index = i
    if index >= num:
        db.session.delete(room_members[index])
        db.session.commit()
        send_message(uid, '房间人数已满')
        return

    your_number = str(index + 1)
    if your_number in bad_number:
        word = bad_word
    else:
        word = good_word
    member.index = your_number
    db.session.add(member)
    db.session.commit()
    message = wrap_enter_message(
        room_id, room_owner, word, your_number, bad_num, num)
    send_message(uid, message)


def update_room(uid, good_word=None, bad_word=None):
    delete_room()
    exist_room = Room.query.filter_by(owner_id=uid).first()

    if exist_room is None:
        send_message(uid, '请先创建房间')
        return

    if good_word is None and bad_word is None:
        words_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'words.txt')

        with open(words_path, 'r') as f:
            lines = f.readlines()
            line_sample = sample(lines, 1)[0].strip()
            good_word, bad_word = line_sample.split(' ')

    num = exist_room.num
    room_id = exist_room.room_id
    bad_num = 0
    if num < 7:
        bad_num = 1
    elif num >= 7:
        bad_num = 2

    bad_number = sample(range(num), bad_num)
    bad_number = [str(n + 1) for n in bad_number]
    str_bad_number = ','.join(bad_number)

    now = int(time.time())
    exist_room.update = now
    exist_room.good_word = good_word
    exist_room.bad_word = bad_word
    exist_room.bad_number = str_bad_number
    db.session.add(exist_room)
    db.session.commit()

    message = wrap_update_message(room_id, bad_num, num,
                                  bad_word, good_word, bad_number)
    send_message(uid, message)


def delete_room():
    rooms = Room.query.all()
    rooms = sorted(rooms, key=lambda x: x.update)

    outdate = int(time.time()) - 30 * 60
    for room in rooms:
        if room.update <= outdate:
            members = Member.query.filter_by(room_id=room.room_id).all()
            for member in members:
                db.session.delete(member)
                db.session.commit()
            db.session.delete(room)
            db.session.commit()
        else:
            break


def wrap_update_message(room_id, bad_num, num, bad_word, good_word, bad_number):
    bad_people = [n + '号' for n in bad_number]
    bad_people = '，'.join(bad_people)

    message = '换词成功！您是法官，请让参与游戏的玩家对我回复【/enter {}】更新自己的词语。\n\n房  号：{}\n配  置：{}个卧底，{}个平民\n卧底词：{}\n平民词：{}\n卧  底：{}\n\n回复【/change】，换一组词；回复【/change 平民词 卧底词】，自己出题。（一局结束后，不必重新建房，回复【/change】直接换词。半小时内无操作的房间将被删除）'.\
        format(room_id, room_id, bad_num, num -
               bad_num, bad_word, good_word, bad_people)
    return message


def wrap_new_message(room_id, bad_num, num, bad_word, good_word, bad_number):
    bad_people = [n + '号' for n in bad_number]
    bad_people = '，'.join(bad_people)

    message = '建房成功！您是法官，请让参与游戏的玩家对我回复【/enter {}】进入房间。\n\n房  号：{}\n配  置：{}个卧底，{}个平民\n卧底词：{}\n平民词：{}\n卧  底：{}\n\n回复【/change】，换一组词；回复【/change 平民词 卧底词】，自己出题。（一局结束后，不必重新建房，回复【/change】直接换词。半小时内无操作的房间将被删除）'.\
        format(room_id, room_id, bad_num, num -
               bad_num, bad_word, good_word, bad_people)
    return message


def wrap_enter_message(room_id, room_owner, word, number, bad_num, num):
    message = '房  号：{}\n房  主：{}\n词  语：{}\n你  是：{}号\n配  置：{}个卧底，{}个平民'\
        .format(room_id, room_owner, word, number, bad_num, num - bad_num)
    return message
