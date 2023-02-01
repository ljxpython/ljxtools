# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:李佳欣
@file: cmd_comand.py
@time: 2021/07/15
"""

'''
如有有命令行方式的交互可以写入到该模块的类中
'''

'''
如有有命令行方式的交互可以写入到该模块的类中
模式：
cmd = "xxxx"
f = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
resp = f.stdout.readlines()
return cmd,resp

'''

import json
import os
import re
import time
from subprocess import PIPE, STDOUT, Popen


class CmdComand(object):
    def __init__(self):
        pass

    ## --------------adb-----------------------
    def adb_screeen(self, ip, path="/sdcard/screen.png"):
        '''
        adb命令。快照
        '''
        cmd = "adb -s {} shell screencap -p {}".format(ip, path)
        f = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        resp = f.stdout.readlines()
        return cmd, resp

    def adb_push(self, ip, src, dest):
        if ip and len(ip):
            cmd = "adb -s " + ip
        else:
            cmd = "adb "
        cmd += " push " + src + " " + dest
        f = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        resp = f.stdout.readlines()
        return cmd, resp

    def adb_pull(self, ip, src, dest):
        if ip and len(ip):
            cmd = "adb -s " + ip
        else:
            cmd = "adb "
        cmd += " pull " + src + " " + dest
        f = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        resp = f.stdout.readlines()
        return cmd, resp

    ## 针对分辨率的适配性adb命令
    def adb_size(self, ip):
        '''
        该命令是获取物理机的物理分辨率
        之后，我们点击是根据在屏幕上的一个比例来进行的，相关的配置如下：
        a = int(reslut[1][0].decode().split(":")[1].replace("\n","").split("x")[0])/2
        b = int(reslut[1][0].decode().split(":")[1].replace("\n", "").split("x")[1])*(0.5)
        :param ip:
        :return:
        '''
        if ip and len(ip):
            cmd = "adb -s " + ip
        else:
            cmd = "adb "
        cmd += " shell wm size"
        f = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        resp = f.stdout.readlines()
        # print(cmd)
        return cmd, resp

    def adb_quit(self, ip):
        '''
        这个命令是两次back按键
        :param ip:
        :return:
        '''
        if ip and len(ip):
            cmd = "adb -s " + ip
        else:
            cmd = "adb "
        cmd += " shell " + " input keyevent 4"

        # cmd = "adb -s {} shell am force-stop {}".format(ip,packagename)
        for i in range(2):
            f = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
            time.sleep(0.1)
            print(cmd)
        return cmd

    def adb_packgename(self, ip, packagename, packageactivity):
        '''
        这个脚本可以实现这个操作，如果你的安卓手机不在这个界面，那么会启动这个app。
        :param ip:
        :param packagename:
        :param packageactivity:
        :return:
        '''
        if ip and len(ip):
            cmd = "adb -s " + ip
        else:
            cmd = "adb "
        cmd += " shell 'dumpsys window | grep mCurrentFocus'"
        print(cmd)
        f = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        resp = f.stdout.read().decode()
        reslut = re.search(r"{}".format(packagename), resp)
        print(resp)
        if not reslut:
            cmd = "adb shell am start -n {}".format(packageactivity)
            f = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
            print(cmd)

        return cmd, resp


adb_oprator = CmdComand()
