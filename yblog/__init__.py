# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/29
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import os
import click

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from celery import Celery, platforms

from flask import Flask, render_template, has_request_context, request, redirect, url_for
from flask_sqlalchemy import get_debug_queries

from yblog.extensions import db, login_manager, csrf, mail, toolbar, migrate, md, cache
from yblog.database.models import Admin, Post, Category, Site, Link, Visit
from yblog.config.base_settings import config

from yblog.views.blog import blog_bp
from yblog.views.auth import auth_bp
from yblog.views.admin import admin_bp
from yblog.views.post_manage import post_manage

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
cfg = os.getenv('FLASK_CONFIG', 'prd')
platforms.C_FORCE_ROOT = True


def create_app(config_name=None):
    config_name = config_name or cfg

    app = Flask('yblog')

    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_views(app)
    register_commands(app)
    register_errors(app)
    reqister_ddl_events(app)
    register_shell_context(app)
    register_template_filter(app)
    register_template_context(app)
    register_request_handlers(app)

    return app


def register_celery(app):
    celery_instance = Celery()
    celery_instance.config_from_object('yblog.config.celery_cfg')

    class ContextTask(celery_instance.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    setattr(ContextTask, 'abstract', True)
    setattr(celery_instance, 'Task', ContextTask)

    return celery_instance


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            if has_request_context():
                record.url = request.url
                record.remote_addr = request.remote_addr
            else:
                record.url = None
                record.remote_addr = None

            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/yblog.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='YBlog Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)
    app.logger.addHandler(file_handler)


def register_extensions(app):
    # mail.init_app(app)
    # toolbar.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    md.init_app(app)
    cache.init_app(app)


def register_blueprints(app):
    @app.route("/")
    def index():
        return redirect(url_for("blog.index"), code=301)

    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')


def register_views(app):
    app.add_url_rule('/post/manage', view_func=post_manage, methods=['POST'])


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category)


def register_template_filter(app):
    @app.template_filter()
    def fmtdate(s, f='%Y-%m'):
        return s.strftime(f)

    @app.template_filter()
    def id2icon(s):
        icons = ["bg-ico-book", "bg-ico-game", "bg-ico-note", "bg-ico-chat", "bg-ico-code", "bg-ico-image",
                 "bg-ico-web", "bg-ico-link", "bg-ico-design", "bg-ico-lock"]
        return icons[int(s) % len(icons)]


def register_template_context(app):
    @app.template_global()
    def id2bg(post_id: int):
        total_bg_count = app.config['YBLOG_TOTAL_BG_COUNTS']
        return 'bg-{}.jpg'.format(str(post_id % total_bg_count + 1).zfill(2))

    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        site = Site.query.first()
        links = Link.query.all()
        return dict(
            gadmin=admin, gsite=site, glinks=links)


def register_errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.error(e)
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error(e)
        return render_template('errors/500.html'), 500


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= app.config['YBLOG_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response


def reqister_ddl_events(app):
    from sqlalchemy import event
    from sqlalchemy import DDL
    auto_incr_value = app.config['YBLOG_AUTO_INCREMENT_VALUE']
    event.listen(
        Post.__table__,
        "after_create",
        DDL("ALTER TABLE %(table)s AUTO_INCREMENT = {};".format(auto_incr_value))
    )


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def updatedb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('--> Drop tables.')
        db.create_all()
        click.echo('--> Database initialized !\nStart update data')

        from yblog.database.initDB import create_default_user, create_default_cate, update_posts_from_folder
        path = 'D:\\Project\\Notable\\notes'
        username = 'Luocy'
        password = 'Luocy'

        click.echo('--> Start create default user')
        create_default_user(username, password)
        click.echo('--> Create default user success !\n--> Start create default category')
        create_default_cate()
        click.echo('--> Create default category success !\n--> Start update posts')
        update_posts_from_folder(path)
        click.echo('--> Update posts success')
