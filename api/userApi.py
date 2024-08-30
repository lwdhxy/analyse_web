# -*- codeing = utf-8 -*-
# 

# 2/16 11:23
# 
# @File :userApi.py
# #Desc :这个是用户接口的文件
import json

from flask import Blueprint, request, flash, session, jsonify

from base.code import ResponseCode, ResponseMessage
from base.response import ResMsg
from base.core import db
from models.model import valid_login, valid_register, User, user_schema

userBp = Blueprint("user", __name__)

# 前端用来获取用户信息的接口
@userBp.route( '/userinfo', methods=["POST"])
def userinfo():
    res = ResMsg()
    username = request.json['username']
    user = User.query.filter(User.username == username).first()
    print(user)
    # data = dict(zip(user.keys(), user))
    data = user_schema.dump(user)
    res.update(code=ResponseCode.SUCCESS, data=data)
    return res.data

@userBp.route( '/get/<id>', methods=["GET"])
def get(id):
    res = ResMsg()
    user = User.query.filter(User.id == id).first()
    print(user)
    data = user_schema.dump(user)
    res.update(code=ResponseCode.SUCCESS, data=data)
    return res.data

# 登录接口，验证用户名和密码
@userBp.route( '/login', methods=["POST"])
def login():
    res = ResMsg()
    username = request.json['username']
    password = request.json['password']
    if valid_login(username, password):
        # flash(username + "登录成功")
        session['username'] = username
        userId = db.session.query(User.id).filter(User.username==username).first()
        # print(userId)
        res.update(code=ResponseCode.SUCCESS,msg=ResponseMessage.SUCCESS,data=userId[0])
    else:
        res.update(code=ResponseCode.ACCOUNT_OR_PASS_WORD_ERR,msg=ResponseMessage.ACCOUNT_OR_PASS_WORD_ERR)
    return res.data

# 注销接口，清除session中的用户名
@userBp.route( '/logout')
def logout():
    res = ResMsg()
    session.pop('username', None)
    return res.data

# 用户注册接口，前端提供表单给这个接口后完成注册，会验证用户名是否存在
@userBp.route('/register', methods=["POST"])
def register():
    res = ResMsg()
    username = request.json['username']
    password = request.json['password']
    realname = request.json['realname']
    if valid_register(username):
        user = User(username=username, password=password, realname=realname)
        db.session.add(user)
        db.session.commit()
        res.update(code=ResponseCode.SUCCESS)
    else:
        res.update(code=ResponseCode.USERNAME_ALREADY_EXIST, msg=ResponseMessage.USERNAME_ALREADY_EXIST)
    return res.data

@userBp.route('/idconfirm', methods=["POST"])
def idconfirm():
    res = ResMsg()
    id = request.json['id']
    idno = request.json['idno']
    realname = request.json['realname']
    db.session.query(User).filter(User.id == id).update({"idno": idno, "realname": realname})
    db.session.commit()
    res.update(code=ResponseCode.SUCCESS)
    return res.data

@userBp.route('/update', methods=["POST"])
def update():
    res = ResMsg()
    try:
        data = request.json
        user_id = data['id']
        realname = data.get('realname', None)
        phone = data.get('phone', None)
        email = data.get('email', None)
        avatar = data.get('avatar', None)
        intro = data.get('intro', None)
        addr = data.get('addr', None)
        age = data.get('age', None)

        user = User.query.get(user_id)
        if user:
            # 更新用户信息，只有提供值的字段才会被更新
            user.realname = realname if realname is not None else user.realname
            user.phone = phone if phone is not None else user.phone
            user.email = email if email is not None else user.email
            user.avatar = avatar if avatar is not None else user.avatar
            user.intro = intro if intro is not None else user.intro
            user.addr = addr if addr is not None else user.addr
            user.age = age if age is not None else user.age

            db.session.commit()
            res.update(code=ResponseCode.SUCCESS, msg="用户信息更新成功")
        else:
            res.update(code=ResponseCode.USER_NOT_EXIST, msg="用户不存在")
    except Exception as e:
        db.session.rollback()
        res.update(code=ResponseCode.FAILURE, msg=str(e))
    return res.data

@userBp.route('/modifypass', methods=["POST"])
def modifypass():
    res = ResMsg()
    id = request.json['id']
    password = request.json['password']
    db.session.query(User).filter(User.id == id).update({"password": password})
    db.session.commit()
    res.update(code=ResponseCode.SUCCESS)
    return res.data

@userBp.route('/list', methods=["GET"])
def get_user_list():
    res = ResMsg()
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    keyword = request.args.get('keyword', '')

    query = User.query
    if keyword:
        query = query.filter(User.username.like(f'%{keyword}%'))

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    users = pagination.items
    total = pagination.total

    data = user_schema.dump(users, many=True)
    res.update(code=ResponseCode.SUCCESS, data={
        'items': data,
        'total': total
    })
    return res.data


@userBp.route('/add', methods=["POST"])
def add_user():
    res = ResMsg()
    try:
        username = request.json['username']
        password = request.json['password']
        realname = request.json.get('realname', '')
        email = request.json.get('email', '')
        age = request.json.get('age', None)
        addr = request.json.get('addr', '')

        if valid_register(username):
            user = User(username=username, password=password, realname=realname,
                        email=email, age=age, addr=addr)
            db.session.add(user)
            db.session.commit()
            res.update(code=ResponseCode.SUCCESS, msg="用户添加成功")
        else:
            res.update(code=ResponseCode.USERNAME_ALREADY_EXIST, msg=ResponseMessage.USERNAME_ALREADY_EXIST)
    except Exception as e:
        db.session.rollback()
        res.update(code=ResponseCode.FAILURE, msg=str(e))
    return res.data


@userBp.route('/delete/<int:id>', methods=["DELETE"])
def delete_user(id):
    res = ResMsg()
    try:
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            res.update(code=ResponseCode.SUCCESS, msg="用户删除成功")
        else:
            res.update(code=ResponseCode.USER_NOT_EXIST, msg="用户不存在")
    except Exception as e:
        db.session.rollback()
        res.update(code=ResponseCode.FAILURE, msg=str(e))
    return res.data


# 重置密码
@userBp.route('/reset_password', methods=["POST"])
def reset_password():
    res = ResMsg()
    try:
        id = request.json['id']
        user = User.query.get(id)
        if user:
            user.password = '123456'
            db.session.commit()
            res.update(code=ResponseCode.SUCCESS, msg="密码重置成功")
        else:
            res.update(code=ResponseCode.USER_NOT_EXIST, msg="用户不存在")
    except Exception as e:
        db.session.rollback()
        res.update(code=ResponseCode.FAILURE, msg=str(e))
    return res.data

# 这个函数非常关键，由于数据库的连接数是有限的，所以在操作完之后，一定要关闭db连接
# 这个方法可以在请求完之后自动关闭连接，这样就不需要每个接口里手动写关闭连接接口
@userBp.after_request
def close_session(response):
    db.session.close()
    return response
