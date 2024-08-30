# -*- codeing = utf-8 -*-
# 

# 2/18 17:06
# 
# @File: movieApi.py.py
# @Desc:
import json
import jieba
from flask_marshmallow import Marshmallow

from base.core import db
ma = Marshmallow()

# 这里定义的电影的模型，和数据库的映射关系
# 字段是和数据库一致的
class Movie(db.Model):
    __tablename__ = 'movies2'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    douban_id = db.Column(db.String(255))
    cover = db.Column(db.String(255))
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    douban_score = db.Column(db.DECIMAL)
    douban_votes = db.Column(db.Integer)
    directors = db.Column(db.String(255))
    actors = db.Column(db.String(255))
    year = db.Column(db.String(255))
    regions = db.Column(db.String(255))
    genres = db.Column(db.String(255))
    storyline = db.Column(db.String(255))  #
    release_date = db.Column(db.String(255))  #

# 定义Marchmallow封装json用的类
class MovieSchema(ma.Schema):
    class Meta:
        # fields = ('url','img','name')
        fields = ('id','douban_id','cover','name','alias','douban_score','douban_votes','directors','actors','year','regions','genres','storyline','release_date')

movie_schema = MovieSchema(many=True)

# jieba分词接口，用来分词， movieApi里的getWordCut方法会调用这个
def getWords():
    intros = db.session.query(Movie).all()
    text = ""
    for i in intros:
        # print(i.intro)  # 每一行
        if i.storyline is not None:
            text = text + i.storyline

    word_count = dict()
    words = jieba.cut(text)
    for word in words:
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1

    # 词频顺序进行排序，以元祖形式存储
    word_count_sorted = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    # print(word_count_sorted)

    # 过滤结果中的标点符号和单词
    word_count_sorted = filter(lambda x: len(x[0]) > 1, word_count_sorted)
    # print(word_count_sorted)

    # 元组转json
    result = json.dumps(dict(word_count_sorted), ensure_ascii=False)
    # result = json.dumps(dict(word_count_sorted), ensure_ascii=False)
    print(json.loads(result))
    result = json.loads(result)
    return result
