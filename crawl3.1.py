import sys
import requests
from news import News
# 爬虫实现
def get_news_data(i):
    init_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2515&k=&num=50&page={}'  # 科技
    # init_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2513&k=&num=50&page={}'#娱乐
    # init_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2511&k=&num=50&page={}'#国际
    # init_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2512&k=&num=50&page={}'#体育
    # init_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2514&k=&num=50&page={}'#军事
    # init_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2516&k=&num=50&page={}'#财经
    page = requests.get(url=init_url.format(i), headers=headers).json()
    headlines = []
    urls = []
    for j in range(50):
        headline = page['result']['data'][j]['title']
        url = page['result']['data'][j]['url']
        headlines.append(headline)
        urls.append(url)
    return headlines, urls

def scrape_news():
    global headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    # choose pagenum you want to scrape
    pagenum = 5
    news_headlines = []
    news_urls = []
    for i in range(1, pagenum):
        try:
            headlines, urls = get_news_data(i)
            news_headlines.extend(headlines)
            news_urls.extend(urls)
        except:
            print("Failed to retrieve links from page " + str(i))
    # 将标题和URL存储在两个列表中，可以根据需要进行进一步处理和使用
    # print("Headlines:", news_headlines)
    # print("URLs:", news_urls)
    return news_urls,news_headlines

if __name__ == "__main__":
    sys.setrecursionlimit(100000)  # Set default recursion depth
    urls,title = scrape_news()
    print(urls)
    print(title)

    # 创建News对象
    news_obj = News("localhost", "root", "123456", "news")
    # 调用insert_data方法写入数据
    # news_obj.insert_data("科技", "股市持续下跌怎么办？“股神”巴菲特这样应对大熊市", "https://new.qq.com/rain/a/20230626A02MTI00")
    for title, url in zip(title, urls):
        news_obj.insert_data("科技", title, url)





