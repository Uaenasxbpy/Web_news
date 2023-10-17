import pymysql
class Users:
    def __init__(self, host, username, password, database):
        # 连接MySQL数据库
        self.conn = pymysql.connect(host=host, user=username, password=password, db=database)
        self.cursor = self.conn.cursor()

    def __del__(self):
        # 关闭数据库连接
        self.conn.close()

    def get_usernames(self):
        """
        查询所有用户名
        :return:
        """
        query = "SELECT username FROM users"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return [row[0] for row in result]

    def get_interests(self, username):
        """
        查询给定用户名的兴趣爱好
        :param username:
        :return:
        """
        query = "SELECT interests FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        if result:
            # 如果结果不为空，则将逗号分隔的字符串转换为列表并返回
            interests = result[0].split(",")
            return interests
        else:
            # 如果结果为空，则返回None
            return None

    def get_user_interests(self):
        """
        返回用户名和兴趣爱好的字典
        :return:
        """
        query = "SELECT username, interests FROM users"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        user_interests = {}

        for row in result:
            username = row[0]
            interests = row[1].split(",")
            user_interests[username] = interests

        return user_interests
