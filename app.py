import json
import os
import random
import time

from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.sql import func

from api.alipayApi import payBp
from api.baiduApi import idocr
from api.movieApi import movieBp
from api.orderApi import orderBp
from base.code import ResponseCode
from base.core import JSONEncoder
from base.response import ResMsg
from api.testApi import bp
from api.userApi import userBp

import logging

from deeplearning.predict_lstm import sentimentalAnalysis_single
from models.movie import getWords

# Flask配置
from utils.smsutil import Sms

app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/test')
# 注册用户相关的方法
app.register_blueprint(userBp, url_prefix='/user')
# 注册电影相关的方法
app.register_blueprint(movieBp, url_prefix='/movie')
app.register_blueprint(payBp, url_prefix='/alipay')
app.register_blueprint(orderBp, url_prefix='/order')  # 订单接口

# 数据库配置信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/flask_douban_comment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 前端返回的JSON用ASCII编码关闭，否则浏览器里面看到的文本会是乱码
app.config['JSON_AS_ASCII'] = False
# Flask必须的配置
app.config['SECRET_KEY'] = 'KJDFLSjfldskj'


UPLOAD_FOLDER="upload"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','gif','GIF'])

# 日志系统配置
# handler = logging.FileHandler('./error.log', encoding='UTF-8')
# logging_format = logging.Formatter(
#             '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
# handler.setFormatter(logging_format)
# app.logger.addHandler(handler)

# 返回json格式转换 使用这个的话就不需要每次都写json返回了，简化代码
app.json_encoder = JSONEncoder

# SQLAlchemy 为ORM框架，即用来简化操作数据库的包，具体内容需要学习ORM相关知识
db = SQLAlchemy(app)
# Marshmallow 是用来封装返回SQLAlchemy 的返回结果的，通过这个包可以直接把数据转成JSON，从而返回给前端使用
ma = Marshmallow(app)

# 一个测试的方法，可以测试服务器是否启动了
@app.route('/test')
def test():  # put application's code here
    res = ResMsg()
    test_dict = dict(name="zhang", age=19)
    res.update(data=test_dict, code=0)
    # data = dict(code=ResponseCode.SUCCESS,
    #             msg=ResponseMessage.SUCCESS,
    #             data=test_dict)
    return res.data
    # return jsonify(res.data)

# 用来捕捉服务器运行过程中的500-内部错误，并给前端返回信息
@app.errorhandler(500)
def special_exception_handler(error):
    app.logger.error(error)
    return '请联系管理员', 500

#判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/file/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    res = ResMsg()
    file_dir=os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']
    if f and allowed_file(f.filename):
        fname = f.filename
        # fname = secure_filename(f.filename)
        print(fname)
        ext = fname.rsplit('.', 1)[1]
        unix_time = int(time.time())
        new_filename = str(unix_time)+'.'+ext
        f.save(os.path.join(file_dir, new_filename))
    res.update(data=new_filename, code=0)
    return res.data

@app.route('/file/idocr', methods=['POST'], strict_slashes=False)
def api_id_ocr():
    res = ResMsg()
    file_dir=os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']
    if f and allowed_file(f.filename):
        fname = f.filename
        # fname = secure_filename(f.filename)  有中文这个会有问题
        # print(fname)
        ext = fname.rsplit('.', 1)[1]
        unix_time = int(time.time())
        new_filename = str(unix_time)+'.'+ext
        f.save(os.path.join(file_dir, new_filename))
        current_path = os.path.dirname(__file__)

        idno, name = idocr(current_path + '/upload/' + new_filename)
    res.update(data=dict(idno=idno,pic=new_filename,name=name), code=0)
    return res.data

@app.route('/file/download/<filename>/')
def api_download(filename):
    # print('下载..' + filename)
    return send_from_directory('upload', filename, as_attachment=False)

#阿里云短信接口
# @app.route('/sms/sendSms', methods=['POST'])
# def sendSms():
#     res = ResMsg()
#     phone = request.json['phone']
#     code = random.randint(100000, 999999)
#     response = json.loads(Sms().sendCode(phone, code))
#     if response['Code'] == "OK":
#         res.update(msg="发送成功", code=0, data=code)
#     else:
#         res.update(msg="发送失败", code=-1)
#     return res.data

# 深度学习情感分析接口
@app.route('/deeplearning/senti_single', methods=['POST'])
def senti_single():
    res = ResMsg()
    data = request.json['data']
    datas = [data]
    print(datas)
    result = sentimentalAnalysis_single(datas)
    res.update(msg="成功", code=0, data=result)
    return res.data

if __name__ == '__main__':
    app.run(debug=True,host='172.0.0.1',port=8081)
