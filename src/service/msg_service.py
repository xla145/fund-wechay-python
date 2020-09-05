# -*- coding: UTF-8 -*-
import logging
from typing import Union

import requests
from wechaty import UrlLink
from wechaty_puppet import UrlLinkPayload, FileBox, get_logger

from service.fund import south_north_fund
from service.muisc import get_music_url
from service.weather import MJWeather
from util.common_util import CommonUtil
from util.request_util import get

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
    weather_str, link = we.get_weather('guangdong', "guangzhou")
    link_payload = UrlLinkPayload(description="点击查看详情", title="当日广州 %s" % weather_str, url=link,
                                  thumbnailUrl="https://img.mupaie.com/20200903161818.png")
    url_link = UrlLink(payload=link_payload)
    return url_link


# 获取北上资金信息
def get_south_north_fund() -> Union[str, UrlLink]:
    # 判断是否是工作日
    if CommonUtil.is_holiday():
        alert_msg = "今天是非工作日，股票市场不交易"
        log.info(alert_msg)
        return alert_msg
    return south_north_fund()


# 获取音乐文件
def get_music_file_url(name: str) -> FileBox:
    log.info("name=%s" % name)
    music_url, music_name = get_music_url(name)
    log.info("url=%s,name=%s" % (music_url, music_name))
    return FileBox.from_url(music_url, music_name)
