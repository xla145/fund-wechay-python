# -*- coding: UTF-8 -*-

# 查看详细
import logging
import re

import jsons
import requests
from wechaty import UrlLink
from wechaty_puppet import UrlLinkPayload, get_logger

from util.common_util import CommonUtil

log: logging.Logger = get_logger('MyBot')


"""
获取北上，南下资金信息
"""
def get_south_north_fund():
    url = "http://money.finance.sina.com.cn/quotes_service/api/jsonp.php/var%20liveDateTableList=/HK_MoneyFlow.getDayMoneyFlowOtherInfo"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
    }
    data = {
        'ts': 2342354353,
        '_': CommonUtil.get_timestamp()
    }
    resp = requests.get(url, data, headers=headers)
    html = resp.text
    live_date_table_list = re.findall("var liveDateTableList=\((.*?)\)", html)
    live_data = live_date_table_list[0]
    live_json = jsons.loads(live_data)
    fund_link = "http://stock.finance.sina.com.cn/hkstock/view/money_flow.php"
    title = "北上资金：%s 南下资金：%s" % (live_json["north_inFlow_total"], live_json["source_inFlow_total"])
    description = "沪股通%s 深股通%s,港股通（沪）%s 港股通（深）%s" % \
                  (live_json["south_hk_sh"]["daliyInflow"], live_json["south_hk_sz"]["daliyInflow"],
                   live_json["north_sh"]["daliyInflow"], live_json["north_sz"]["daliyInflow"])
    log.info(title, description)
    link_payload = UrlLinkPayload(description=description, title=title, url=fund_link,
                                  thumbnailUrl="")
    url_link = UrlLink(payload=link_payload)
    return url_link


if __name__ == '__main__':
    get_south_north_fund()
