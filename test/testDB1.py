# -*- codeing = utf-8 -*-
# 

# 2/10 12:57
# 
# @File :testDB1.py
from sqlalchemy import create_engine
from base import DB_URI

# test文件夹内的文件都是写此程序时的测试代码，所以都可以删除，不影响本体Flask运行

engine = create_engine(DB_URI)  # 创建引擎
conn = engine.connect()  # 连接
result = conn.execute('SELECT 1')  # 执行SQL
print(result.fetchone())
conn.close()  # 关闭连接