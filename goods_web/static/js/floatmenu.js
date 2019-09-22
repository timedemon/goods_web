

$(".fy-header .menu .ctx .bigmenu").bind("mouseover",function(){
    $(".fy-header .menu .floatmenu").fadeIn()
});
$(".fy-header .menu .floatmenu").bind("mouseleave",function(){
    $(this).fadeOut()
});