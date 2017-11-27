# coding=utf-8
import re
from flask import Flask
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

app = Flask(__name__)


url = 'http://info.tokyodisneyresort.jp/schedule/stop/stop_list.html'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})#ユーザーエージェント偽装
response = urlopen(req)
html = response.read()
soup = BeautifulSoup(html, "html.parser")
land = soup.find("section", class_="tdl col")
sea = soup.find("section", class_="tds col")


@app.route('/disney-api', methods=['GET'])
def get_json():
    return get_land_elements()


def get_land_elements():
    attraction = land.findAll("dd")[0]
    show = land.findAll("dd")[1]
    character = land.findAll("dd")[2]
    shop = land.findAll("dd")[3]
    restaurant = land.findAll("dd")[4]
    service = land.findAll("dd")[5]
    row = []
    for e in attraction.find(["a","p"]):
        row.append(e.get)
    return row


def get_sea_elements():
    return 'sea'


if __name__ == '__main__':
    app.run()
