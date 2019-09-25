
#!/usr/bin/python3
# -*- coding: utf-8 -*-


import re
import pymysql
import random
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import hashlib
from urllib import request
import  json
from urllib import  parse

'''
用户注册文件

'''

db_conf = json.load(open("server.json"))

# MD5加密
def get_passwd_md5(passwd):
    '''
    函数功能：将用户的密码用MD5加密
    参数描述：
        passwd:用户输入的密码
        :return 返回加密后的密码

    '''
    m = hashlib.md5()
    m.update(passwd.encode())
    print(m.hexdigest(), type(m.hexdigest()))
    return m.hexdigest()


# 得到用户名
def get_user_name():
    '''
    函数功能：得到用户名
    :return: 返回用户名
    '''
    user_name = input("请输入用户名(只能包含英文字母、数字下划线，最短6位，最长15位):\n")
    return user_name

# 得到密码
def get_user_passwd():
    '''
    函数功能：得到用户输入的密码
    :return: 返回用户密码
    '''
    while True:
        user_passwd = input("请输入密码(只能包含英文字母、数字下划线，最短6位，最长15位): \n")
        user_passwd2 = input("请再次输入密码：\n")
        if user_passwd == user_passwd2:
            break
        else:
            print("两次密码输入不同，请重新输入！")
    return user_passwd

# 得到手机号
def get_phone():
    '''
    函数功能：得到用户输入的手机号
    :return: 返回用户输入的手机号
    '''
    phone = input("请输入手机号：\n")
    return  phone

# 得到邮箱账号昵称，邮箱账号名
def get_email():
    '''
    函数功能：得到邮箱账号昵称，邮箱账号名
    函数参数：无
    :return:
             email_account: 邮箱账号名
    '''
    email_account = input("请输入邮箱账号名：\n")
    return  email_account


# 验证注册用户名格式以及数据库是否已存在用户名函数
def check_user_name(user_name):
    '''
    函数功能：验证注册用户名格式以及数据库师傅已存在函数
    函数参数：user_name：用户输入的用户名
    返回值：    1: 用户格式错误
                2: 用户名存在
                0：不存在:

    '''
    # [a-zA-Z0-9_]{6, 15}
    if not re.match("^\w{6,15}$", user_name):
        return 1
    elif re.match("^\w{6,15}$", user_name):
        # 创建对象，连接数据库
        try:
            conn = pymysql.connect(db_conf["db_server"], db_conf["db_user"], db_conf["db_password"], db_conf["db_name"])
        except Exception as e:
            print("连接出错！", e)
            raise e
        # 获取一个游标对象，用于执行sql语句
        try:
            with conn.cursor() as cur:

                # 执行任意支持的SQL语句

                sql = "select uname from shop_user where uname='{}'".format(user_name)
                cur.execute(sql)
                # 通过用游标获取结果
                rows = cur.fetchone()

                print(rows, type(rows))
        finally:
            # 关闭数据库
            conn.close()
        if rows:
            return 2
        else:
            return 0


# 验证注册密码格式函数
def check_user_passwd(user_passwd):
    '''
    函数功能：验证注册密码格式函数
    参数描述：user_passwd：用户注册时输入的密码
    返回值：1：密码格式错误
           2：密码格式正确

    '''
    if not re.match("^\w{6,15}$", user_passwd):
        return 1
    else:
        return 0

# 验证手机号格式函数
def check_phone(phone):
    '''
    函数功能：验证手机号格式函数
     参数描述：phone: 用户输入的手机号
     返回值：0：手机号格式正确
            1：手机号格式错误

    '''
    if re.match("\d{11}", phone):
        return 0
    else:
        return 1

# 调用验证密码格式、用户名格式、手机号格式函数
def check_login_msg():
    '''
    函数功能：循环调用验证密码格式、用户名格式、手机号格式函数，直到用户输入正确
    :return: 返回输入正确的用户名，密码，手机号
    '''
    while True:
        user_name= get_user_name()
        ret = check_user_name(user_name)
        print(ret)
        if not ret :
            print(123)
            break
        elif ret == 1:
            print("用户名格式错误，请重新输入！")

        elif ret == 2:
            print("用户名已存在，请重新输入！")

    while True:
        user_passed = get_user_passwd()
        ret = check_user_passwd(user_passed)
        if ret == 1:
            print("密码格式不对！")
        else:
            break
    while True:
        phone = get_phone()
        ret = check_phone(phone)
        if ret == 1:
            print("手机号格式不对！")
        else:
            break

    return user_name, user_passed, phone

# 发送邮箱验证码
def send_mail_security_code():
    '''
    函数功能：发送邮箱验证码
    函数参数：无
    返回值：email: 邮箱名
            security_code:邮箱验证码

    '''
    while True:
        email = get_email()
        l= []
        for i in range(6):
            a = chr(random.randint(65, 90))
            a_lower = chr(random.randint(97, 122))
            num = str(random.randint(0,9))
            one = random.choice([a, a_lower, num])
            l.append(one)
        security_code = ''.join(l)

        my_sender = '1417098555@qq.com'  # 发件人邮箱账号
        my_pass = 'apoclbggmfrvgdie'  # 发件人邮箱密码
        my_user = email # 收件人邮箱账号，我这边发送给自己
        ret = True
        try:
            msg = MIMEText(security_code, 'plain', 'utf-8')
            msg['From'] = formataddr(["周志勇", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(['zzy', my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "验证码查收！"  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print(e)
            ret = False
        if ret:
            print("\n邮箱验证码发送成功！")
            break
        else:
            print("\n验证码发送失败！请检查邮箱是否正确！")
    return email, security_code

# 发送手机验证码
def send_phone_security_code(phone):
    '''
    函数功能：发送短信验证码(6位随机数字)
    函数参数：
    phone 接收短信验证码的手机号
    返回值：发送成功返回验证码，失败返回False
    '''
    # while True:
    verify_code = str(random.randint(100000, 999999))
        # # phone = get_phone()
        # try:
        #     url = "http://v.juhe.cn/sms/send"
        #     params = {
        #         "mobile": phone,  # 接受短信的用户手机号码
        #         "tpl_id": "162901",  # 您申请的短信模板ID，根据实际情况修改
        #         "tpl_value": "#code#=%s" % verify_code,  # 您设置的模板变量，根据实际情况修改
        #         "key": "ab75e2e54bf3044898459cb209b195e4",  # 应用APPKEY(应用详细页查询)
        #     }
        #     params = parse.urlencode(params).encode()
        #     f = request.urlopen(url, params)
        #     content = f.read()
        #     res = json.loads(content)
        #
        #     if res and res['error_code'] == 0:
        #         # return verify_code, phone
        #         break
        #     else:
        #         print("短信发送失败，请输入正确的手机号！")
        #         # return False
        # except:
        #     print("短信发送失败，请检查网络环境！")

    return verify_code

# 循环让用户输入验证码核对验证码
def check_security_code(ret_ecode, ret_pcode):
    '''
    函数功能：循环让用户输入验证码，直到正确为止
    函数参数：ret_ecode:邮箱验证码
             ret_pcode:手机验证码
    '''
    while True:
        s = input("请输入邮箱验证码:(不区分大小写！)\n")
        if s.lower() == ret_ecode.lower():
            print("邮箱验证成功！")
            break
        else:
            print("验证码不对，请重新输入！")
    while True:
        s = input("请输入手机验证码: (不区分大小写！)\n")
        if s.lower() == ret_pcode.lower():
            print("手机验证成功！")
            break
        else:
            print("验证码不对，请重新输入！")

# 连接数据库,将用户信息写入数据库
def conn_sql(name, passwd, sex, interest, email, birth, edu):
    '''
    函数功能：连接数据库，将用户信息写入数据库
    参数描述：name:验证通过后的用户名
             passwd:验证通过后的密码
             pho:验证通过后的手机号
             ema:验证通过后的邮箱
    返回值：  True: 插入数据成功
    '''
    # 创建对象，连接数据库
    conn = pymysql.connect(db_conf["db_server"], db_conf["db_user"], db_conf["db_password"], db_conf["db_name"])

    with conn.cursor() as cur:
        try:
            # 执行任意支持的SQL语句
            sql = "insert into shop_user(uname, passwd, sex, interest, email, birth, edu) values ('{}', '{}', '{}', '{}','{}', '{}', '{}')".format(name, passwd, sex, interest, email, birth, edu)
            cur.execute(sql)
            # 提交事务
            conn.commit()
        except Exception as e:
            print("插入失败！",e)
            return False
        finally:
            # 关闭游标
            cur.close()
            # 关闭数据库
            conn.close()
    return True

# def register_main():
#     '''
#     函数功能：主函数，调用得到用户输入信息，发送验证码，插入数据函数
#
#     '''
#     # 得到用户输入信息
#     user_msg = check_login_msg()
#     user_name = user_msg[0]
#     user_passwd = user_msg[1]
#     phone = user_msg[2]
#     md5_passwd = get_passwd_md5(user_passwd)
#     print(user_msg)
#
#     # 发送验证码
#     ret1 = send_mail_security_code()
#     email = ret1[0]
#     email_security_code =  ret1[1]
#
#     # 写入数据库
#     ret2 = send_phone_security_code(phone)
#     phone = ret2[0]
#     phone_security_code = ret2[1]
#
#     check_security_code(email_security_code, phone_security_code)
#
#     conn_sql(user_name, md5_passwd, phone, email)
#
#
#
#
# if __name__ == '__main__':
#     register_main()
