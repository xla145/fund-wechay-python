# -*- coding: UTF-8 -*-
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}


# get 请求
def get(url, params: dict = None):
    resp = requests.get(url, params, headers=headers)
    return resp.text


# post 请求
def post(url, data):
    resp = requests.post(url, data, headers=headers)
    return resp.text
