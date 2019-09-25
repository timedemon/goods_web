"use strict";

// 向后端发送手机号
$(function () {

    var can_submit = false;
    $("form").submit(function () {
       return can_submit
    });

   $("#send_phone_code").click(function () {
       //校验手机号格式
       var phone = $("#phone").val();
       if (!/1\d{10}/.test(phone)) {
           // alert("手机号格式错误！");
            $("#phone_tips").text("手机号格式错误！");
            $("#phone_tips").css("color","red");
           $("#phone").focus();
           can_submit = false;
           return;
       } else if (/1\d{10}/.test(phone)) {
            $("phone_tips").hidden;
           $("#phone").focus();
       }
       // 通过Ajax将手机号发送给服务器后端程序
    $.ajax({
        url: "/send_phone_code",
        data: {
            phone: phone
        },
        success: function (data) {
            if (data.err === 0) {
                alert("短信发送成功！")
            }else if (data.err === 1) {
                // alert("请输入正确的手机号！")
                $("#phone_tips").text("请输入正确的手机号！");
                $("#phone_tips").css("color","red");
            }
        },
        error: function () {
            alert("短信发送失败！请检查网络！")
        }
    });
       var s = 10;
       $("#send_phone_code").prop("disabled", true);
       $("#send_phone_code").html(s + "S");

       var timer = window.setInterval(function () {
           --s;
           if (s === 0) {
               window.clearInterval(timer);
               $("#send_phone_code").html("重新发送！");
               $("#send_phone_code").prop("disabled", false)
           }
       }, 1000);
   });

   // 向后端发送用户名
   $('input[name="uname"]').blur(function () {
        var uname = $("#uname").val();

    $.ajax({
        type:"GET",
        // contentType:"application/json;charset=UTF-8",
        dataType:"json",
        url: "/check_uname",
        data: {
            uname: uname
        },
        success: function (data) {
            if (data.uname_format === 1) {
                $("#uname_tips").text("用户名格式错误！");
                $("#uname_tips").css("color","red");
                can_submit = false;
            } else if (data.uname_format === 2) {
                $("#uname_tips").text("用户名已存在！");
                $("#uname_tips").css("color","red");
                can_submit = false;
            }else if(data.uname_format === 0) {
                $("#uname_tips").text("用户名可用！");
                $("#uname_tips").css("color","green");
                can_submit = true;
            }
        },
        error: function () {
            alert("注册信息发送失败！请检查网络！")
        }
    });
    });



});



$(function () {
    // 接收后端发送过来的验证码校验和是否注册成功的消息
    $("#submit").click(function () {
        // var can_submit = false;
        var phone_code = $("#phone_code").val();
        var uname = $('#uname').val();
        var password = $('#password').val();
        var sex = $('input[name="sex"]').val();
        var favorite = $('input[name="favorite"]').val();
        var email = $('input[name="email"]').val();
        var phone = $('input[name="phone"]').val();
        var edu = $('#edu').val();
        var birth = $('#birth').val();

       console.log(phone_code);
    $.ajax({
        type:"GET",
        contentType:"application/json;charset=UTF-8",
        dataType:"json",
        url: "/check_reg",
        data: {
            uname: uname,
            phone_code: phone_code,
            password:password,
            sex: sex,
            phone: phone,
            favorite: favorite,
            email: email,
            edu:edu,
            birth:birth
        },
        success: function (data) {
            console.log(data);
            if (data['phone_code'] === 1) {
                console.log("验证码");
                $("#phone_code_tips").text("验证码错误！");
                $("#phone_code_tips").css("color","red");
            }else if (data['phone_code']=== 0) {

                $("#phone_code_tips").text("√");
                $("#phone_code_tips").css("color","green");
                console.log("12");
                if (data['reg'] === 1) {
                    // console.log("12");
                alert("注册失败！");
                }else if (data['reg'] === 0) {
                alert("注册成功！");
                window.location.href='/login';
                }
                // console.log("13");
            }
        },
        error: function (data) {
            console.log(type(data));
            alert("接收消息失败！")
        }
    });
    });
});
