# -*- coding: UTF-8 -*-
import logging

import requests
from wechaty import UrlLink
from wechaty_puppet import UrlLinkPayload, FileBox, get_logger

from service.muisc import get_music_url
from service.weather import MJWeather

log: logging.Logger = get_logger('msg_service')


# 获取公众号文章链接，返回 UrlLink 对象
def get_wx_public_article_url_link(wx_public) -> UrlLink:
    url = "http://localhost:8088/get_public_article"
    data = {
        "wx_public": wx_public
    }
    resp = requests.post(url, data)
    article_json = resp.json()
    # 取第一条
    article = article_json[0]
    title = str(article["title"]).replace("<em>", "").replace("</em>", "")
    article["title"] = title[0:15]
    if len(title) > 15:
        description = title[15:]
    else:
        description = title[0:15]
    link_payload = UrlLinkPayload(description=description, title=title, url=article["link"],
                                  thumbnailUrl=article["imageUrl"])
    url_link = UrlLink(payload=link_payload)
    return url_link


# 获取天气预报
def get_weather_url_link() -> UrlLink:
    we = MJWeather()
    weather_str, link = we.get_weather('guangzhou')
    link_payload = UrlLinkPayload(description="点击查看详情", title="当日广州 %s" % weather_str, url=link,
                                  thumbnailUrl="https://img.mupaie.com/20200903161818.png")
    url_link = UrlLink(payload=link_payload)
    return url_link


# 获取音乐文件
def get_music_file_url(name: str) -> FileBox:
    log.info("name=%s" % name)
    music_url, music_name = get_music_url(name)
    log.info("url=%s,name=%s" % (music_url, music_name))
    return FileBox.from_url(music_url, music_name)
