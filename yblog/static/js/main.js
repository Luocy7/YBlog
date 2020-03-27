;(function () {

    "use strict";
    // 返回顶部
    var goBack = function () {
        var rocket = $("#rocket");

        $(window).scroll(function () {
            $(window).scrollTop() > 500 ? rocket.addClass("show") : rocket.removeClass("show");
        });
        rocket.click(function () {
            $("#rocket").addClass("launch");
            $("html, body").animate({
                scrollTop: 0
            }, 500, function () {
                $("#rocket").removeClass("show launch");
            });
            return false;
        });

        $('#toc-up').click(function () {
            $('html, body').animate({
                scrollTop: $('#post-content').find("h2,h3,h4").first().offset().top
            }, 400);
        });
        $('#toc-down').click(function () {
            $('html, body').animate({
                scrollTop: $('#post-content').find("h2,h3,h4").last().offset().top
            }, 400);
        });
    };

    var postDirectory = new Headroom(document.getElementById("directory"), {
        tolerance: 0,
        offset: 100,
        classes: {
            initial: "initial",
            pinned: "pinned",
            unpinned: "unpinned"
        }
    });

    var hlnumber = function () {
        $("pre code").each(function () {
            $(this).html("<ol><li>" + $(this).html().replace(/\n/g, "\n</li><li>") + "\n</li></ol>");
        });
        $("code ol li:last-child").remove();
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

    $('article img').zoomify();

    $(document).ready(function () {
        $('pre code').each(function (i, block) {
            hljs.highlightBlock(block);
        });
    });

    $(function () {
        postDirectory.init();
        hlnumber();
        weclcomeback();
        goBack();
    });

})();

