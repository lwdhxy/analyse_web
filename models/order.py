# -*- codeing = utf-8 -*-
# Author: MiniBigData

# 3/21 11:28
# 
# @File :order.py
from flask_marshmallow import Marshmallow
from sqlalchemy import and_

from base.core import db
ma = Marshmallow()

class Order(db.Model):
    __tablename__ = 'tb_order'
    id = db.Column(db.String(36), primary_key=True)
    group_id = db.Column(db.Integer)  #
    user_id = db.Column(db.Integer)  # 用户ID
    reason = db.Column(db.String(512))
    type = db.Column(db.String(20))  # 类型
    remark = db.Column(db.String(512))
    amount = db.Column(db.DECIMAL)
    status = db.Column(db.Integer)
    deleted = db.Column(db.Integer)
    phone = db.Column(db.String(200))
    create_time = db.Column(db.String(50))
    update_time = db.Column(db.String(50))
    oid = db.Column(db.Integer)  # 关联ID

    def __repr__(self):
        return '<Order %r>' % self.id

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id','group_id','user_id','reason','type','remark','amount','status','deleted','create_time','update_time','phone','oid')
        # fields = ('id','username','age','realname')

order_schema = OrderSchema(many=False)
############################################
# 辅助函数、装饰器
############################################

