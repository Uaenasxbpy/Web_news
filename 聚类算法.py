import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# 聚类算法实现
history = [
    [1, '政治'],
    [1, '科技'],
    [2, '科技'],
    [3, '体育'],
    [3, '体育'],
    [3, '科技'],
]
# 创建一个空字典，用于存储用户的类别访问次数
user_visits = {}

# 遍历历史记录表
for record in history:
    username = record[0]
    category = record[1]

    # 检查字典中是否已经存在该用户的记录
    if username not in user_visits:
        user_visits[username] = {}

    # 更新对应类别的访问次数
    if category not in user_visits[username]:
        user_visits[username][category] = 1
    else:
        user_visits[username][category] += 1

# 创建一个空的DataFrame来存储用户访问次数数据
user_visits_df = pd.DataFrame()

# 向DataFrame中添加用户的访问次数数据
for user_id, categories in user_visits.items():
    user_visits_df = user_visits_df.append(categories, ignore_index=True)

# 填充缺失值为0
user_visits_df.fillna(0, inplace=True)

# 将访问次数转换为特征向量
scaler = MinMaxScaler()
users_scaled = scaler.fit_transform(user_visits_df)

# 使用协同过滤算法计算用户之间的相似性
user_similarity = users_scaled.dot(users_scaled.T)

# 根据用户相似性计算相似用户聚类
def cluster_similar_users(users, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(users)
    labels = kmeans.labels_
    return labels

num_clusters = 3  # 设置聚类数量
labels = cluster_similar_users(user_similarity, num_clusters)

# 输出每个用户所属的聚类标签
for i, label in enumerate(labels):
    print(f"用户 {i+1} 的标签为: {label}")
