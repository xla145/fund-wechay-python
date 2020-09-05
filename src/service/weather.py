# -*- coding: UTF-8 -*-

"""
墨迹天气
"""

import requests
from lxml import etree

from util.common_util import CommonUtil


class MJWeather(object):

    def __init__(self) -> None:
        super().__init__()
        global headers
        global session
        session = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
            "X-Requested-With": "XMLHttpRequest",
            "Host": "tianqi.moji.com"
        }

    # 访问页面获取cookie
    def get_weather(self, province_en: str, city_en: str):
        url = "https://tianqi.moji.com/weather/china/%s/%s" % (province_en, city_en)
        resp = session.get(url, headers=headers)
        html = resp.text
        dom = etree.HTML(html)
        weather_list = dom.xpath("//div[@class='forecast clearfix']/ul[@class='days clearfix'][1]/li//text()")
        new_arr = CommonUtil.del_empty_str([w.strip() for w in weather_list])
        new_arr = CommonUtil.del_empty_str(new_arr)
        weather_str = "天气 %s，温度：%s，空气质量: %s" % (new_arr[1], new_arr[2], new_arr[5])
        return weather_str, url

    # 获取24小时的天气
    def get_24hour(self):
        self.get_index()
        url = "https://tianqi.moji.com/index/getHour24"
        resp = session.get(url, headers=headers)
        weather_json = resp.json()
        print(weather_json)


if __name__ == '__main__':
    we = MJWeather()
    we.get_weather('guangzhou')
