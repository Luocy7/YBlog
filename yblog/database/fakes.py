# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/17
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from yblog import db
from yblog.database.models import Admin, Category, Post, Link, Tag

fake = Faker()


def fake_admin():
    admin = Admin()
    admin.user_name = 'luocy'
    admin.email = 'luocy77@gmail.com'
    admin.password = 'luocy'
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_tags(count=20):
    for i in range(count):
        tag = Tag(name=fake.word())
        db.session.add(tag)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            slug=fake.sentence(),
            content=fake.text(2000),
            created=fake.date_time_this_year(),
            modified=fake.date_time_this_year(),
            category=Category.query.get(random.randint(1, Category.query.count()))
        )
        for index in range(random.randint(1,2)):
            tag = Tag.query.get(random.randint(1, Tag.query.count()))
            post.tags.append(tag)

        db.session.add(post)
    db.session.commit()


def fake_links():
    twitter = Link(link_name='Twitter', link_url='#')
    facebook = Link(link_name='Facebook', link_url='#')
    linkedin = Link(link_name='LinkedIn', link_url='#')
    google = Link(link_name='Google+', link_url='#')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()
