import pymysql

class News:
    type = ""
    title = ""
    url = ""

    def __init__(self, host, username, password, database):
        # 连接MySQL数据库
        self.conn = pymysql.connect(host=host, user=username, password=password, db=database)
        self.cursor = self.conn.cursor()

    def __del__(self):
        # 关闭数据库连接
        self.conn.close()

    # 根据请求的兴趣爱好，在news数据库中请求与type相匹配的url和title
    # 请求到的url和title放在两个列表中，传给主页的HTML
    # user_news = News("Localhost", "root", "123456", "news")
    # print(user_news.get_message("科技"))
    # print(user_news.get_message("体育"))

    def get_message(self, news_type):
        # 查询每个相同的type的url和title，放在两个列表中
        urls = []
        titles = []
        sql = "SELECT url, title FROM news WHERE type = %s"
        self.cursor.execute(sql, (news_type,))
        results = self.cursor.fetchall()
        for row in results:
            urls.append(row[0])
            titles.append(row[1])
        return urls, titles

    # 根据输入的url在news数据库中查找他的type
    # 用于后端在判断历史记录里面的新闻的种类，然后在推荐新闻
    def get_type(self, url):
        sql = "SELECT type FROM news WHERE url = %s"
        self.cursor.execute(sql, (url,))
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None

    # 写入数据的方法
    def insert_data(self, news_type, title, url):
        # 插入数据到news表中
        sql = "INSERT INTO news (type, title, url) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (news_type, title, url))
        self.conn.commit()



