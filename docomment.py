# -*- codeing = utf-8 -*-


# 4/17 17:26
# 
# @File: docomment.py
# @Desc: 批量对评论进行情感分析
import numpy as np
import sqlalchemy as sqla
import pandas as pd

from deeplearning.predict_lstm import sentimentalAnalysis_single

db=sqla.create_engine('mysql+pymysql://root:123456@127.0.0.1/flask_douban_comment?charset=utf8')

sql = 'select * from comments where douban_comment_id not in (select douban_comment_id from  comments2) limit 20000'
df = pd.read_sql(sql, con=db)
labels = pd.DataFrame('positive', index = df.index, columns = ['label'])
scores = pd.DataFrame(0, index = df.index, columns = ['score'])

# 方法一、使用单个接口 使用深度学习来进行运算
# for x in df.index:
#   datas = [df.loc[x, "content"]]
#   # print(datas)
#   result = sentimentalAnalysis_single(datas)
#   labels.loc[x, "label"] = result[0]['label']
#   scores.loc[x, "score"] = round(result[0]['prob'], 4)

# 方法二
# print(df["content"].values.tolist())
result = sentimentalAnalysis_single(df["content"].values.tolist())
result = pd.DataFrame.from_dict(result)
df_result = pd.concat([df,result['label'],result['prob'].round(4)], axis=1)
# print(result['label'])
# print(df_result)
# df_result = pd.concat([df,labels,scores], axis=1) #合并
df_result = df_result.drop(['id'], axis=1)
df_result.rename(columns={'prob':'score'},inplace=True)
print(df_result)
df_result.to_sql(name="comments2", con=db, if_exists='append', index=False)