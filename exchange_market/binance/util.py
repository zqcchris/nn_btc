#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20180917
# @Author  : zhaoqingchen
# @github  :

import hmac
import time
import hashlib

import urllib
import requests
from exchange_market.binance.enum import Interval

# timeout in 5 seconds:
TIMEOUT = 5


# 各种请求,获取数据方式
def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
        # "Connection": "close"
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)
    try:
        response = requests.get(url, postdata, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json()}
    except Exception as e:
        print("httpGet failed, detail is:%s" % e)
        return {"status": "fail", "msg": "%s" % e}


def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    try:
        response = requests.post(url, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
    except Exception as e:
        print("httpPost failed, detail is:%s" % e)
        return {"status":"fail","msg": "%s"%e}


def api_key_get(url, request_path, params, ACCESS_KEY, SECRET_KEY):
    method = 'GET'
    timestamp = int(round(time.time()*1000))
    params.update({'timestamp': timestamp})

    host_name = host_url = url
    # host_name = urlparse.urlparse(host_url).hostname
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()

    params['signature'] = createSign(params, SECRET_KEY)
    url = host_url + request_path
    add_to_headers = {"X-MBX-APIKEY": ACCESS_KEY}
    return http_get_request(url, params, add_to_headers)


def api_key_post(url, request_path, params, ACCESS_KEY, SECRET_KEY):
    params.update({'timestamp': int(time.time() * 1000)})
    host_url = url
    params['signature'] = createSign(params,  SECRET_KEY)
    url = host_url + request_path + '?' + urllib.parse.urlencode(params)
    add_to_headers = {"X-MBX-APIKEY": ACCESS_KEY}
    return http_post_request(url, params, add_to_headers)


def createSign(pParams, secret_key):
    payload = urllib.parse.urlencode(pParams).replace("%40", "@")
    digest = hmac.new(secret_key.encode("utf-8"), payload.encode("utf-8"), digestmod=hashlib.sha256).hexdigest()
    return digest


def interval2sec(interval):
    if interval == Interval.min1.value:
        return 60
    elif interval == Interval.min5.value:
        return 60 * 5
    elif interval == Interval.min15.value:
        return 60 * 15
    elif interval == Interval.min30.value:
        return 60 * 30
    elif interval == Interval.hour1.value:
        return 60 * 60
    elif interval == Interval.hour2.value:
        return 60 * 60 * 2
    elif interval == Interval.hour4.value:
        return 60 * 60 * 4
    elif interval == Interval.day1.value:
        return 60 * 60 * 4 * 6

