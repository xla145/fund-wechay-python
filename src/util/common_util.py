# -*- coding: UTF-8 -*-

# 工具类 分隔符
import datetime

import util
from util.request_util import get


class CommonUtil:

    @staticmethod
    def md5(text):
        hl = util.hashlib.md5()
        hl.update(text.encode(encoding='utf-8'))
        return hl.hexdigest()

    @staticmethod
    def str_join(arr, separator=","):
        if arr.__len__() == 1:
            return str(arr)
        return separator.join(arr)

    # 删除空字符串
    @staticmethod
    def del_empty_str(str_arr: util.List[str]):
        for s in str_arr:
            if s == '':
                str_arr.remove(s)
        return str_arr

    @staticmethod
    def get_timestamp() -> int:
        return int(util.time.time())

    @staticmethod
    def time_format(date_time: datetime.datetime, time_format: str) -> str:
        return date_time.strftime(time_format)

    @staticmethod
    def is_holiday(cur_time: datetime.datetime = datetime.datetime.utcnow()) -> bool:
        url = "http://tool.bitefu.net/jiari/?d=%s" % (CommonUtil.time_format(cur_time, "%Y-%m-%d"))
        text = get(url)
        if int(text) == 0:
            return False
        return True


if __name__ == '__main__':
    print(CommonUtil.is_holiday(datetime.datetime.utcnow()))
