import time
import requests
from bs4 import BeautifulSoup


class TaobaoSpider:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.categories = ['女装', '男装', '内衣', '鞋靴', '箱包', '配饰', '童装玩具',
                           '孕产', '用品', '家电', '数码', '手机', '美妆', '洗护', '保健品',
                           '珠宝', '眼镜', '手表', '运动', '户外', '乐器', '游戏', '动漫',
                           '影视', '美食', '鲜花', '宠物', '农资绿植']
        self.data = []

    def get_data(self, category):
        for i in range(1, 101):
            try:
                url = f'https://s.taobao.com/search?q={category}&s={44*i}'
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    self.parse_data(response.text)
                else:
                    print(f"Failed to get page {i} for category {category}")
            except Exception as e:
                print(f"Error occurred: {e}")
            time.sleep(1)  # delay to avoid being blocked

    def parse_data(self, html):
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find_all('div', class_='items')[0].find_all('div', class_='item')
        for item in items:
            temp = {
                'title': item.find_all('img')[0]['alt'],
                'price': item.find_all('strong')[0].get_text(),
                'shop': item.find_all('div', class_='shop')[0].find_all('span')[0].get_text(),
                'location': item.find_all('div', class_='location')[0].get_text()
            }
            self.data.append(temp)

    def run(self):
        for category in self.categories:
            try:
                self.get_data(category)
                time.sleep(5)  # 在每次请求之间等待5秒
            except Exception as e:
                print(f"Error occurred: {str(e)}")


if __name__ == '__main__':
    spider = TaobaoSpider()
    spider.run()
    print(spider.data)
