from pymongo import MongoClient
import requests
from lxml import html
from pprint import pprint

# url = 'https://lenta.ru/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56'}

response = requests.get('https://lenta.ru/', headers=headers)
dom = html.fromstring(response.text)
collecting = dom.xpath("//div[@klass='topnews_column']")

news_list = []
for col in collecting:
    cards = col.xpath(".//a[@class='card-mini _topnews']")
    for card in cards:
        news_list.append({
            "source": "lenta.ru",
            "news": col[0].xpath(".//h3/text()")[0],
            "linc": col[0].xpath(".//a[@class='card-big _topnews _news']/@href")[0],
            "publication_time": col[0].xpath(".//time[@class='card-big__date']/text()")[0]
        })

    client = MongoClient("localhost", 27017)
    db = client["news_list"]
    lenta = db.lenta

    for elem in news_list:
        lenta.insert_one(elem)

    list(lenta.find({}))

    # fishing_list = []
    # for item in fishing_items:
    #     fish = {}
    #     name = item.xpath(".//h3[@class='s-item__title']/text()")[0]
    #     link = item.xpath(".//h3[@class='s-item__title']/../@href")[0]
    #     price = item.xpath(".//span[@class='s-item__price']//text()")
    #     info = item.xpath(".//span[contains(@class,'s-item__hotness')]/span/text()")

    #     fish['name'] = name
    #     fish['price'] = price
    #     fish['info'] = info
    #     fish['link'] = link
    #
    #     fishing_list.append(fish)
    #
    # #pprint(fishing_list)
