;(function () {

    "use strict";

    var headerAction = new Headroom(document.getElementById("header"), {
        tolerance: 0,
        offset: 50,
        classes: {
            initial: "initial",
            pinned: "pinned",
            unpinned: "unpinned",
            top: "top",
            notTop: "not-top",
            notBottom: "not-bottom"
        }
    });

    var sidebarAction = new Headroom(document.getElementById("sidebar"), {
        tolerance: 0,
        offset: 300,
        classes: {
            initial: "sidebar",
            pinned: "pinned",
            unpinned: "unpinned",
            top: "top",
            notTop: "not-top",
            notBottom: "sidebar"
        }
    });


    var cateTopInit = $(".sticky-block-box").offset().top;

    var sidebarInit = function () {
        var sidebar = $("#sidebar");
        var cateDistance = $(document).scrollTop() - cateTopInit + 1;
        cateDistance > 0 ? sidebar.addClass("sticky") : sidebar.removeClass("sticky");
    };

    var sidebarScrollInit = function () {
        var tocList = $(".catalog-list");
        var tocListHeight = tocList.height();
        if (tocListHeight > $(window).height()) {
            var activeToc = document.getElementsByClassName("toc-title active");

            if (activeToc[0]) {
                var activeHeight = activeToc[0].offsetTop;

                var acDistance = $(window).height() * 2 / 5 - activeHeight;

                if (acDistance < 0) {
                    tocList.css("margin-top", acDistance + "px");
                } else {
                    tocList.css("margin-top", "0");
                }
            }
        }
    };

    var sidebarSticky = function () {
        $(window).scroll(function () {
            sidebarInit();
            sidebarScrollInit();
        });
    };

    var postHandle = function () {
        let article = document.getElementById("article");

        let postA = article.querySelectorAll("a");

        let header1 = article.querySelectorAll("h1");

        if (header1[0]) {
            header1[0].parentNode.removeChild(header1[0]);
        }

        let header2 = article.querySelectorAll("h2");

        for (let i = 0; i < postA.length; i++) {
            postA[i].setAttribute('target', '_blank');
            postA[i].setAttribute('rel', 'noopener noreferrer nofollow');
        }


        for (let i = 0; i < header2.length; i++) {
            let spanNode1 = document.createElement("span");
            let spanNode2 = document.createElement("span");
            let textNode = document.createTextNode(header2[i].innerText);
            spanNode1.appendChild(textNode);
            header2[i].innerText = "";
            header2[i].appendChild(spanNode1);
            header2[i].appendChild(spanNode2);
        }


    };

    function SideCatalog() {
        this.settings = {
            tocContainer: "#catalog",
            postContainer: "#article",
        };
        this.cateTopInit = $(".sticky-block-box").offset().top;

        this.createToc();

        this.bindClick();

        this.locateCataByContent();

        this.bindEvents();
    }

    SideCatalog.prototype = {
        createToc: function () {
            var arr = ["<dl class='catalog-list'>"];
            var tocLevelClass,
                tagName;

            var titleA = $(this.settings.postContainer).find("h2,h3,h4");

            if (!titleA.get(0)) {
                $('.sticky-block-box').css('visibility', 'hidden');
            }

            titleA.each(function (index, item) {
                if ("h2" === $(item).prop("tagName").toLowerCase()) {
                    tagName = 'dt';
                    tocLevelClass = 'level1';
                } else if ("h3" === $(item).prop("tagName").toLowerCase()) {
                    tagName = 'dd';
                    tocLevelClass = 'level2';
                } else {
                    tagName = 'dd';
                    tocLevelClass = 'level3';
                }
                var node = '<' + tagName + ' class="toc-title ' + tocLevelClass + '">' +
                    '<a class="toca" href=\'javascript:void(0)\'>' + $(item).text() + '</a></' + tagName + '>';
                arr.push(node);
            });
            $(this.settings.tocContainer).html(arr.join(""));
        },

        bindClick: function () {
            var _this = this;
            var titleArr = $(this.settings.postContainer).find("h2,h3,h4");
            var categoriesNav = $(this.settings.tocContainer);
            var sidebar = $("#sidebar");
            categoriesNav.find(".toca").each(function (index, domEle) {
                $(domEle).parent().on("click", function () {
                    $(window).scrollTop(titleArr.eq(index).offset().top - 100);
                    var cateDistance = $(document).scrollTop() - _this.cateTopInit + 1;
                    cateDistance > 0 ? sidebar.addClass("sticky") : sidebar.removeClass("sticky");
                });
            });
        },

        bindEvents: function () {
            var _this = this;

            //文档滚动事件
            $(document).scroll(function () {
                _this.locateCataByContent();
            });
        },


        // 根据当前document显示的内容定位目录项
        locateCataByContent: function () {
            var postContainer = $(this.settings.postContainer);
            var headerList = postContainer.find("h2,h3,h4");
            var scrollTop = $(document).scrollTop();
            var tocList = $('.catalog-list');

            for (var i = 0, len = headerList.length; i < len; i++) {
                var ele = headerList[i],
                    eleNext = headerList[i + 1];
                // 判断当前滚动位置的内容属于哪条目录或子目录
                if ($(ele).offset().top - 101 <= scrollTop && ((i + 1 === len) || ((i + 1 < len) && $(eleNext).offset().top > scrollTop))) {

                    tocList.find('.active').removeClass('active');
                    tocList.children().eq(i).addClass('active');
                }
            }
        }
    };

    $(function () {
        postHandle();
        var calalog = new SideCatalog();
        sidebarInit();
        sidebarScrollInit();
        sidebarSticky();
        headerAction.init();
        sidebarAction.init();
    });

})();