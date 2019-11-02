#!/usr/bin/python
# -*- coding: UTF-8 -*-
#coding=utf8
from __future__ import unicode_literals
import os
import socket
from datetime import datetime
import time
import requests
import psutil
import json
import sys
import argparse

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def get_cpu_info():

    ##逻辑cpu
    cpu_count = psutil.cpu_count()
    ##物理cpu个数
    cpu_count_phy = psutil.cpu_count(logical=False)
    # ##获取1s内，cpu整体使用率
    # cpu_percent = psutil.cpu_percent(interval=1)
    ##cpu类型
    cpu_type=os.popen("cat /proc/cpuinfo |grep 'model name'|uniq |awk -F ':' '{print $2}'").read().strip('\n ')
    if cpu_count and cpu_type:
        return dict(cpu_count=cpu_count,cpu_type=cpu_type)
    else:
        print("获取cpu信息不完全，请查看服务器硬件配置。cpu_count=%s,cpu_type=%s"%(cpu_count,cpu_type))
        exit(1)

def get_memory_info():
    virtual_mem = psutil.virtual_memory()
    mem_total = bytes2human(virtual_mem.total)
    swap_mem=psutil.swap_memory()
    if mem_total:
        return dict(mem_total=mem_total)
    else:
        print("获取内存信息失败")
        exit(1)


def get_disk_info():
    disk_usage = psutil.disk_usage('/')

    disk_total = bytes2human(disk_usage.total)
    if disk_total:
        return dict(disk_total=disk_total)
    else:
        print("获取根分区信息失败")
        exit(1)
def get_net_info():
    """
    net_inter_name_List:服务器所有网络接口名称
    var_inter_List=['lo','docker0'] 定义非物理网络接口列表
    phy_inter_List=list(set(net_inter_name_List)-set(var_inter_List))
    isup
    inter_ipv4_addr
    inter_ipv6_addr
    inter_mac_addr
    :return:
    """
    net_inter_inf={}
    net_inter_name_List=psutil.net_if_stats().keys()
    var_inter_List = ['lo', 'docker0','cni0']
    phy_inter_List = list(set(net_inter_name_List) - set(var_inter_List))
    inter_ipv4_addr = None
    inter_ipv6_addr = None
    inter_mac_addr = None
    for inter in phy_inter_List:
        isup = psutil.net_if_stats().get(inter).isup
        if isup:
            if len(psutil.net_if_addrs().get(inter)) == 3:
                inter_ipv4_addr = psutil.net_if_addrs().get(inter)[0].address
                # inter_ipv6_addr = psutil.net_if_addrs().get(inter)[1].address
                inter_mac_addr = psutil.net_if_addrs().get(inter)[-1].address
                break
            elif len(psutil.net_if_addrs().get(inter)) > 3:
                inter_ipv4_addr = psutil.net_if_addrs().get(inter)[0].address
                # inter_ipv6_addr = psutil.net_if_addrs().get(inter)[1].address
                inter_mac_addr = psutil.net_if_addrs().get(inter)[-1].address
                break
    if inter_ipv4_addr and inter_mac_addr:
        net_inter_inf.update(dict(inter_ipv4_addr=inter_ipv4_addr, inter_mac_addr=inter_mac_addr))
        return net_inter_inf
    else:
        print("ip信息获取失败")
        exit(1)
def get_boot_info():
    """
    获取服务器开机时间
    :return:
    """
    # boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    # boot_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time()))
    ##架构
    # cpu_jg=subprocess.getstatusoutput('uname -m')[1]
    cpu_jg = os.popen('uname -m').read().strip(' \n')
    # ipdb.set_trace()
    # print(cpu_jg)
    if cpu_jg=="x86_64":
        czxt = os.popen('cat /etc/redhat-release').read().strip(' \n')
        # czxt=subprocess.getstatusoutput('cat /etc/redhat-release')[1]
        # ipdb.set_trace()
    else:
        czxt = os.popen('cat /etc/issue|head -n 1').read().strip(' \\n \\l\n')
        #czxt = os.popen('cat /etc/issue|head -n 1').read().strip(' \n')
        # czxt = subprocess.getstatusoutput('cat /etc/issue|head -n 1')[1]
        # ipdb.set_trace()
    # print(czxt)
    if cpu_jg and czxt:
        return dict(cpu_result=cpu_jg,czxt=czxt.strip(' \n \l'))
    else:
        print("获取系统信息失败")
        exit(1)

def get_system_info():
    return dict(hostname = socket.gethostname())

def collect_monitor_data(deplyInf):
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    data={
        "bootinf":get_boot_info(),
        "cpuinf":get_cpu_info(),
        "memoryinf":get_memory_info(),
        "diskinf":get_disk_info(),
        "netinf":get_net_info(),
        "systeminf":get_system_info(),
        'cur_time':cur_time,
        "deplyInf":deplyInf
    }
    return data


def sendData(data):
    url="http://192.168.2.50:10000/serverInfcollection/serverDataAPI"
    try:
        response=requests.post(url,json.dumps(data))
        print(response.status_code)
        print(response.text)
    except Exception as error:
        print(error)

def _argparse():
    parser=argparse.ArgumentParser(description="this is description")
    parser.add_argument("--admin",dest="admin",help=u"管理员的uid",default=1)
    parser.add_argument("--localtion", dest="localtion",help=u"服务器位置-机柜1/zstack2.25", default="机柜1")
    parser.add_argument("--user", dest="user",help=u"使用者名称-开发1/测试1", default="开发")
    parser.add_argument("--application",dest="application", help=u"用途说明-测试/部署pro6.3.11", default="部署pro6.3")
    return parser.parse_args()

def main():
    parser=_argparse()
    try:
        uid=int(parser.admin)
    except :
        print("管理员id必须为数字")
        exit(1)
    else:
        deplyInf={
            "adminId":parser.admin,
            "localtion":parser.localtion,
            "user":parser.user,
            "application":parser.application
        }
        data = collect_monitor_data(deplyInf)
        print(json.dumps(data))
        sendData(data)

if __name__ == '__main__':
    main()

