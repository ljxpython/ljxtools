# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:李佳欣
@file: result_assert_handle.py
@time: 2022/09/05
"""


def result_assert(resp: dict):
    '''
    火山的接口返回主要由两部分组成，
    第一部分 请求相关参数，及是否有异常
    "ResponseMetadata": {
        "Action": "ListPortMapping",
        "Region": "cn-north-1",
        "RequestId": "2022090515193501017425415608099BBA",
        "Service": "ipaas",
        "Version": "2020-10-25"
    },
    如果有异常，查询不到业务的逻辑，形式如下：
    如果遇到如下的情况，那么我们直接跑出exception，终止本次异常的测试
    "ResponseMetadata": {
        "Action": "GetJobDetails",
        "Error": {
            "Code": "[service.GetJobDetails] error: remote or network error: *maintainer.MaintainerServiceGetRequestDetailResult read field 0 'success' error: *maintainer.GetRequestDetailResp read field 1 'RequestInfo' error: Required field RequestID is not set",
            "CodeN": 8000000,
            "Message": "[service.GetJobDetails] error: remote or network error: *maintainer.MaintainerServiceGetRequestDetailResult read field 0 'success' error: *maintainer.GetRequestDetailResp read field 1 'RequestInfo' error: Required field RequestID is not set"
        },
        "Region": "cn-north-1",
        "RequestId": "202209051520220101742541560809D48C",
        "Service": "ipaas",
        "Version": "2020-10-25"
    }
    第二部分 业务查询的结果
    "Result": {
        "row": [],
        "total": 0
    }
    :param resp:
    :return: 返回两部分
    '''
