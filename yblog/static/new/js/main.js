;(function () {

    "use strict";
    // 返回顶部
    var goBack = function () {
        var back2top = $(".to-top-btn");

        $(window).scrollTop() > 500 ? back2top.addClass("show") : back2top.removeClass("show");

        $(window).scroll(function () {
            $(window).scrollTop() > 500 ? back2top.addClass("show") : back2top.removeClass("show");
        });
        back2top.click(function () {
            $("html, body").animate({
                scrollTop: 0
            }, 500);
            return false;
        });
    };

    var weclcomeback = function () {
        let OriginTitile = document.title, titleTime;
        document.addEventListener('visibilitychange', function () {
            if (document.hidden) {
                document.title = 'Luocy`s Blog';
                clearTimeout(titleTime);
            } else {
                document.title = 'Welcome Back! ╮(╯▽╰)╭';
                titleTime = setTimeout(function () {
                    document.title = OriginTitile;
                }, 2000);
            }
        });
    };

    var blueinput = function () {
        $("input[type=search]").each(function () {
            var searchForm = $(this).parent();
            var searchImg = $(this).next();
            $(this).focus(function () {
                searchForm.addClass("active");
                searchImg.attr("src","https://b-gold-cdn.xitu.io/v3/static/img/juejin-search-icon-focus.470748c.svg");
            });
            $(this).blur(function () {
                searchForm.removeClass("active");
                searchImg.attr("src","https://b-gold-cdn.xitu.io/v3/static/img/juejin-search-icon.6f8ba1b.svg");
            });
        });
    };

    $(function () {
        weclcomeback();
        goBack();
        blueinput();
    });

})();

