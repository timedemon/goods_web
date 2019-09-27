#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: zzy
@file: main.py
@time: 2019/9/12 13:48
'''
import os
from datetime import timedelta
from flask import Flask, render_template, request,session,redirect,Response,jsonify,make_response
from user_login import  check_login_passwd
from user_register import get_passwd_md5, conn_sql, check_user_name, send_phone_security_code
from get_goods_info import *

app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
db_conf = json.load(open("server.json"))

lt_price = ''
lt_num = ''
kele_price = ''
kele_num = ''
dounai_price = ''
dounai_num = ''
binggan_price = ''
binggan_num = ''
@app.route('/')
def home():
    '''
    函数功能：网页主界面
    :return:
    '''
    global lt_price, lt_num, kele_price, kele_num, dounai_price, dounai_num, binggan_price, binggan_num
    uname = session.get("uname")

    goods_info = get_goods_info()
    # print(goods_info,123)
    lt_price = goods_info[0][1]
    kele_price = goods_info[1][1]
    dounai_price = goods_info[2][1]
    binggan_price = goods_info[3][1]

    lt_num = goods_info[0][2]
    kele_num = goods_info[1][2]
    dounai_num = goods_info[2][2]
    binggan_num = goods_info[3][2]

    rsp =Response(render_template("shop.html", uname=uname, lt_price=lt_price, kele_price= kele_price, dounai_price= dounai_price,
                                  binggan_price=binggan_price))
    return rsp

@app.route('/login', methods=["GET","POST"])
def login():
    '''
    函数功能：验证登录密码是否正确
    :return: 返回模板渲染
    '''
    if request.method == "GET":
        uname = session.get("uname")
        if uname:
            rsp = redirect("/")
            return rsp
        return render_template('login.html')
    elif request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("password")
        pwd =get_passwd_md5(pwd)

        ret = check_login_passwd(uname, pwd)
        if ret ==1:
            return render_template('login_fail.html')
        elif ret == 0: # 登录成功，跳转到首页

            session["uname"] = uname
            session.permanent = True

            rsp = redirect("/")
            return rsp

@app.route('/reg', methods=["GET", "POST"])
def reg():
    '''
    函数功能：注册用户,通过ajax得到用户名，手机号，手机验证码，前端提交表单后得到其他注册内容，然后
            将后端验证后的注册信息，通过ajax返回给前端。当用户名格式正确，并且验证码正确时，将用户信息写入数据库
    :return:
            result["phone_code"] = 1 表示验证码错误
            result["phone_code"] = 0 表示验证码正确
            result["reg"] = 1 表示注册失败
            result["reg"] = 0 表示注册成功
    '''
    if request.method == "GET":
        return render_template('regin.html')

@app.route('/check_reg', methods=['get', 'post'])
def regi():
    '''
    函数功能：校验验证码是否正确，若正确就将注册信息写入数据库
    :return:
    '''
    result = {}
    uname = request.args.get("uname")
    # print('表单得到的用户名', uname)
    pwd = request.args.get("password")
    sex = request.args.get("sex")
    interest = request.args.get("favorite")
    email = request.args.get("email")

    phone = request.args.get("phone")
    # print("表单得到的手机号！", type(phone))

    session_phone = session.get("phone")
    # print("发送验证码的手机号", session_phone)

    phone_code = session.get("phone_code")
    # print('发送的验证码', phone_code)

    user_phone_code = request.args.get("phone_code")
    # print("用户输入的验证码", user_phone_code)
    birth = request.args.get("birth")
    edu = request.args.get("edu")


    if phone == session_phone and phone_code == user_phone_code:
        result["phone_code"] = 0
        pwd = get_passwd_md5(pwd)
        print(pwd)
        ret = conn_sql(uname, pwd, sex, interest, email, birth, edu)
        print(ret)
        if not ret:
            result["reg"] = 1
        else:
            result["reg"] = 0
    else:
        result["phone_code"] = 1
        result["reg"] = 1
    return jsonify(result)



@app.route("/check_uname")

def check_uname():
    '''
    函数功能：校验用户名是否存在,通过ajax得到用户名，
            将后端验证后的注册信息，通过ajax返回给前端。
    :return:result["uname_format"] = 1 表示用户名格式错误
            result["uname_format"] = 2 表示用户名已存在
            result["uname_format"] = 0 表示用户名可以被注册

    '''
    result = {}
    uname = str(request.args.get("uname"))
    print(uname)

    ret = check_user_name(uname) # 校验用户名的函数
    if ret == 1:
        result["uname_format"] = 1
    elif ret == 2:
        result["uname_format"] = 2
    elif ret == 0:
        result["uname_format"] = 0
        session["uname"] = uname
    return jsonify(result)

@app.route("/send_phone_code")
def send_phone_code():
    '''
    函数功能：发送手机验证码
    :return: result["err"] = 0 表示发送验证码成功
             result["err"] = 1 表示发送验证码失败
    '''
    result = {}
    phone = request.args.get("phone")
    print("得到发送短信的手机号！",phone)
    if phone:
        phone_code = send_phone_security_code(phone)
        print(phone_code)
        session["phone_code"] = phone_code
        session["phone"] = phone
        result["err"] = 0
        result["phone_code"] = phone_code
    else:
        result["err"] = 1
    return jsonify(result)

@app.route("/logout")
def logout():
    '''
    函数功能：退出，清除session
    :return:
    '''
    if "uname" in session:
        session.pop("uname")
        rsp = redirect("/")
        return rsp
    else:
        return redirect("/login")

@app.route("/latiao_info",methods=["GET","POST"])
def latiao_info():
    '''
    函数功能：进入辣条购买界面,加入购物车
    :return:
    '''
    uname = session.get("uname")
    lt_price = session.get("lt_price")
    if request.method == "GET":
        # print(uname)
        if uname:
            return render_template("latiao.html", lt_num=lt_num, lt_price=lt_price, uname=uname)
        else:
            return "请先登录！"
    elif request.method == "POST":
        buy_lt_num = request.form.get("buy_lt_num")
        lt_price = session.get("lt_price")
        op1 = "select id from buy_car where uname= '{}' and goods_name= '{}'".format(uname, "辣条")
        op2 = "insert into buy_car(uname, goods_name, goods_num, goods_price) values ({},{},{},{})".format(uname, "辣条", buy_lt_num, lt_price)
        op3 = "update buy_car set  goods_num = {} where goods_name = '{}' and uname = '{}'".format(buy_lt_num, '辣条', uname)
        ret = add_buy_car(op1,op2,op3)
        if ret:
            return "成功加入购物车"
        else:
            return "加入购物车失败"

@app.route("/kele_info",methods=["GET","POST"])
def kele_info():
    '''
        函数功能：进入可乐购买界面,加入购物车
        :return:
        '''
    uname = session.get("uname")
    kele_price = session.get("kele_price")
    if request.method == "GET":
        # print(uname)
        if uname:
            return render_template("kele.html", kele_num=kele_num, kele_price=kele_price, uname=uname)
        else:
            return "请先登录！"
    elif request.method == "POST":
        buy_kele_num = request.form.get("buy_kele_num")
        kele_price = session.get("kele_price")
        op1 = "select id from buy_car where uname= '{}' and goods_name= '{}'".format(uname, "可乐")
        op2 = "insert into buy_car(uname, goods_name, goods_num, goods_price) values ({},{},{},{})".format(uname, "可乐",
                                                                                                           buy_kele_num,
                                                                                                           kele_price)
        op3 = "update buy_car set  goods_num = {} where goods_name = '{}' and uname = '{}'".format(buy_kele_num, '可乐',
                                                                                                   uname)
        ret = add_buy_car(op1, op2, op3)
        if ret:
            return "成功加入购物车"
        else:
            return "加入购物车失败"

@app.route("/dounai_info",methods=["GET","POST"])
def dounai_info():
    '''
        函数功能：进入豆奶购买界面,加入购物车
        :return:
        '''
    uname = session.get("uname")
    dounai_price = session.get("dounai_price")
    if request.method == "GET":
        # print(uname)
        if uname:
            return render_template("dounai.html", dounai_num=dounai_num, dounai_price=dounai_price, uname=uname)
        else:
            return "请先登录！"
    elif request.method == "POST":
        buy_dounai_num = request.form.get("buy_dounai_num")
        dounai_price = session.get("dounai_price")
        op1 = "select id from buy_car where uname= '{}' and goods_name= '{}'".format(uname, "可乐")
        op2 = "insert into buy_car(uname, goods_name, goods_num, goods_price) values ({},{},{},{})".format(uname, "可乐",buy_dounai_num, dounai_price)

        op3 = "update buy_car set  goods_num = {} where goods_name = '{}' and uname = '{}'".format(buy_dounai_num, '可乐', uname)

        ret = add_buy_car(op1, op2, op3)
        if ret:
            return "成功加入购物车"
        else:
            return "加入购物车失败"

@app.route("/binggan_info",methods=["GET","POST"])
def binggan_info():
    '''
        函数功能：进入饼干购买界面,加入购物车
        :return:
        '''
    uname = session.get("uname")
    binggan_price = session.get("binggan_price")
    if request.method == "GET":
        # print(uname)
        if uname:
            return render_template("binggan.html", binggan_num=binggan_num, binggan_price=binggan_price, uname=uname)
        else:
            return "请先登录！"
    elif request.method == "POST":
        buy_binggan_num = request.form.get("buy_binggan_num")
        binggan_price = session.get("binggan_price")
        op1 = "select id from buy_car where uname= '{}' and goods_name= '{}'".format(uname, "饼干")
        op2 = "insert into buy_car(uname, goods_name, goods_num, goods_price) values ({},{},{},{})".format(uname, "饼干",buy_binggan_num, binggan_price)
        op3 = "update buy_car set  goods_num = {} where goods_name = '{}' and uname = '{}'".format(buy_binggan_num, '饼干', uname)
        ret = add_buy_car(op1, op2, op3)
        if ret:
            return "成功加入购物车"
        else:
            return "加入购物车失败"

@app.route("/buy_car", methods=["GET","POST"])
def buy_car():
    '''
    函数功能：进入购物车界面，修改购物车中的商品信息，提交修改，点击购买进入订单界面
    :return: 点击购买时，返回订单界面。点击提交修改时，返回修改后的购物车界面。
    '''
    uname = session.get("uname")
    session["uname"] = uname
    if request.method == "GET":
        # print("购物车用户",uname)
        if  uname:
            op = "select * from buy_car where uname= '{}'".format(uname)
            rows = conn_sql_2(op)
            if not rows:
                return "购物车为空！"
            else:
                return render_template("buy_car.html",rows=rows)
        else:
            return "请先登录！"
    elif request.method == "POST":
        print("提交购物车",uname)
        if uname:
            ready_buy = request.form.get("ready_buy")
            commit_changes = request.form.get("commit_changes")
            print(ready_buy,commit_changes)
            if ready_buy:
                user_address = request.form.get("address")
                print("收货地址",user_address)
                session["user_address"] = user_address
                op = "select * from buy_car where uname= '{}'".format(uname)
                rows = conn_sql_2(op)
                if not rows:
                    return "购物车为空！"
                else:
                    return render_template("order.html",rows=rows,address = user_address)
            elif commit_changes:
                change_goods_num = request.form.get("change_goods_num")
                change_goods_name = request.form.get("change_goods_name")
                print("修改的商品信息",change_goods_name,change_goods_num,type(change_goods_num),type(change_goods_name))
                op = "update buy_car set goods_num = {} where goods_name = '{}' and uname = '{}'".format(change_goods_num, change_goods_name, uname)
                conn_sql_2(op)
                op2 = "select * from buy_car where uname = '{}'".format(uname)
                rows = conn_sql_2(op2)
                return render_template("buy_car.html", rows=rows)
        else:
            return "请先登录！"

@app.route("/order")
def order():
    '''
    函数功能：进入我的订单界面
    :return:
    '''
    uname = session.get("uname")

    if uname:
        user_address = session.get("user_address")
        op = "select * from buy_car where uname= '{}'".format(uname)
        rows = conn_sql_2(op)
        return render_template("order.html", rows=rows, address=user_address)
    else:
        return "请先登录！"



if __name__ == '__main__':
    app.run(debug=True, port=80)