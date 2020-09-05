# -*- coding: UTF-8 -*-
import logging
import os
import time

import requests
from wechaty_puppet import get_logger

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
}

log: logging.Logger = get_logger('music')


# 下载一些vip音乐
def download(music_id: int):
    ts = int(time.time() * 1000)
    url = "https://api.zhuolin.wang/api.php?types=url&id=%s&source=netease&_=%d" % (music_id, ts)
    resp = requests.get(url, headers=header)
    json = resp.json()
    music_url = json["url"]
    # resp = requests.get(music_url, headers=header)
    # if not os.path.exists("music"):
    #     os.mkdir("music")
    # music_path = "music/%s.mp3" % music_name
    # with open(music_path, 'wb') as file:
    #     file.write(resp.content)
    return music_url


# 获取音乐列表
def get_music(name):
    url = "https://api.zhuolin.wang/api.php"
    data = {
        "types": "search",
        "count": 20,
        "source": "netease",
        "pages": 1,
        "name": name
    }
    resp = requests.post(url, data=data, headers=header)
    json = resp.json()
    music_list = []
    for music in json:
        music_list.append({"id": music["id"], "name": music["name"], "artist": "-".join(music["artist"])})
        # 获取音乐下载地址
    return music_list


"""
获取音乐下载链接
"""


def get_music_url(name: str):
    music_list = get_music(name)
    music_id = music_list[0]["id"]
    music_name = music_list[0]["name"]
    music_url = download(music_id)
    return music_url, music_name


if __name__ == '__main__':
    # 给音乐的编号
    # music_url, music_name = get_music_url("丢了你")
    # print(music_name)
    text = "音乐-丢啦你"
    print(text[text.find("-") + 1:])
