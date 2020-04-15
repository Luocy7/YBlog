# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/04/06
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

from pathlib import Path
from misaka import Markdown, HtmlRenderer, HtmlTocRenderer


class CustomRenderer(HtmlRenderer):
    def link(self, content, link, title=''):
        return '<a href="{}" target="_blank">{}</a>'.format(link, content)


class Md2Html:
    _ext = ('fenced-code', 'tables', 'autolink', 'underline', 'quote')

    def __init__(self, nesting_level=4, md_ext=_ext):
        # self.rndr = HtmlRenderer(nesting_level=nesting_level)
        self.rndr = CustomRenderer(nesting_level=nesting_level)
        self.tocrndr = HtmlTocRenderer(nesting_level=nesting_level)

        self.md = Markdown(self.rndr, extensions=md_ext)
        self.toc = Markdown(self.tocrndr, extensions=('fenced-code', 'autolink', 'underline'))

    def ge_toc(self, md_contont):
        return self.toc(md_contont)

    def get_html(self, md_contont):
        return self.md(md_contont)


ext = ('fenced-code', 'tables', 'autolink', 'underline', 'quote')

m = Md2Html(4, ext)

if __name__ == '__main__':
    mdfile = Path("C:\\Users\\y1297\\Desktop\\test.md")
    htmlfile = Path("C:\\Users\\y1297\\Desktop\\test.html")
    tocfile = Path("C:\\Users\\y1297\\Desktop\\toc.html")

    mdtext = mdfile.read_text(encoding="utf-8")

    htmlfile.write_text(m.get_html(mdtext), encoding="utf-8")
    tocfile.write_text(m.ge_toc(mdtext), encoding="utf-8")
