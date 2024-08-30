# -*- codeing = utf-8 -*-
# 

# 2/10 12:57
# 
# @File :testDB1.py
from testDB2 import save
from testDB2 import Tour

tour = Tour(name='圆通寺')  # 创建一个tour对象
save(tour)  # 添加到session


