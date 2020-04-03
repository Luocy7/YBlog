# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/14
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

from flask import render_template, flash, redirect, url_for, Blueprint, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from sqlalchemy import or_

from yblog.database.forms import LoginForm
from yblog.database.models import Admin
from yblog.utils import redirect_back
from yblog.utils.RestResUtil import RestResponse
from yblog.extensions import limiter

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("20/day;10/hour;5/minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.filter(or_(Admin.user_name == username,
                                       Admin.email == username
                                       )).first()
        if admin:
            if (username == admin.user_name
                    or username == admin.email)\
                    and admin.verify_password(password):
                login_user(admin, remember)
                return jsonify(RestResponse.ok(msg='Login Success'))
        return jsonify(RestResponse.fail(msg='请输入正确的用户名和密码'))
    return render_template('admin/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()
