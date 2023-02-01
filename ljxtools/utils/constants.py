# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:李佳欣
@file: constants.py
@time: 2021/07/14
"""

'''
这个模块将常量固定
框架项目的顶层目录
一定要注意，所有功能最好不好耦合，各个模块单独运行，有利于系统的良好运行
只有该模块，对相关环境的路径进行明确，与其他模块进行必要的联系
'''

import os

# dirname(path) 是返回path的父路径

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_dir = os.path.join(base_dir, "config")
config_file_path = os.path.join(config_dir, "config.yaml")

common_dir = os.path.join(base_dir, "common")

data_dir = os.path.join(base_dir, "data")

demo_dir = os.path.join(base_dir, "demo")

logs_dir = os.path.join(base_dir, "logs")

output_dir = os.path.join(base_dir, "output")

test_case_dir = os.path.join(base_dir, "test_case")
test_data_dir = os.path.join(base_dir, "test_data")


if __name__ == '__main__':
    print(os.path.abspath("."))
    print(base_dir)
    print(common_dir)
    # print(conf_dir)
