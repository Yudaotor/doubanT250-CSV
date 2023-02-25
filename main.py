import requests
from lxml import etree
import csv
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 "
                  "Safari/537.36 Edg/110.0.1587.50 "
}
fp = open("./doubanTop250.csv", 'a', newline='', encoding='utf-8-sig')
writer = csv.writer(fp)
writer.writerow(
    ("名字", "排名", "图片链接", "豆瓣链接", "分数", "评分人数", "导演", "上映时间", "国家", "类型"))
for page in range(0, 226, 25):
    url = 'https://movie.douban.com/top250?start=%s&filter=' % page
    response = requests.get(url=url, headers=headers).text
    html_etree = etree.HTML(response)
    movie_li = html_etree.xpath('//*[@id="content"]/div/div[1]/ol/li')
    for item in movie_li:
        name = item.xpath("./div/div[2]/div[1]/a/span[1]/text()")[0]
        rank = item.xpath('./div/div[1]/em/text()')[0]
        image_link = item.xpath('./div/div[1]/a/img/@src')[0]
        link = item.xpath('./div/div[1]/a/@href')[0]
        rate = item.xpath('./div/div[2]/div[2]/div/span[2]/text()')[0]
        rate_number = re.sub(r'\D', "", item.xpath('./div/div[2]/div[2]/div/span[4]/text()')[0])
        director = re.findall('导演:(.*?)主', "".join(item.xpath('./div/div[2]/div[2]/p[1]/text()[1]')[0].split()))
        timeAndCountryAndType = "".join(item.xpath('./div/div[2]/div[2]/p[1]/text()[2]')[0].split())
        timeAndCountryAndType = timeAndCountryAndType.split('/')
        time = timeAndCountryAndType[0]
        country = timeAndCountryAndType[1]
        typee = timeAndCountryAndType[2]
        writer.writerow((rank, name, image_link, link, rate, rate_number, "".join(director), time, country, typee))
fp.close()
