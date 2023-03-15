
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# # 画图的主题设计
sns.set_theme()
sns.set_context('notebook')
#
# # 加载数据
# # 行为类型包括：浏览：pv,购买：buy，加购：cart，收藏：fav
data_user = pd.read_csv('E:/file/data_analysis/UserBehavior.csv',header=None,names=['user_id','goods_id','item_id','behavior','time'])
data_user.head(20)#查看表中前20行数据

# 查看数据集量级
print('整体数据的大小为',len(data_user))
print('数据集中用户数量是：',len(set(data_user['user_id'])))
print('数据集中商品数量是：',len(set(data_user['goods_id'])))
print('数据集中商品类别数量是：',len(set(data_user['item_id'])))

# 查看数据缺失情况
# data_user.isnull().sum()
#
# # 分割天(date)和小时(hour)
# data_user['date'] = data_user['time'].map(lambda x: x.split(' ')[0])
# data_user['hour'] = data_user['time'].map(lambda x: x.split(' ')[1])
# data_user.head()
#
# # 查看字段类型：
# data_user.dtypes
# #根据结果将原类型转换为方便处理的类型
# data_user['user_id'] = data_user['user_id'].astype('object')
# data_user['item_id'] = data_user['item_id'].astype('object')
# data_user['item_category'] = data_user['item_category'].astype('object')
# data_user['date'] = pd.to_datetime(data_user['date'])
# data_user['hour'] = data_user['hour'].astype('int64')

#数据分析 可视化
#首先从宏观流量分析开始
#1.基于天级别访问流量分析，包括访问量（PV）:刷新一次页面算一次访问和独立访问量（UV）：一个用户的所有访问量都只记录一次，属于SQL里的unique操作
#PV访问量
pv_daily = data_user.groupby('date')['user_id'].count()
pv_daily = pv_daily.reset_index()
pv_daily = pv_daily.rename(columns={'user_id':'pv_daily'})
#UV访问量
uv_daily = data_user.groupby('date')['user_id'].apply(lambda x: len(x.unique()))
uv_daily = uv_daily.reset_index()
uv_daily = uv_daily.rename(columns = {'user_id':'uv_daily'})
# 可视化
fig, axes = plt.subplots(2,1,sharex=True)
# pv_daily: pandas 对象
# Matplotlib, Pandas , histplot:  柱状图
pv_daily.plot(x='date', y='pv_daily', ax=axes[0], colormap='cividis')
uv_daily.plot(x='date', y='uv_daily', ax=axes[1], colormap='RdGy')
axes[0].set_title('pv_daily')
axes[1].set_title('uv_daily')
plt.show()


#基于小时级别访问流量
# 计算每小时的PV
pv_hour = data_user.groupby('hour')['user_id'].count()
pv_hour = pv_hour.reset_index()
pv_hour = pv_hour.rename(columns={'user_id':'pv_hour'})
# 计算每小时UV
uv_hour = data_user.groupby('hour')['user_id'].apply(lambda x: len(x.unique()))
uv_hour = uv_hour.reset_index()
uv_hour = uv_hour.rename(columns={'user_id':'uv_hour'})
# 可视化
fig, axes = plt.subplots(2,1,sharex=True)
pv_hour.plot(x='hour',y='pv_hour',ax=axes[0],colormap='cividis')
uv_hour.plot(x='hour', y='uv_hour', ax=axes[1],colormap='RdGy')
axes[0].set_title('pv_hour')
axes[1].set_title('uv_hour')
plt.show()
#根据以上趋势查看双十二当天基于小时的用户访问数据
data_user_1212 = data_user.loc[data_user['date']=='2017-12-12']
# 计算每小时的PV
pv_hour_1212 = data_user_1212.groupby('hour')['user_id'].count().reset_index().rename(columns={'user_id':'1212_pv_hour'})
uv_hour_1212 = data_user_1212.groupby('hour')['user_id'].apply(lambda x: len(x.unique())).reset_index().rename(columns={'user_id':'1212_uv_hour'})
#和30日总体的小时级别PV/UV变化趋势做对比：
fig, axes = plt.subplots(2,1,sharex=True)
pv_hour.plot(x='hour',y='pv_hour',ax=axes[0],colormap='cividis')
pv_hour_1212.plot(x='hour', y='1212_pv_hour', ax=axes[1],colormap='RdGy')
axes[0].set_title('pv_hour')
axes[1].set_title('pv_hour_1212')
# 可视化 UV
fig, axes = plt.subplots(2,1,sharex=True)
uv_hour.plot(x='hour',y='uv_hour',ax=axes[0],colormap='cividis')
uv_hour_1212.plot(x='hour', y='1212_uv_hour', ax=axes[1],colormap='RdGy')
axes[0].set_title('uv_hour')
axes[1].set_title('uv_hour_1212')
plt.show()

# 不同用户行为流量分析
# 一天当中（按照每小时）用户发生的行为
# 基于 behavior_type & hour 分组
# 点击、收藏、加购物车、支付四种行为，分别用数字1、2、3、4表示
pv_behavior = data_user.groupby(['behavior_type','hour'])['user_id'].count()
pv_behavior = pv_behavior.reset_index()
pv_behavior = pv_behavior.rename(columns={'user_id':'pv_behavior'})
# 可视化
# sns: serborn
ax = sns.lineplot(x='hour',y='pv_behavior',hue='behavior_type',data=pv_behavior)
# 因为浏览行为的占比太大，导致其他行为趋势不明显，去掉浏览行为后再看
sns.lineplot(x='hour',y='pv_behavior',hue='behavior_type',data=pv_behavior[pv_behavior.behavior_type!='pv'])
plt.show()

# 根据数据还能分析浏览-收藏/加购-购买转化率
behavior_type = data_user.groupby(['behavior_type'])['user_id'].count()
click_num, fav_num, add_num, pay_num = behavior_type['pv'], behavior_type['fav'], behavior_type['cart'], behavior_type['buy']
fav_add_num = fav_num + add_num
print('加购/收藏转化率：', 100 * fav_add_num / click_num)
print('点击 到 购买转化率: ', 100 * pay_num / click_num)
print('加购/收藏 到 购买转化率: ', 100 * pay_num / fav_add_num)
# 根据结果可以看出加购/收藏后购买转化率最大，接着分析双十二的转化率
data_user_1212 = data_user.loc[data_user['date']=='2014-12-12']
behavior_type = data_user_1212.groupby(['behavior_type'])['user_id'].count()

click_num, fav_num, add_num, pay_num = behavior_type['pv'], behavior_type['fav'], behavior_type['cart'], behavior_type['buy']
fav_add_num = fav_num + add_num
print('双十二 加购/收藏转化率：', 100 * fav_add_num / click_num)
print('双十二 点击 到 购买转化率: ', 100 * pay_num / click_num)
print('双十二 加购/收藏 到 购买转化率: ', 100 * pay_num / fav_add_num)
# 由结果可以看出双十二当天，加购/收藏 到 购买转化率是平时的2倍之多，作为商家来讲，可以考虑在特定节日推出特定主题的优惠活动，是个有效的促活、转化的方式

#用户价值分析：根据RFM分析模型探索用户价值
#1.用户购买频次分析
## 浏览 >> 加购/收藏 >> 购买（4）
data_user_buy = data_user[data_user.behavior_type=='buy'].groupby('user_id')['behavior_type'].count()
data_user_buy.plot(x='user_id',y='buy_count')

# 2.每日的收益在所有活跃用户中的转化:ARPU分析:每日消费总次数 / 每日活跃用户数
#给数据集中每一个用户赋值一个1，表示有登录操作
data_user['action'] = 1

# 得到 date, user_id, behavior_type和计算用户每日的登录次数
data_user_arpu = data_user.groupby(['date','user_id','behavior_type'])['action'].count()
data_user_arpu = data_user_arpu.reset_index()
# 计算arpu，近似公式： ARPU = 每日消费次数 / 每日活跃用户数
arpu = data_user_arpu.groupby('date').apply(lambda x:x[x['behavior_type']==4]['action'].sum() / len(x['user_id'].unique()) )
data_user_arpu.head(20)

# 可视化
arpu.plot(colormap='cividis')
plt.title('ARPU')
plt.show()

# 3.整个平台的用户消费的均值:ARPPU分析：总收入/活跃用户付费数量，该数据集中没有收益金额，将总收入转化为总的购买行为次数
# 计算每日的所有用户的购买次数
data_user_arppu = data_user[data_user['behavior_type']==4].groupby(['date','user_id'])['behavior_type'].count()
data_user_arppu = data_user_arppu.reset_index().rename(columns={'behavior_type':'buy_count'})
data_user_arppu.head()
# 计算ARPPU
data_user_arppu = data_user_arppu.groupby('date').apply(lambda x:x['buy_count'].sum() / x['user_id'].count())
# 可视化
data_user_arppu.plot(colormap='cividis')
plt.title('ARPPU')

# 4.复购情况分析
# 两天以上都在该平台产生了购买行为，一天多次的购买不算是复购。复购率 = 复购用户数量 / 有购买行为的用户数量
# 计算用户购买频次
data_user_pay = data_user[data_user.behavior_type==4]
# 基于date去重，得到的结果即为购物分布的天数：
data_user_pay = data_user_pay.groupby('user_id')['date'].apply(lambda x: len(x.unique()))
# 计算复购率：
repeat_buy_ratio = data_user_pay[data_user_pay > 1].count() / data_user_pay.count()
data_user['action'] = 1 # 对每一行的行为记为1次，通过对行为次数的相加，从而计算频次
data_user_buy = data_user[data_user.behavior_type == 4]
data_user_buy = data_user_buy.groupby(['user_id','date'])['action'].count()
data_user_buy = data_user_buy.reset_index()
data_user_buy.head(30)


# 除了复购率，复购周期也值得我们关注，知道用户多久复购一次，有助于淘宝产品宣传在这个时间间隔内采取策略，增加用户的复购意向，最终转化为实际收益。

# data_user = pd.read_excel('E:/file/data_analysis/data.xlsx',header=None,names=['user_id','goods_id','item_id','behavior','time'])

#数据预处理

# data_user['time'] = data_user.time.map(time.localtime).map(lambda x: time.strftime("%Y--%m--%d %H", x)).astype('datetime64')

# data_user['time']=data_user['time'].apply(lambda _:datetime.strptime(_,"%Y%m%d,%H"))
# print(data_user.info())
# print(data_user.head())
#
# timearray=time.localtime(1512140483)
# print(type(timearray))
# styleTime=time.strftime("%Y-%m-%d %H",timearray)
# print(type(styleTime))