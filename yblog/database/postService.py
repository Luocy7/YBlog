# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/31
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""
from sqlalchemy.exc import IntegrityError

from yblog import db
from yblog.database.models import Post, Tag, Category


class DBError(Exception):
    def __init__(self, errorinfo):
        super().__init__(self)
        self.errorinfo = errorinfo

    def __str__(self):
        return self.errorinfo


def get_or_create_cate_by_name(catename):
    _category = Category.query.filter(Category.name == catename).first()
    if not _category:
        try:
            category = Category(name=catename)
            db.session.add(category)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise DBError("Create Category <{}> Fail".format(catename))

        return category
    return _category


def get_or_create_tag_by_name(tagname):
    _tag = Tag.query.filter(Tag.name == tagname).first()
    if not _tag:
        try:
            tag = Tag(name=tagname)
            db.session.add(tag)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise DBError("Create Tag <{}> Fail".format(tagname))
        return tag
    return _tag


def create_post_by_name(data: dict):
    post_name = data.get('md_name')
    try:
        post = Post(
            mdname=post_name,
            title=data.get('md_title', post_name),
            content=data.get('md_content', '')
        )
        db.session.add(post)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise DBError("Create Post <{}> Fail -->Name or Title duplicate!".format(post_name))
    return post


def get_or_create_post_by_name(data: dict):
    _post = Post.query.filter(Post.mdname == data.get('md_name')).first()
    if not _post:
        return create_post_by_name(data)
    return _post


def update_post_by_name(data: dict):
    post = Post.query.filter(Post.mdname == data.get('md_name')).first()
    if post:
        post.title = data.get('md_title')
        post.created = data.get('md_created')
        post.modified = data.get('md_modified')
        post.content = data.get('md_content')

        try:
            tags = data.get('md_tags', '')
            if tags:
                for tag in tags:
                    _tag = get_or_create_tag_by_name(tag)
                    post.tags.append(_tag)

            db.session.add(post)
            db.session.commit()
        except IntegrityError as e:
            name = data.get('md_name')
            title = data.get('md_title')
            db.session.rollback()
            raise DBError('Update Post <{}> Fail --> Title <{}> duplicate!'.format(name, title))
    else:
        raise DBError('Post not found')


def update_or_create_post_with_data(data: dict):
    try:
        post = get_or_create_post_by_name(data)
        post.title = data.get('md_title')
        post.created = data.get('md_created')
        post.modified = data.get('md_modified')
        post.content = data.get('md_content')

        tags = data.get('md_tags', '')
        if tags:
            for tag in tags:
                _tag = get_or_create_tag_by_name(tag)
                post.tags.append(_tag)

        db.session.add(post)
        db.session.commit()
    except IntegrityError:
        name = data.get('md_name')
        title = data.get('md_title')
        db.session.rollback()
        raise DBError('Update Post <{}> Fail --> Title <{}> duplicate!'.format(name, title))


def delete_post_with_data(data: dict):
    post = Post.query.filter(Post.mdname == data['md_name']).first()
    if post:
        db.session.delete(post)
        db.session.commit()
    else:
        raise DBError('Post not found')


def change_postname_with_data(data: dict):
    post = Post.query.filter(Post.mdname == data['md_name']).first()
    if post:
        post.mdname = data.get('dest_name')
        db.session.add(post)
        db.session.commit()
    else:
        raise DBError('Post not found')
