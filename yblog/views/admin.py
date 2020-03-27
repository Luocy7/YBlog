# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/14
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

from flask import render_template, Blueprint
from flask_login import login_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/index')
@login_required
def index():
    return render_template('admin/index_ex.html')


@admin_bp.route('/post')
@login_required
def post():
    return render_template('admin/post_list.html')


@admin_bp.route('/publish')
@login_required
def publish():
    return render_template('admin/post_edit.html')


@admin_bp.route('/category')
@login_required
def category():
    return render_template('admin/category.html')


@admin_bp.route('/attach')
@login_required
def attach():
    return render_template('admin/attach.html')


@admin_bp.route('/links')
@login_required
def links():
    return render_template('admin/links.html')


@admin_bp.route('/setting')
@login_required
def setting():
    return render_template('admin/setting.html')


@admin_bp.route('/profile')
@login_required
def profile():
    return render_template('admin/profile.html')
