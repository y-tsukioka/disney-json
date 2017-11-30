# coding=utf-8
import json
from flask import Flask, jsonify
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

url = 'http://info.tokyodisneyresort.jp/schedule/stop/stop_list.html'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})#ユーザーエージェント偽装
response = urlopen(req)
html = response.read()
soup = BeautifulSoup(html, "html.parser")


@app.route('/disney-api.json', methods=['GET'])
def get_disney_json():
    land_list = get_json(soup.find("section", class_="tdl col"), "land")
    sea_list = get_json(soup.find("section", class_="tds col"), "sea")
    d_dict = {"attractions": land_list+sea_list}
    return json.dumps(d_dict, ensure_ascii=False, indent=4)


def get_json(s_list, place):
    attraction = get_element(s_list.findAll("dd")[0], place, "attraction")
    show = get_element(s_list.findAll("dd")[1], place, "show")
    character = get_element(s_list.findAll("dd")[2], place, "character")
    shop = get_element(s_list.findAll("dd")[3], place, "shop")
    restaurant = get_element(s_list.findAll("dd")[4], place, "restaurant")
    service = get_element(s_list.findAll("dd")[5], place, "service")
    e_list = attraction+show+character+shop+restaurant+service

    return e_list


def get_element(e_list, place, typ):
    json_arr = []
    for a in e_list.findAll("li"):
        title = a.find(["a", "p"]).get_text()
        span = a.find("span").get_text().split("-")
        if len(span) == 1:
            start = span[0]
            end = span[0]
        else:
            start = span[0]
            end = span[1]
        json_arr.append({"place": place, "type": typ, "title": title, "start": start, "end": end})

    return json_arr


if __name__ == '__main__':
    app.run()
