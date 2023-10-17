from flask import Flask, render_template, request, session, redirect, url_for, flash
import mysql.connector
from datetime import datetime

# 创建一个News类的对象，实现对interests标签的新闻到达选择
from news import News
user_news = News("Localhost", "root", "123456", "news")
# print(user_news.get_message("科技"))
# print(user_news.get_message("体育"))


app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 连接到 MySQL 数据库
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="user"
)

cursor = conn.cursor()

# 注册页面路由
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # 获取表单输入值
        username = request.form.get('username')
        password = request.form.get('password')

        # 检查用户名是否已存在
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        if user:
            # 用户名已被注册
            flash('该用户名已被注册，请尝试其他用户名。')
            return redirect(url_for('signup'))
        else:
            # 在数据库中插入新用户信息
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            conn.commit()

            # 设置 session 并重定向到选择兴趣页面
            session['username'] = username
            return redirect(url_for('choose_interests'))
    else:
        # 呈现注册表单
        return render_template('signup.html')


# 登录页面路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:  # 如果已经登录，直接跳转到主页
        return redirect(url_for('index'))
    # 处理登录表单的 POST 请求
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        if user:
            # 设置用户的 session 并重定向到主页
            session['username'] = user[0]
            return redirect(url_for('index'))
        else:
            # 登录信息错误，请重新输入
            return render_template('login.html', message='你的用户名或者密码错误！')
    else:
        # 显示登录页面
        return render_template('login.html')

# 主页路由
@app.route('/')
def index():
    # 检查当前会话是否有效（即用户是否已登录）
    if 'username' in session:
        # 查询用户信息
        query = "SELECT * FROM users WHERE username=%s"
        cursor.execute(query, (session['username'],))
        users = cursor.fetchone()
        interests_str = users[2] # 获取用户的兴趣爱好信息
#      url = ["https://www.bilibili.com","https://www.baidu.com","https://juejin.cn/"]
        if interests_str:

            # 将兴趣爱好字符串拆分成列表
            interests = [i.strip() for i in interests_str.split(',')]
            # 完整的兴趣列表
            complete_interests = ["体育", "科技", "经济", "政治", "娱乐"]
            guess_interests = list(set(complete_interests) ^ set(interests))
#           print(guess_interests)
#           print(interests)

            # 用字典存储每个兴趣爱好对应的新闻url和title
            news_dict = {}
            for interest in interests:
                urls, titles = user_news.get_message(interest)
#               print(urls)
#               print(titles)
                news_list = [{'url': url, 'title': title} for url, title in zip(urls, titles)]
                import random
                # 从news_list中随机选择20个新闻
                news_list = random.sample(news_list, 20)
                news_dict[interest] = news_list

            # 根据猜测用户喜欢的类别，传入一个字典
            guess_news_dict = {}
            for guess_interest in guess_interests:
                guess_urls, guess_titles = user_news.get_message(guess_interest)
                #               print(urls)
                #               print(titles)
                guess_news_list = [{'url': url, 'title': title} for url, title in zip(guess_urls, guess_titles)]
                import random
                # 从news_list中随机选择20个新闻
                guess_news_list = random.sample(guess_news_list, 10)
                guess_news_dict[guess_interest] = guess_news_list


            # 根据历史记录更新用户的兴趣
            update_interests(users[0])
            # 在HTML模板中展示兴趣爱好和对应的新闻链接
            return render_template('index.html', news_dict=news_dict,username = users[0],guess_news_dict=guess_news_dict)
        else:
            # 如果用户未选择兴趣爱好，则重定向到选择兴趣爱好页面
            return redirect(url_for('choose_interests'))
    else:
        # 如果未登录，重定向到登录页面
        return redirect(url_for('login'))


# 选择感兴趣的新闻类别页面路由
@app.route('/choose_interests', methods=['GET', 'POST'])
def choose_interests():
    if request.method == 'POST':
        # 获取POST请求中的用户名和感兴趣的新闻类别
        username = session.get('username')
        interests = request.form.getlist('interests')
        # 更新用户感兴趣的新闻类别
        query = "UPDATE users SET interests=%s WHERE username=%s"
        cursor.execute(query, (', '.join(interests), username))
        conn.commit()
        # 跳转到主页
        return redirect(url_for('index'))
    else:
        return render_template('choose_interests.html')


# 关于我们路由
@app.route('/about')
def about():
    # 显示关于我们页面
    return render_template('about.html')


# Flask 路由，用于处理用户浏览记录的 Ajax 请求
@app.route('/log_history', methods=['POST'])
def log_history():
    # 获取当前用户的 ID
    username = session.get('username')
    if username:
        # 获取 Ajax 请求中携带的新闻的原链接和时间
        url = request.form.get('news_url')
        time_str = request.form.get('time')
        # 将时间字符串转换为 datetime 对象
        time = datetime.strptime(time_str, '%Y/%m/%d %H:%M:%S')
        # 将用户浏览记录和浏览时间插入到数据库表 user_history 中
        sql = "INSERT INTO user_history (username, url, time) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, url, time))
        conn.commit()
        # print(f"User {username} visited {url} at {time}")
    # 返回空的响应
    return ''

# 用户浏览记录页面路由
@app.route('/history')
def history():
    # 检查当前会话是否有效（即用户是否已登录）
    if 'username' in session:
        # 查询用户浏览记录
        cursor = conn.cursor()
        query = "SELECT url, time FROM user_history WHERE username=%s ORDER BY time DESC"
        cursor.execute(query, (session['username'],))
        user_history = cursor.fetchall()
        # 显示用户浏览记录
        return render_template('history.html', user_history=user_history)
    else:
        # 如果未登录，重定向到登录页面
        return redirect(url_for('login'))

# 更新用户的兴趣
def update_interests(username):
    # 1. 从 user_history 表中获取该用户浏览过的新闻的 url。
    sql = "SELECT url FROM user_history WHERE username=%s"
    cursor.execute(sql, (username,))
    urls = set([row[0] for row in cursor.fetchall()])
#    print(urls)

    # 2. 根据新闻的 url 在 news 表中查询新闻的类别信息。
    interests = set()
    for url in urls:
        # 调用这个News类的方法，获取type
        interest = user_news.get_type(url)
        # print(interest)
        if interest:
            interests.add(interest)
        # print(interests)

    # 3. 删除不在浏览记录中出现的兴趣。
    if interests:
        # 将兴趣列表转换为逗号分隔的字符串
        interests_str = ','.join(interests)
        # 构造SQL语句
        sql = "UPDATE users SET interests = %s WHERE username = %s"
        # 执行SQL语句
        cursor.execute(sql, (interests_str, username))
        conn.commit()



if __name__ == '__main__':
    app.run(debug=True)
