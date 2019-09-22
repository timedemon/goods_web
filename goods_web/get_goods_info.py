#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: zzy
@file: get_goods_info.py
@time: 2019/9/16 22:56
'''
import json
import pymysql

db_conf = json.load(open("server.json"))

def conn_sql_2(op):
    '''
    函数功能：连接数据库，得到购物车的商品信息
    :param op: 数据库操作
    :return: rows: 返回查询到的商品信息
    '''
    # 创建对象，连接数据库
    conn = pymysql.connect(db_conf["db_server"], db_conf["db_user"], db_conf["db_password"], db_conf["db_name"])
    # 获取一个游标对象，用于执行sql语句
    try:
        with conn.cursor() as cur:

            # 执行任意支持的SQL语句
            sql = op
            cur.execute(sql)
            conn.commit()
            # 通过用游标获取结果
            rows = cur.fetchall()
            print(rows, type(rows))
            return rows
    finally:
        # 关闭数据库
        conn.close()

def get_latiao_info():
    op = "select goods_price,goods_num from goods_information where goods_name='辣条'"
    lt_info = conn_sql_2(op)
    return lt_info

def get_kele_info():
    op = "select goods_price,goods_num from goods_information where goods_name='可乐'"
    kele_info = conn_sql_2(op)
    return kele_info

def get_dounai_info():
    op = "select goods_price,goods_num from goods_information where goods_name='豆奶'"
    dounai_info = conn_sql_2(op)
    return dounai_info

def get_binggan_info():
    op = "select goods_price,goods_num from goods_information where goods_name='饼干'"
    binggan_info = conn_sql_2(op)
    return binggan_info

def add_buy_car(op1, op2, op3):
    '''
       函数功能：连接数据库,将商品加入购物车,先查询购物车表中是否已存在对应用户的此商品的ID，若存在就修改商品数量，若不存在，
               就在表格中增加对应商品
       参数：数据库操作
       :return: True: 加入成功
    '''
    conn = pymysql.connect(db_conf["db_server"], db_conf["db_user"], db_conf["db_password"], db_conf["db_name"])
    with conn.cursor() as cur:
        try:
            sql = op1
            cur.execute(sql)
            rows = cur.fetchone()
            if not rows:
                cur.execute(op2)
                conn.commit()
            else:
                # print("修改已存数据")
                sql = op3
                cur.execute(sql)
                conn.commit()
        except Exception as e:
            print("插入失败！", e)
        finally:
            # 关闭游标
            cur.close()
    # 关闭数据库
    conn.close()
    return True