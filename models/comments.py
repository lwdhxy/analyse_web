# -*- codeing = utf-8 -*-
# 

# 4/18 20:06
# 
# @File: comments.py
# @Desc:
import json
from flask_marshmallow import Marshmallow

from base.core import db
ma = Marshmallow()

# 这里定义的电影评论的模型，和数据库的映射关系
# 字段是和数据库一致的
class Comment(db.Model):
    __tablename__ = 'comments2'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    douban_id = db.Column(db.Integer)
    douban_user_nickname = db.Column(db.String(255))
    douban_user_avatar = db.Column(db.String(255))
    douban_user_url = db.Column(db.String(255))
    content = db.Column(db.TEXT)  #本文类型
    votes = db.Column(db.Integer)
    rating = db.Column(db.String(255))
    label = db.Column(db.String(255))
    score = db.Column(db.String(255))
    comment_time =  db.Column(db.TIMESTAMP(True), nullable=False)

# 定义Marchmallow封装json用的类
class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id','douban_id','douban_user_nickname','douban_user_avatar', \
                  'douban_user_url','content','votes','rating','label','score', \
                  'comment_time')

comment_schema = CommentSchema(many=True)
