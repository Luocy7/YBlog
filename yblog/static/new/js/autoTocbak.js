(function (window, $) {

    'use strict';

    function SideCatalog() {
        this.settings = {
            tocContainer: "#catalog",
            postContainer: "#article",
        };
        this.cateTopInit = $(".sticky-block-box").offset().top;

        this.createToc();

        this.bindClick();

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
                    console.log(cateDistance);
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

    window.SideCatalog = SideCatalog;

    $.fn.sideCatalog = function () {
        var calalog = new SideCatalog();
        return $(this);
    };

})(window, jQuery);

$('#sidetoc').sideCatalog();
