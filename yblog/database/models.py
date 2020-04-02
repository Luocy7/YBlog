# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/17
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

from yblog.extensions import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(10), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(255), default='')
    avatar = db.Column(db.String(255), default='')
    level = db.Column(db.SmallInteger, default=0)

    @property
    def is_admin(self):
        return True if self.level > 0 else False

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def reset_password(self, old_password, new_password):
        if check_password_hash(self.password_hash, old_password):
            self.password = new_password
            return True
        return False

    def __repr__(self):
        return '<Admin %r>' % self.user_name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    posts = db.relationship('Post', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()


Post2Tag = db.Table("post2tag",
                    db.Column('id', db.Integer, primary_key=True),
                    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete="cascade")),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete="cascade"))
                    )


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    posts = db.relationship('Post', secondary=Post2Tag, back_populates='tags')

    def __repr__(self):
        return self.name


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    mdname = db.Column(db.String(255), unique=True, info='MdName', index=True)
    title = db.Column(db.String(255), unique=True, info='Title')
    cover_link = db.Column(db.String(255), default='', info='Post Cover Link')

    content = db.Column(db.TEXT(64000), info='Post Content')
    created = db.Column(db.DateTime(), default=datetime.now, info='Post Created Time')
    modified = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now, info='Post Last Modified Time')

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')
    tags = db.relationship('Tag', secondary=Post2Tag, back_populates='posts')

    is_published = db.Column(db.Boolean, default=True)

    post_day_views = db.relationship('PostDayView', backref='post_day_views', lazy='joined')
    post_total_views = db.Column(db.Integer, default=0)

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.__repr__()


class PostDayView(db.Model):
    __tablename__ = 'post_day_views'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    views = db.Column(db.Integer, default=0)
    visit_date = db.Column(db.Date(), default=date.today)

    def __repr__(self):
        return "On {} this post was total viewed {}".format(self.visit_date, self.views)


class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    link_avatar = db.Column(db.String(200), default='')
    link_name = db.Column(db.String(20))
    link_url = db.Column(db.String(100))
    link_type = db.Column(db.SmallInteger, default=0, info='0:Account Link, 1:Friend Link;')

    def showtype(self):
        if self.link_type:
            return "友链"
        else:
            return "普通"


class Site(db.Model):
    __tablename__ = 'site'
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(200))
    site_avatar = db.Column(db.String(200))
    site_record = db.Column(db.String(200))


class Visit(db.Model):
    """Page visit record."""
    __tablename__ = 'visits'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50))
    visit_time = db.Column(db.DateTime, default=datetime.now)
    visit_path = db.Column(db.String(50))
    visit_args = db.Column(db.JSON)
    referrer = db.Column(db.String(50))
    platform = db.Column(db.String(50))
    browser = db.Column(db.String(50))
    browser_version = db.Column(db.String(50))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
