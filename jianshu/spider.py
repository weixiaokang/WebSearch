import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test


class jianshu():
    def all_url(self, url):
        html = self.request(url)
        soup = BeautifulSoup(html.text, 'lxml')
        result = soup.find_all(name='a', class_='title')
        meta_a = soup.select('div[class="meta"] > a')
        meta = soup.select('div[class="meta"]')
        flag = 0
        for result_url in result:
            content_url = 'http://www.jianshu.com' + result_url['href']
            content = self.request(content_url)
            soup = BeautifulSoup(content.text, 'lxml')
            titles = soup.find_all(name='h1', class_='title')
            title = titles[0].text
            pattern = re.compile("[^\u2E80-\u9FFF]")
            names = soup.find_all(name='span', class_='name')
            name = names[0].text
            times = soup.find_all(name='span', class_='publish-time')
            time = times[0].text
            wordages = soup.find_all(name='span', class_='wordage')
            wordage = wordages[0].text
            pos = flag * 2
            view_count = meta_a[pos].text.strip()
            comment_count = meta_a[pos + 1].text.strip()
            like_count = meta[flag].span.text.strip()
            flag += 1
            snippets = soup.find_all(attrs={'name': 'description'})
            if len(snippets) > 0:
                snippet = snippets[0]['content']
            else:
                snippet = ''
            self.save(title, pattern.sub('', content.text), snippet, name, content_url, time, wordage, view_count
                      , comment_count, like_count)

    def save(self, title, content, snippet, autor, url, time, wordage, view_count, comment_count, like_count):  # 这个函数保存文本
        db.doc.save({'title': title,
                       'content': content,
                       'snippet': snippet,
                       'autor': autor,
                       '_id': url,
                       'time': time,
                       'wordage': wordage,
                       'view_count': view_count,
                       'comment_count': comment_count,
                       'like_count': like_count})

    def request(self, url):
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = requests.get(url, headers=headers)
        return content

JianShu = jianshu()
# JianShu.all_url('http://www.jianshu.com/c/f6b4ca4bb891?utm_medium=index-collections&utm_source=desktop')
JianShu.all_url('http://www.jianshu.com/c/453ac7ca7ca2')
