# -*- coding: UTF-8 -*-

# 工具类 分隔符

import util


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



if __name__ == '__main__':
    print(CommonUtil.del_empty_str(['今天', '雷阵雨', '25° / 35°', '西北风', '1级', '', '46 优', '']))
