# -*- coding: utf-8 -*-

import os
import click

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from celery import Celery

from flask import Flask, render_template, has_request_context, request
from flask_sqlalchemy import get_debug_queries

from yblog.views.blog import blog_bp
from yblog.views.auth import auth_bp
from yblog.views.admin import admin_bp

from yblog.extensions import bootstrap, db, login_manager, csrf, mail, moment, toolbar, \
    migrate, md, redis_client, cache
from yblog.common.models import Admin, Post, Category, Site, Link, Visit
from yblog.config.base_settings import config
from yblog.config.celeryconfig import broker_url
celery = Celery(__name__, broker=broker_url)
celery.config_from_object('yblog.config.celeryconfig')

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
cfg = os.getenv('FLASK_CONFIG', 'default')


def create_app(config_name=None):
    config_name = config_name or cfg

    app = Flask('yblog')

    app.config.from_object(config[config_name])

    register_celery(app)
    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    reqister_ddl_events(app)
    register_shell_context(app)
    register_template_filter(app)
    register_template_context(app)
    register_request_handlers(app)
    return app


def register_celery(app):

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask


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
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.NOTSET)

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
    # bootstrap.init_app(app)
    # mail.init_app(app)
    # moment.init_app(app)
    # toolbar.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    md.init_app(app)
    redis_client.init_app(app)
    cache.init_app(app)
    from yblog.utils.analytis import analytis
    analytis.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')


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
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
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
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--tag', default=20, help='Quantity of tags, default is 20.')
    def forge(category, post, tag):
        """Generate fake data."""
        from yblog.utils.fakes import fake_admin, fake_categories, fake_posts, fake_links, fake_tags

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d tags...' % tag)
        fake_tags(tag)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating links...')
        fake_links()

        click.echo('Done.')

    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def inject(drop):
        """inject data into database."""
        from Notable.MdFileTools import insert_cate, insert_tag, insert_blogs

        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')

        db.create_all()

        admin = Admin()
        admin.user_name = 'Luocy'
        admin.email = 'luocy77@gmail.com'
        admin.password = input("Please input Admin Password : ")
        db.session.add(admin)
        db.session.commit()

        click.echo('Start inject Categories')
        insert_cate()
        click.echo('Start inject Tags')
        insert_tag()
        click.echo('Start inject Blogs')
        insert_blogs()
        click.echo('Inject Done!')
