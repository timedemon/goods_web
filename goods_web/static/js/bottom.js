

$(function(){
	var i = 0;//定义索引，图片和小圆点共用
	var timer;//定义定时函数
	$('.pic .img img').eq(0).show().siblings().hide();//定义默认的显示图片，也就是索引为0的那张图片
	start();//开始实现图片轮播，用到了定时器
	$('b').hover(function(){//当鼠标运动到某个小圆点是，切换图片
		clearInterval(timer);//并且清除定时
		i=$(this).index();//获取当前鼠标运动到的小圆点的索引
		change();//执行切换图片的函数
	});
    $('b').mouseleave(function(){
		start();//定义当鼠标离开小圆点时继续执行定时函数，轮播开始
	});


	function start(){//轮播开始函数
		timer = setInterval(function(){//自动轮播定时函数
			i++;//索引进行累加，防止图片只显示一张
			if(i==5){
				i=0;//我这里是用的8张图片，当索引为8时，图片没有了，将索引清零
			}
			change();//继续执行图片轮播
		},2000)//2000是多久切换一次图片，表示两秒
	}
	function change(){//图片显示函数，这里的fadeOut和fadeIn是图片显示方式是淡入淡出
		$('.pic .img img').eq(i).fadeIn(300).siblings().stop().fadeOut(300);//eq选择当前图片，siblings表示排除其他图片，stop表示其他图片停止切换，只切换当前图片
		$('b').eq(i).addClass('rudis').siblings().removeClass('rudis');//这里是设置小圆点的背景颜色改变，用的是添加类名的方法，因为我们在css文件里设置了当类名为‘rudis’时设置背景颜色为白色，其他的圆点设置为移除类名，所以其他的没有添加背景颜色
	}
});