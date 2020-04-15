# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/17
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

from flask import Blueprint
from flask import render_template, request, current_app, abort

from yblog.extensions import cache, limiter
from yblog.database.models import Tag, Post, Category
from collections import OrderedDict

blog_bp = Blueprint('blog', __name__)


@blog_bp.route("/", methods=['GET'])
# @cache.cached(query_string=True)
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.is_published).order_by(Post.created.desc()).paginate(
        page, per_page=current_app.config['YBLOG_PER_PAGE'], error_out=True)
    posts = pagination.items
    return render_template('index.html',
                           posts=posts,
                           pagination=pagination
                           )


@blog_bp.route("/archives", methods=['GET'])
# @cache.cached()
def archives():
    posts = Post.query.filter(Post.is_published).order_by(Post.created.desc())
    archive_dict = group_posts_by_date(posts)
    return render_template("archives.html", archives=archive_dict)


def group_posts_by_date(posts):
    post_dict = OrderedDict()
    for p in posts:
        year_month = p.created.strftime("%Y-%m")
        if post_dict.get(year_month, None) is None:
            post_dict[year_month] = [p]
        else:
            post_dict[year_month].append(p)
    return post_dict


@blog_bp.route("/about", methods=['GET'])
@cache.cached()
def about():
    return render_template('about.html')


@blog_bp.route("/category/<string:cate>", methods=["GET"])
# @cache.cached(query_string=True)
def category(cate):
    page = request.args.get('page', 1, type=int)
    cate = Category.query.filter(Category.name == cate).first()
    if cate:
        pagination = Post.query.filter(Post.category == cate).paginate(
            page, per_page=current_app.config['YBLOG_CATE_PER_PAGE'], error_out=True)

        posts = pagination.items
        return render_template('page-category.html',
                               category=cate,
                               posts=posts,
                               pagination=pagination
                               )
    else:
        abort(404)


@blog_bp.route("/tag/<string:tag>", methods=["GET"])
# @cache.cached(query_string=True)
def show_tag(tag):
    page = request.args.get('page', 1, type=int)
    tag = Tag.query.filter(Tag.name == tag).first()
    if tag:
        pagination = Post.query.filter(Post.tags.contains(tag)).paginate(
            page, per_page=current_app.config['YBLOG_TAG_PER_PAGE'], error_out=True)

        posts = pagination.items
        return render_template('page-tag.html',
                               tag=tag,
                               posts=posts,
                               pagination=pagination
                               )
    else:
        abort(404)


@blog_bp.route("/post/<int:postid>", methods=['GET'])
# @cache.cached()
def show_post(postid):
    p = Post.query.get_or_404(postid)
    return render_template('post.html',
                           post=p)


@blog_bp.route("/p/<int:postid>", methods=['GET'])
@limiter.exempt
def show_article(postid):
    p = Post.query.get_or_404(postid)
    return render_template('new/post.html',
                           post=p)