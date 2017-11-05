#!/usr/bin/python
# -*- coding:utf-8 -*-

import tushare as ts

print(ts.__version__)

print ts.get_hist_data('600848') #一次性获取全部日k线数据
