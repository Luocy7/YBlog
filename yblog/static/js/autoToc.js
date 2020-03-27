(function (window, $) {

    'use strict';

    function SideCatalog(wrapper, options) {
        var defaults = {
            tocContainer: "#toc",
            postContainer: "#post-content", // 文章内容容器ID
        };

        this.settings = $.extend(defaults, options);

        this.$wrapper = $(wrapper);

        this.mouseUpDown = true;
        this.timer = null;

        this.createToc();

        this.bindClick();

        this.bindEvents();
    }

    SideCatalog.prototype = {
        createToc: function () {
            var arr = ["<dl>"];
            var tocLevelClass,
                tagName,
                dotHtml;

            var titleA = $(this.settings.postContainer).find("h2,h3,h4");

            if (!titleA.get(0)) {
                $('#directory').css('visibility', 'hidden');
            }

            titleA.each(function (index, item) {
                if ("h2" === $(item).prop("tagName").toLowerCase()) {
                    tagName = 'dt';
                    tocLevelClass = 'level1';
                    dotHtml = '<em class="dot"></em>';
                } else if ("h3" === $(item).prop("tagName").toLowerCase()) {
                    tagName = 'dd';
                    tocLevelClass = 'level2';
                    dotHtml = '';
                } else {
                    tagName = 'dd';
                    tocLevelClass = 'level3';
                    dotHtml = '';
                }
                var node = '<' + tagName + ' class="toc-title ' + tocLevelClass + '">' + dotHtml +
                    '<a class="toca" href=\'javascript:void(0)\'>' + $(item).text() + '</a></' + tagName + '>';
                arr.push(node);
            });
            arr.push("<a class=\"arrow\" href=\"javascript:void(0)\"></a></dl>");
            $(this.settings.tocContainer).html(arr.join(""));
        },

        bindClick: function () {
            var titleArr = $(this.settings.postContainer).find("h2,h3,h4");
            var categoriesNav = $(this.settings.tocContainer);
            categoriesNav.find(".toca").each(function (index, domEle) {
                $(domEle).parent().on("click", function () {
                    $(window).scrollTop(titleArr.eq(index).offset().top);
                });
            });
        },

        bindEvents: function () {
            var _this = this;

            this.initCatalogUpDown();

            //文档滚动事件
            $(document).scroll(function () {
                _this.locateCataByContent();
            });
        },

        initCatalogUpDown: function () {
            function mouseScrollhandler(e) {
                e.stopPropagation();
                e.cancelBubble = true;
                e.preventDefault();

                if (!_this.mouseUpDown) {
                    return false;
                }

                _this.mouseUpDown = false;
                clearTimeout(_this.timer);
                _this.timer = setTimeout(function () { // 防止鼠标连续滚动导致的目录滚动bug
                    _this.mouseUpDown = true;
                }, 200);

                e = e || window.event;
                if (e.wheelDelta >= 0 || e.detail < 0) {
                    _this.scrollElement($('#toc'), 25.6 * 8, 'up', 0);
                } else {
                    _this.scrollElement($('#toc'), 25.6 * 8, 'down', 0);
                }
            }

            var _this = this;

            // 目录内容很长需要滚动显示时
            setTimeout(function () {
                var $toc = $('#toc');
                var tocHeight = $('#toc').height();
                var listHeight = $('#toc').find('dl').height();
                if (listHeight > tocHeight) {
                    $('#sidetoc').mouseover(function (e) {
                        _this.setUpDownClass();
                        $('#toc-updown').css('visibility', 'visible');
                        e.stopPropagation();
                    }).mouseout(function (e) {
                        $('#toc-updown').css('visibility', 'hidden');
                        e.stopPropagation();
                    });

                    // 鼠标滚轮事件在标准下和IE下是有区别的。
                    // firefox是按标准实现的,事件名为"DOMMouseScroll",IE下采用的则是"mousewheel"。
                    // 事件属性，IE是event.wheelDelta，Firefox是event.detail
                    // 属性的方向值也不一样，IE向上滚 > 0，Firefox向下滚 > 0。
                    // Firefox
                    if (document.addEventListener) {
                        document.getElementById('toc').addEventListener('DOMMouseScroll', mouseScrollhandler, false);
                    }
                    // IE/Chrome/Safari/Opera
                    document.getElementById('toc').onmousewheel = mouseScrollhandler;
                } else {
                    $('#toc-updown').css('display', 'none');
                }
            }, 1000);
        },

        setUpDownClass: function () {
            var $toc = $('#toc');
            var $tocUp = this.$wrapper.find('#toc-up');
            var $tocDown = this.$wrapper.find('#toc-down');
            if ($toc.height() + $toc.scrollTop() > $toc[0].scrollHeight - 5) {
                $tocUp[0].className = 'toc-up-enable';
                $tocDown[0].className = 'toc-down-disable';
            } else {
                if ($toc.scrollTop() < 5) {
                    $tocUp[0].className = 'toc-up-disable';
                    $tocDown[0].className = 'toc-down-enable';
                } else {
                    $tocUp[0].className = 'toc-up-enable';
                    $tocDown[0].className = 'toc-down-enable';
                }
            }
        },

        scrollElement: function (ele, jump, dir, dur) {
            var _this = this;
            dur = dur || 300;
            var top = ('down' === dir) ? ($(ele).scrollTop() + jump) : ($(ele).scrollTop() - jump);
            $(ele).animate({scrollTop: top }, dur, 'linear', function () {
                _this.setUpDownClass();
            });
        },


        // 根据当前document显示的内容定位目录项
        locateCataByContent: function () {
            var postContainer = $(this.settings.postContainer);
            var tocList = postContainer.find("h2,h3,h4");
            var scrollTop = $(document).scrollTop();
            var tocDl = $('#toc dl');
            var toc = tocDl.children();

            for (var i = 0, len = tocList.length; i < len; i++) {
                var ele = tocList[i],
                    ele1 = tocList[i + 1];
                // 判断当前滚动位置的内容属于哪条目录或子目录
                if ($(ele).offset().top - 20 <= scrollTop && ((i + 1 === len) || ((i + 1 < len) && $(ele1).offset().top > scrollTop))) {
                    tocDl.find('.highlight').removeClass('highlight');
                    $('#toc dl:eq(i)').addClass('highlight');

                    var top = 6 + i * 25.6;
                    top = top > tocDl.height() ? tocDl.height() : top;

                    $('#toc .arrow').stop().animate({'top': top + 'px'}, 100);

                    // 根据sideCatalog当前定位滚动其到合适位置以保证当前选中目录条目在目录中间位置
                    ele.order = i + 1;
                    if (ele.order > 5) {
                        $('#toc').stop().animate({'scrollTop': (ele.order - 5) * 25.6}, 100);
                    } else {
                        $('#toc').stop().animate({'scrollTop': 0}, 100);
                    }
                }
            }
        }
    };

    window.SideCatalog = SideCatalog;

    $.fn.sideCatalog = function (options) {
        var calalog = new SideCatalog(this, options);
        return $(this);
    };

})(window, jQuery);

$('#sidetoc').sideCatalog();