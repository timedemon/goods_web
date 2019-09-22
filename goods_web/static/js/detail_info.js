
//商品图片,鼠标点击切换展示
$('.fy-pro .left .sub-pic img').bind('mouseover',function(){
        $('.fy-pro .left .pic2 img').attr('src',$(this).attr('src'));
});

//购物篮
$(function aa() {
        $("#plus").click(function() {
            var n = $("#count").val(),
                num = parseInt(n) + 1;
            if(num == 0) {
                alert("cc");
            }
            $("#count").val(num);
        });
        $("#minis").click(function() {
            var n = $("#count").val(),
                num = parseInt(n) - 1;
            num = num < 1 ? 0 : num;
            $("#count").val(num);
        });
    });