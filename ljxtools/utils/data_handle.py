# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:李佳欣
@file: config.py
@time: 2022/03/12
"""


'''
对配置文件的封装

对yaml二次功能封装
实现：
根据global文件切换线上环境/线下环境   -- 这个需求暂时不做了，有替代的方案
指定路径，完成yaml读取
指定路径，完成yaml动态写入
对配置文件相关参数，读取 --（这部分考虑是不是做到外层）

'''


import inspect
import json
import os

import yaml


class DataSlove(object):
    def __init__(self):
        pass

    def read_yaml(self, file_path: str) -> dict:
        """读取yaml里面里面的数据"""
        try:
            with open(file_path, "r", encoding='utf8') as f:
                return yaml.load(f, Loader=yaml.Loader)
        except Exception as error:
            logger.info(f'读取yaml失败，错误如下：{error}')
            return False

    def read_json(self, file_path: str):
        logger.info("加载 {} 文件......".format(file_path))
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
        logger.info("读到数据 ==>>  {} ".format(data))
        return data

    def get_data_yaml(self, test_path, test_name):
        '''
        封装函数，简化代码，直接调用这一行代码就可以讲test_data中指定的数据读取出来
        这块要说一下命名规则 test_case_{num}_{env}.yaml
        :return:
        '''
        env_value = os.environ.get('TEST_ENV')
        case_data_name = test_name + '_' + env_value
        path = os.path.join(test_data_dir, test_path, case_data_name)
        logger.info("test data read from {}".format(path))
        return self.read_yaml(path)

    def get_config(self, file_name: str):
        '''
        根据文件名，读取config.yaml中的配置文件
        :param file_name:
        :return:
        '''
        yaml_data = self.read_yaml(config_file_path)
        # print(type(yaml_data))
        # print(yaml_data)
        # print(yaml_data.keys())
        dict_data = dict()
        # 判断是不是有这个字段，如果有则返回正确的值，如果错误，则给出正确的提示
        if file_name in yaml_data.keys():
            dict_data = yaml_data[file_name]
        else:
            logger.info(f"{file_name} is not exist in {config_file_path}")
        return dict_data

    def get_data(self, file: str) -> dict:
        '''
        根据文件的结尾（yaml，json 来选取不同的方式解析文件）返回执行case的具体信息
        :param file:
        :return:
        '''
        filter_dict = dict()
        if os.path.splitext(os.path.split(file)[1])[1] == ".yaml":
            logger.info(file)
            filter_dict = self.read_yaml(file)
        if os.path.splitext(os.path.split(file)[1])[1] == ".json":
            logger.info(file)
            filter_dict = self.read_json(file)
        return filter_dict


def get_file_name(env_value):
    '''
    拿到测试数据
    需要提供test_case目录下那一个的路径和文件名，函数自动返回对应data目录下的所有py文件
    判断环境，过滤不属于boe或者online中的文件
    :return:
    '''
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    file_name_dir = module.__file__
    ## 拿到test_case 下的路径信息
    file_path = file_name_dir.replace(test_case_dir + "/", "")
    # 在下面这个路径下查找信息
    final_path = os.path.join(test_data_dir, file_path)
    # final_path = test_data_dir + file_path
    # logger.info(final_path)
    # 取到文件名
    file_name = os.path.splitext(os.path.split(file_name_dir)[1])[0]
    # logger.info(file_name)
    # 找到该目录
    test_info_dir = os.path.join(os.path.dirname(final_path), file_name)
    # logger.info(test_info_dir)
    filter_list = get_file_list(test_info_dir, env_value)
    logger.info(filter_list)
    return filter_list


def get_file_list(file_path: str, env_value) -> list:
    '''
    根据文件路径，找到指定的文件，并返回列表
    :param file_path:
    :return:
    '''
    # file_list = os.listdir(file_path)
    # filter_path_list = list()
    abs_file_list = file_opreator.absolute_iterates(file_path)
    filter_list = list()
    for file in abs_file_list:

        # 先判断文件结尾是不是["yaml" ,"json"]
        # logger.info(file)
        # logger.info(os.path.splitext(file)[1] )
        # logger.info(os.path.splitext(os.path.split(file)[1])[0])
        # logger.info(type(os.path.splitext(file)[1]))
        # logger.info(type(os.path.splitext(os.path.split(file)[1])[0]))
        # logger.info(env_value)
        if os.path.splitext(file)[1] in [".yaml", ".json"] and env_value in os.path.splitext(os.path.split(file)[1])[0]:
            filter_list.append(file)

    logger.info(filter_list)
    return filter_list


def get_client_info(info: dict) -> dict:
    '''
    返回客户端需要的相关参数
    console类型需要：
        self.api_root_host = api_root_host
        self.version = version
        self.region = region
        self.server_name = server_name
        self.account = account
        self.password = password

    :return: dict[...]
    '''
    # message_dict = dict()
    message_dict = {
        "api_root_host": info["HOST"],
        "version": info["version"],
        "region": info["region"],
        "server_name": info["ServiceName"],
        "account": info["account"],
        "password": info["password"],
    }
    return message_dict


def get_openapi_info(info: dict) -> dict:
    '''
    返回客户端需要的相关参数
    openapi类型需要：
        self.api_root_host = api_root_host
        self.ak = ak
        self.sk = sk
        self.version = version
        self.region = region
        self.server_name = server_name

    :return: dict[...]
    '''
    message_dict = {
        "api_root_host": info["HOST"],
        "version": info["version"],
        "region": info["region"],
        "server_name": info["ServiceName"],
        "ak": info["ak"],
        "sk": info["sk"],
    }
    return message_dict


def get_api_content(apiname: str) -> dict:
    '''
    根据文件名，读取指定服务的所有接口信息
    目前，文件存储在test_data目录下，暂时已 servername.yaml来进行命名
    :param apiname:
    :return:
    '''
    path = os.path.join(test_data_dir, apiname + ".yaml")
    content = data_slove.read_yaml(path)
    return content


def set_content(interface_api: dict, config: dict):
    '''
    遍历interface_api,如果config中能匹配到相应的key值，则把value值写入
    下面的逻辑在写的时候，快把我逼疯了
    E.g:
            interface_api = set_content(interface_api,filter_data[ipaas_api.HostManagement.ListHost])


    :param interface_api:
    :param config:
    :return:
    '''
    # if isinstance(interface_api,dict):
    #     for k,v in interface_api.items():
    #         set_content(v,config)
    # elif isinstance(interface_api,(list,tuple,str)):
    #     if interface_api ==
    # logger.info(interface_api)
    # logger.info(config)
    if isinstance(interface_api, dict):
        for k, _ in interface_api.items():
            # logger.info(k)
            # logger.info(interface_api)
            # logger.info(k)
            # if isinstance(interface_api[k],dict):
            #     logger.debug(f"{k} is a dict")
            if isinstance(interface_api[k], dict) and k in config.keys():
                logger.info(f"{k} is dict same in api and config")
                set_content(interface_api[k], config[k])
            elif isinstance(interface_api[k], dict) and k not in config.keys():
                logger.info(f"{k} not in config,应该进入下一个循环")
                set_content(interface_api[k], config)
            elif isinstance(interface_api[k], (str, list, tuple)) and k not in config.keys():
                logger.info(f"{k} not in config11")
                continue
            elif isinstance(interface_api[k], (list, str, tuple)) and k in config.keys():
                logger.info(f"{k} is value in in config")
                interface_api[k] = config[k]
            elif interface_api[k] is None and k in config.keys():
                interface_api[k] = config[k]
            elif interface_api[k] is None and k not in config.keys():
                continue
            else:
                logger.info(f"难道我有些情况没有考虑到？{interface_api[k]}")
    # else:
    #     pass
    # if k in config.keys() and not isinstance(k,dict):
    #     interface_api[k] = config[k]
    # # elif
    # elif isinstance(k,dict):
    #     set_content(k,config)
    return interface_api


def clear_dict(d):
    if d is None:
        logger.info(f"{d} is None")
        return None
    elif isinstance(d, list):
        return list(filter(lambda x: x is not None, map(clear_dict, d)))
    elif not isinstance(d, dict):
        return d
    else:
        r = dict(filter(lambda x: x[1] is not None, map(lambda x: (x[0], clear_dict(x[1])), d.items())))
        if not bool(r):
            return None
        logger.info(r)
        return r


def get_requests_params(request_params: dict) -> dict:
    '''
    将请求体中的action，method，
    :param request_params:
    :return:
    '''


class YamlHandle(object):
    '''
    下面这个方法暂时废弃，上面的类方法包括了下面的相关方法调用
    '''

    def __init__(self):
        # self.configpath = conf_dir
        pass

    def env(self):
        pass

    @staticmethod
    def read_yaml(file):
        """读取yaml里面里面的数据"""
        try:
            with open(file, "r", encoding='utf8') as f:
                return yaml.load(f, Loader=yaml.Loader)
        except Exception as error:
            print(f'读取yaml失败，错误如下：{error}')
            return False

    @classmethod
    def write_yaml(self, data, yaml_file='conf.yaml', mode='w'):
        """往yaml里面写入数据
        yamlFile：yaml文件名
        data：要写入的数据
        mode：写入方式： w，覆盖写入， a，追加写入
        将原数据读取出来，如果没有要加入的key，则创建一个，如果有，则执行key下面的数据修改
        """
        # try:
        old_data = self.read_yaml(yaml_file) or {}
        print(old_data)
        print(type(data))
        for data_key, data_value in data.items():
            if not old_data.get(data_key):
                old_data.setdefault(data_key, {})
                print(old_data)
            # for value_key, value_value in data_value.items():
            #     old_data[data_key][value_key] = value_value
        with open(yaml_file, mode, encoding="utf-8") as f:
            yaml.dump(old_data, f, Dumper=yaml.Dumper)
        return True
        # except Exception as error:
        #     print(f'yaml文件写入失败，错误如下：\n{error}')
        #     return False


data_slove = DataSlove()

yaml_slove = YamlHandle()

if __name__ == '__main__':

    dict_1 = {
        'ACTION': 'ListHost',
        'METHOD': 'GET',
        'PARAMS': {
            'product_id': '1549663199064756224',
            'X-Account-Id': '2100001638',
            'X-User-Id': None,
            'adb_key_id': None,
            'security_group_id': None,
            'host_id': 'h-1742848680918027',
            'host_id_list': None,
            'offset': None,
            'count': None,
        },
        'BODYS': None,
        'CASE': None,
    }
    clear_dict(dict_1)
    pass
