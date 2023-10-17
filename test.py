import jieba

# 使用jieba提取关键词进行类别分析，然后返回type
def get_top_keywords(file_path, num_keywords = 1):
    # 排除词汇库
    excludes = {"on", "the", "of", "and", "in"}
    txt = open(file_path, "r", encoding="utf-8").read()
    words = jieba.lcut(txt)
    # 删除无意义的字
    words = [word for word in words if word not in excludes]
    # 统计词频
    word_counts = {}
    for word in words:
        if len(word) == 1:
            continue
        else:
            word_counts[word] = word_counts.get(word, 0) + 1
    # 按照频次进行排序
    sorted_keywords = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    # 获取出现次数最多的词汇
    top_keywords = [word for word, _ in sorted_keywords[:num_keywords]]
    print(top_keywords)
    # 进行分类处理
    type = classify(top_keywords)
    return type

# 用出现次数最多的关键词分析类别
def classify(keywords):
    # 定义类别关键词
    sports_keywords = ["体育", "运动"]
    politics_keywords = ["政治", "党派"]
    entertainment_keywords = ["娱乐", "明星"]
    economy_keywords = ["经济", "金融"]
    technology_keywords = ["科技", "技术","安全"]

    # 统计关键词出现次数
    sports_count = sum(keyword in sports_keywords for keyword in keywords)
    politics_count = sum(keyword in politics_keywords for keyword in keywords)
    entertainment_count = sum(keyword in entertainment_keywords for keyword in keywords)
    economy_count = sum(keyword in economy_keywords for keyword in keywords)
    technology_count = sum(keyword in technology_keywords for keyword in keywords)

    # 比较关键词出现次数，进行分类
    counts = [sports_count, politics_count, entertainment_count, economy_count, technology_count]
    category_index = counts.index(max(counts))

    # 分类对应的标签
    categories = ["体育", "政治", "娱乐", "经济", "科技"]
    category = categories[category_index]
    # 返回分析出来的类别
    return category

print(get_top_keywords("测试.txt"))