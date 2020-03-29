# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/17
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import hmac
import hashlib
from flask import Blueprint
from flask import render_template, request, current_app, abort, jsonify

from yblog.extensions import cache, csrf
from yblog.common.models import Tag, Post, Category
from yblog.common.RestResponse import RestResponse
from collections import OrderedDict

blog_bp = Blueprint('blog', __name__)


@blog_bp.route("/", methods=['GET'])
@cache.cached(query_string=True)
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.created.desc()).paginate(
        page, per_page=current_app.config['YBLOG_PER_PAGE'], error_out=True)
    posts = pagination.items
    return render_template('index.html',
                           posts=posts,
                           pagination=pagination
                           )


@blog_bp.route("/archives", methods=['GET'])
@cache.cached()
def archives():
    posts = Post.query.order_by(Post.created.desc())
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
@cache.cached(query_string=True)
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
@cache.cached(query_string=True)
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
@cache.cached()
def show_post(postid):
    p = Post.query.get_or_404(postid)
    return render_template('post.html',
                           post=p)


@csrf.exempt
@blog_bp.route("/yblg-github-moniter", methods=['POST'])
def yblg_github_moniter():
    if request.method == 'POST':
        signature = request.headers.get("X-Hub-Signature")
        if not signature or not signature.startswith("sha1="):
            abort(400, "X-Hub-Signature required")

        # Create local hash of payload
        github_webhook_secret = current_app.config['GITHUB_WEBHOOK_SECRET'].encode("utf-8")
        digest = hmac.new(github_webhook_secret,
                          request.data, hashlib.sha1).hexdigest()
        verify_signature = "sha1=" + digest
        current_app.logger.info("github request signature: {}".format(verify_signature))

        # Verify signature
        if not hmac.compare_digest(signature, verify_signature):
            abort(400, "Invalid signature")

        request_data = request.get_json()

        # We are only interested in push events from the a certain repo
        if request_data.get("repository", {}).get("name") != "YBlog":
            return jsonify(RestResponse.ok(msg='Dont care!')), 200

        # todo celery task
        # http://flask.pocoo.org/docs/1.0/patterns/celery/
        return jsonify(RestResponse.ok(msg='Success', code=200))
    else:
        abort(400)
