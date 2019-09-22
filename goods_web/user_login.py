#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: zzy
@file: user_login.py.py
@time: 2019/8/22 11:52
'''
'''
用户登录文件

'''
from user_register import  check_user_name
import pymysql
import json


# 验证登录密码函数
def check_login_passwd(user_name,passwd):
    '''
    函数功能：验证登录密码是否匹配
    :param user_name: 用户输入的用户名（数据库已存在的用户名）
    :param passwd: 用户输入的密码
    :return: 0：密码匹配用户名
             1：密码不匹配
    '''
    print(user_name,passwd)
    conf = json.load(open("server.json"))
    # 创建对象，连接数据库
    conn = pymysql.connect(conf["db_server"], conf["db_user"], conf["db_password"], conf["db_name"] )
    # 获取一个游标对象，用于执行sql语句
    try:
        with conn.cursor() as cur:

            # 执行任意支持的SQL语句
            sql = "select uname from shop_user where uname='{}' and passwd='{}'".format(user_name, passwd)
            cur.execute(sql)
            # 通过用游标获取结果
            rows = cur.fetchone()
            print(rows, type(rows))
    finally:
        # 关闭数据库
        conn.close()
    if  rows:
        return 0
    else:
        return 1

# 验证登录信息
def check_login():
    '''
    函数功能：循环调用验证用户名，密码函数，验证登录信息
    函数参数：无
    :return: user_name: 用户输入的正确的用户名
             passwd: 用户输入的正确的密码
    '''
    while True:
        user_name = input("用户名：\n")

        ret = check_user_name(user_name)

        if ret == user_name:
            print("用户名不存在，请重新输入！")
        elif ret == 1:
            print("用户格式错误，请重新输入！")
        elif ret == 2:
            print("\n用户名正确！")
            break
    while True:
        passwd = input("\n密码：")
        ret = check_login_passwd(user_name,passwd)
        if ret == 0:
            print("密码正确！")
            break
        else:
            print("密码错误，请重新输入！")
    return user_name


