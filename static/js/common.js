$(function(){
//  var browser={ 
//versions:function(){
// var u = navigator.userAgent, app = navigator.appVersion; 
// return {//移动终端浏览器版本信息 
// trident: u.indexOf('Trident') > -1, //IE内核 
// presto: u.indexOf('Presto') > -1, //opera内核 
// webKit: u.indexOf('AppleWebKit') > -1, //苹果、谷歌内核 
// gecko: u.indexOf('Gecko') > -1 && u.indexOf('KHTML') == -1, //火狐内核 
// mobile: !!u.match(/AppleWebKit.*Mobile.*/), //是否为移动终端 
// ios : !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/),
// android: u.indexOf('Android') > -1 ,  
// iPhone: u.indexOf('iPhone') > -1 , //是否为iPhone或者QQHD浏览器 
// iPad: u.indexOf('iPad') > -1, //是否iPad 
// webApp: u.indexOf('Safari') == -1 //是否web应该程序，没有头部与底部 
//};
//}(),
// language:(navigator.browserLanguage || navigator.language).toLowerCase() 
//}
//
// if(browser.versions.mobile || browser.versions.ios || browser.versions.android || 
// browser.versions.iPhone || browser.versions.iPad){ 
// window.location ="http://m.simplexue.com"; 
//}  
    
    //浏览器版本检测
var browserlow = $('<div class="browserlow">您的浏览器版本过低。为保证正常浏览及学习体验，请升级到IE9以上或更换为Chrome、火狐、safari等现代浏览器</div>');
if ( !-[1,] ) { 
    //alert("IE6-8"); 
    $("body").prepend(browserlow);
} else { 
   // alert("Not IE"); 
}

//个人设置下拉菜单
 $(".loginedCol #myCard,.loginOn #myCard").mouseover(function(){
    $(this).next(".my_list").fadeIn();
    $('.logined .my_card').addClass('hover');
  });
  $(".my_card").mouseleave(function(){
    $(this).children(".my_list").fadeOut();
     $('.logined .my_card').removeClass('hover');
  });
  //ajax加载   
     $("#ajaxloading").ajaxStart(function(){
        $(this).html("<img src='/images/loaded.gif';>");
      });
     $("#ajaxloading").ajaxSuccess(function(){
        $(this).html("");
        // $(this).empty(); // 或者直接清除
     });
	//点击登陆按钮 弹出
		
		//点击注册按钮 弹出
		$("#reg").click(function() {
			$("#maskLayer,#LogF").fadeIn(350);
			$('#tab-2').addClass("cur").siblings().removeClass("cur");
			$("#logbox").find(".login").eq(1).show().siblings().hide();
		});
		//点击忘记密码时
		$("#forgPass").click(function() {
			$("#maskLayer,#forgPassF").fadeIn(350);
			$("#LogF,#RegF,#getoverF").fadeOut();
		});
		//点击SignNow时
		$("#SignNow").click(function() {
			$("#maskLayer,#RegF").fadeIn(350);
			$("#LogF,#forgPassF,#getoverF").fadeOut();
		});
		//点击returnlog时
		$("#returnlog").click(function() {
			$("#maskLayer,#LogF").fadeIn(350);
			$("#RegF,#forgPassF,#getoverF").fadeOut();
		});
		//点击logInNow时
		$("#logInNow").click(function() {
			$("#maskLayer,#LogF").fadeIn(350);
			$("#RegF,#forgPassF,#getoverF").fadeOut();
		});
		//点击弹出关闭按钮，隐藏弹出窗    
		$(".LogCloseBtn,#getoverbtn").click(function() {
			$("#maskLayer,.embedWrap").fadeOut();
		});

		//登陆注册tab导航菜单效果
		$("#type_change_menu").find(".title_tab").click(function() {
			var $this = $(this);
			var $thisIndex = $this.index();
			$(this).addClass("cur").siblings().removeClass("cur");
			$("#logbox").find(".login").eq($thisIndex).show().siblings().hide();
		});
		//用户邀请码显示隐藏
		$("#role_type1").click(function() {
			$("#invitation").hide();
                        $("#invitation input").val('');
		});
		$("#role_type2").click(function() {
			$("#invitation").show();
		});
		//登陆注册文本框提示文字
		$(".formbox .input_txt").each(function() {
			var thisVal = $(this).val();
			//判断文本框的值是否为空，有值的情况就隐藏提示语，没有值就显示
			if (thisVal != "") {
				$(this).siblings(".placeholder").hide();
			} else {
				$(this).siblings(".placeholder").show();
			}
			//聚焦型输入框验证 
			$(this).focus(function() {
				$(this).siblings(".placeholder").hide();
			}).blur(function() {
				var val = $(this).val();
				if (val != "") {
					$(this).siblings(".placeholder").hide();
				} else {
					$(this).siblings(".placeholder").show();
				}
			});
		});
		//登陆注册弹出层end   
//返回顶部
$(window).scroll(function() {
	if ($(window).scrollTop() > 100) {
		$("#fixedTips").css('opacity', 1).css('right','15px');
	} else {
		$("#fixedTips").css('opacity', 0).css('right','-115px');
	}
});
$('#toTop').click(function() {
	$('body,html').animate({
		scrollTop: 0
	}, 500);
});
  /* Placeholders.js v4.0.1 */
!function(a){"use strict";function b(){}function c(){try{return document.activeElement}catch(a){}}function d(a,b){for(var c=0,d=a.length;d>c;c++)if(a[c]===b)return!0;return!1}function e(a,b,c){return a.addEventListener?a.addEventListener(b,c,!1):a.attachEvent?a.attachEvent("on"+b,c):void 0}function f(a,b){var c;a.createTextRange?(c=a.createTextRange(),c.move("character",b),c.select()):a.selectionStart&&(a.focus(),a.setSelectionRange(b,b))}function g(a,b){try{return a.type=b,!0}catch(c){return!1}}function h(a,b){if(a&&a.getAttribute(B))b(a);else for(var c,d=a?a.getElementsByTagName("input"):N,e=a?a.getElementsByTagName("textarea"):O,f=d?d.length:0,g=e?e.length:0,h=f+g,i=0;h>i;i++)c=f>i?d[i]:e[i-f],b(c)}function i(a){h(a,k)}function j(a){h(a,l)}function k(a,b){var c=!!b&&a.value!==b,d=a.value===a.getAttribute(B);if((c||d)&&"true"===a.getAttribute(C)){a.removeAttribute(C),a.value=a.value.replace(a.getAttribute(B),""),a.className=a.className.replace(A,"");var e=a.getAttribute(I);parseInt(e,10)>=0&&(a.setAttribute("maxLength",e),a.removeAttribute(I));var f=a.getAttribute(D);return f&&(a.type=f),!0}return!1}function l(a){var b=a.getAttribute(B);if(""===a.value&&b){a.setAttribute(C,"true"),a.value=b,a.className+=" "+z;var c=a.getAttribute(I);c||(a.setAttribute(I,a.maxLength),a.removeAttribute("maxLength"));var d=a.getAttribute(D);return d?a.type="text":"password"===a.type&&g(a,"text")&&a.setAttribute(D,"password"),!0}return!1}function m(a){return function(){P&&a.value===a.getAttribute(B)&&"true"===a.getAttribute(C)?f(a,0):k(a)}}function n(a){return function(){l(a)}}function o(a){return function(){i(a)}}function p(a){return function(b){return v=a.value,"true"===a.getAttribute(C)&&v===a.getAttribute(B)&&d(x,b.keyCode)?(b.preventDefault&&b.preventDefault(),!1):void 0}}function q(a){return function(){k(a,v),""===a.value&&(a.blur(),f(a,0))}}function r(a){return function(){a===c()&&a.value===a.getAttribute(B)&&"true"===a.getAttribute(C)&&f(a,0)}}function s(a){var b=a.form;b&&"string"==typeof b&&(b=document.getElementById(b),b.getAttribute(E)||(e(b,"submit",o(b)),b.setAttribute(E,"true"))),e(a,"focus",m(a)),e(a,"blur",n(a)),P&&(e(a,"keydown",p(a)),e(a,"keyup",q(a)),e(a,"click",r(a))),a.setAttribute(F,"true"),a.setAttribute(B,T),(P||a!==c())&&l(a)}var t=document.createElement("input"),u=void 0!==t.placeholder;if(a.Placeholders={nativeSupport:u,disable:u?b:i,enable:u?b:j},!u){var v,w=["text","search","url","tel","email","password","number","textarea"],x=[27,33,34,35,36,37,38,39,40,8,46],y="#ccc",z="placeholdersjs",A=new RegExp("(?:^|\\s)"+z+"(?!\\S)"),B="data-placeholder-value",C="data-placeholder-active",D="data-placeholder-type",E="data-placeholder-submit",F="data-placeholder-bound",G="data-placeholder-focus",H="data-placeholder-live",I="data-placeholder-maxlength",J=100,K=document.getElementsByTagName("head")[0],L=document.documentElement,M=a.Placeholders,N=document.getElementsByTagName("input"),O=document.getElementsByTagName("textarea"),P="false"===L.getAttribute(G),Q="false"!==L.getAttribute(H),R=document.createElement("style");R.type="text/css";var S=document.createTextNode("."+z+" {color:"+y+";}");R.styleSheet?R.styleSheet.cssText=S.nodeValue:R.appendChild(S),K.insertBefore(R,K.firstChild);for(var T,U,V=0,W=N.length+O.length;W>V;V++)U=V<N.length?N[V]:O[V-N.length],T=U.attributes.placeholder,T&&(T=T.nodeValue,T&&d(w,U.type)&&s(U));var X=setInterval(function(){for(var a=0,b=N.length+O.length;b>a;a++)U=a<N.length?N[a]:O[a-N.length],T=U.attributes.placeholder,T?(T=T.nodeValue,T&&d(w,U.type)&&(U.getAttribute(F)||s(U),(T!==U.getAttribute(B)||"password"===U.type&&!U.getAttribute(D))&&("password"===U.type&&!U.getAttribute(D)&&g(U,"text")&&U.setAttribute(D,"password"),U.value===U.getAttribute(B)&&(U.value=T),U.setAttribute(B,T)))):U.getAttribute(C)&&(k(U),U.removeAttribute(B));Q||clearInterval(X)},J);e(a,"beforeunload",function(){M.disable()})}}(this);

})
/**
 * 分页调用js
 * @param {type} data 后台ajax 数据
 * @param {type} method 
 * @param {type} type   方法中的参数类型
 * @returns {String}
 */
function getPaginator(data,method,type,tag,order)
{
      if (typeof type == "undefined") {
           type = "";
       }
      if (typeof tag == "undefined") {
           tag = "";
       }
      if (typeof order == "undefined") {
           order = "";
       }
       var pagerlink = "";
    //now, append with paginator partial
                if(data.paginator_last>1){
                     pagerlink = ' <ul class="pagination">';   
                    if(data.paginator_previous){
                        pagerlink +='<li class="previous" title="首页"><a href="javascript:void(0);" onclick="'+method+'(1,\''+type+'\',\''+tag+'\',\''+order+'\');">&nbsp;</a></li>';
                    }
                    if(data.paginator_previous){
                         pagerlink +='<li class="previous-btn" title="上一页"><a href="javascript:void(0);" onclick="'+method+'('+data.paginator_previous+',\''+type+'\',\''+tag+'\',\''+order+'\');">&nbsp;</a></li>';
                    }
                   $.each(data.paginator_pageRange, function(i, item) {
                        if (i == data.paginator_current) {
                          pagerlink +='<li class="active">'+i+'</li>';
                       } else {
                          pagerlink +='<li><a href="javascript:void(0);" onclick="'+method+'('+i+',\''+type+'\',\''+tag+'\',\''+order+'\')">'+i+'</a></li>';
                       }                    
                         });

                 if (data.paginator_next) {
                          pagerlink += '<li class="next-btn" title="下一页"><a href="javascript:void(0);" onclick="'+method+'('+data.paginator_next+',\''+type+'\',\''+tag+'\',\''+order+'\');">&nbsp;</a></li>';
                   } 
                  if (data.paginator_next) {
                          pagerlink += '<li class="next" title="末页"><a href="javascript:void(0);" onclick="'+method+'('+data.paginator_last+',\''+type+'\',\''+tag+'\',\''+order+'\');">&nbsp;</a></li>';
                   }
                    pagerlink +='</ul>'; 
                }
               
              return pagerlink;

}
/**
 * 带跳转的分页
 * @param data
 * @param method
 * @param type
 * @param jump
 * @returns {string}
 */
function getPaginatorRedirect(data,method,type,tag,order,jump)
{
	if (typeof type == "undefined") {
		type = "";
	}
	if (typeof tag == "undefined") {
		tag = "";
	}
	if (typeof order == "undefined") {
		order = "";
	}
	var pagerlink = "<div class='clear' style='clear: both;'></div><div class='pagerbar'>";
	if(data.paginator_last>1){
		pagerlink ="<div class='clear' style='clear: both;'></div><div class='pagerbar'>";
		if(data.paginator_previous){
			pagerlink +='<a class="first" href="javascript:void(0);" onclick="'+method+'(1,\''+type+'\',\''+tag+'\',\''+order+'\');"  title="首页">首页</a>';
		}
		if(data.paginator_previous){
			pagerlink +='<a class="" href="javascript:void(0);" onclick="'+method+'('+data.paginator_previous+',\''+type+'\',\''+tag+'\',\''+order+'\');">上一页</a>';
		}
		$.each(data.paginator_pageRange, function(i, item) {
			if (i == data.paginator_current) {
				pagerlink +='<a class="current" href="javascript:void(0);">'+i+'</a>';
			}else{
				pagerlink +='<a href="javascript:void(0);" onclick="'+method+'('+i+',\''+type+'\',\''+tag+'\',\''+order+'\')">'+i+'</a>';
			}
		});
		if (data.paginator_next) {
			pagerlink += '<a href="javascript:void(0);" onclick="'+method+'('+data.paginator_next+',\''+type+'\',\''+tag+'\',\''+order+'\');">下一页</a>';
		}
		if (data.paginator_next) {
			pagerlink += '<a class="last" href="javascript:void(0);" onclick="'+method+'('+data.paginator_last+',\''+type+'\',\''+tag+'\',\''+order+'\');" title="尾页">尾页</a>';
		}
		if(typeof jump == "undefined"){
			pagerlink +='&nbsp;&nbsp;跳转：<input class="pagenum" onkeypress="return IsNum(event)" type="text">&nbsp;&nbsp;页<a href="javascript:void(0);" onclick="return show('+data.paginator_last+','+'\''+method+'\',\''+type+'\',\''+tag+'\',\''+order+'\');">确定</a>';
		}
	}
	pagerlink+="</div></div>";
	return pagerlink;

}
function IsNum(e) {
	var k = window.event ? e.keyCode : e.which;
	if (((k >= 48) && (k <= 57)) || k == 8 || k == 0) {
	} else {
		if (window.event) {
			window.event.returnValue = false;
		}
		else {
			e.preventDefault(); //for firefox
		}
	}
}

function show (last,method,type,tag,order){
	var pagenum = $(".pagenum").val();
//        var reg='/.*[/u4e00-/u9fa5]+.*$/ ';
//        if (reg.test(pagenum)){
//            return false;
//        } 
	if(pagenum == undefined){
		pagenum = 1;
	}else if(pagenum > last){
		pagenum = last;
	}
	//console.log(method);
	eval(method+'('+pagenum+',"'+type+'","'+tag+'","'+order+'")');
}

function getEditor()
{   
			var editor;
			KindEditor.ready(function(K) {
				editor = K.create('textarea[name="content"]', {
                                        uploadJson : '/imagemanager/upload?type=2',
                                        cssPath: '/kindeditor/plugins/code/prettify.css',
					resizeType : 1,
					allowPreviewEmoticons : false,
                                        afterBlur:function(){
						this.sync(); 
                                            },
					allowImageUpload :true,
                                        allowImageRemote:false,
					items : [
						'code','|','fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
						'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
						'insertunorderedlist', '|', 'emoticons', 'image', 'link']
				});
			});		
}
function test1(obj)
{
	if(obj.value=="全角字符当做1个长度")
	{
		$.formValidator.getInitConfig("1").wideword = false;
		obj.value = "全角字符当做2个长度";
	}
	else
	{
		$.formValidator.getInitConfig("1").wideword = true;
		obj.value = "全角字符当做1个长度";
	}
        $('body').data(obj.validatorgroup,initConfig);
}
function stripscript(s){
       var pattern = new RegExp("[<><>]");
        var rs = "";
        for (var i = 0; i < s.length; i++) {
                rs = rs+s.substr(i, 1).replace(pattern, '');
        }
       return rs;
    }

//刷新验证码
function refreshCaptcha(obj){
	$.ajax({
		dataType: 'JSON', //数据类型
		type: "POST",
		url: "/user/refreshcaptcha",
		success: function (data) {
			$(obj).attr("src",data.imgSrc);
		}
	});
}
 