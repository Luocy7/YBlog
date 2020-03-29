from pathlib import Path
import re
from datetime import datetime, timedelta

from yblog import db
from yblog.database.models import Category, Post, Tag

nt_folder = Path(__file__).parent.absolute()
nt_input = nt_folder / 'input'
nt_export = nt_folder / 'export'
nt_input.mkdir(exist_ok=True)
nt_export.mkdir(exist_ok=True)


def file_divide(ntfile):
    with open(ntfile, 'r', encoding='utf-8') as nt_f:
        nt_content = nt_f.readlines()
        return nt_content[0:6], nt_content[6:]


def parse_head(headdata):
    tags = re.search(r'\[(.*)\]', headdata[1]).group(1).split(',')
    title = headdata[2].replace('title: ', '').strip().replace('\\', '-')
    created_str = headdata[3].replace('created: ', '').strip()[1:-1]
    modified_str = headdata[4].replace('modified: ', '').strip()[1:-1]
    created = utc2local(created_str)
    modified = utc2local(modified_str)
    return tags, title, created, modified


def utc2local(utcstr: str):
    utc_date = datetime.strptime(utcstr, "%Y-%m-%dT%H:%M:%S.%fZ")
    local_date = utc_date + timedelta(hours=8)
    return datetime.strftime(local_date, '%Y-%m-%d %H:%M:%S')


def fmtcontent(content):
    return ''.join(content)


def insert_cate():
    category = Category.query.first()
    if category is None:
        category = Category(name='Default')
        db.session.add(category)
    db.session.commit()


def insert_tag():
    tmp_tags = []
    for nt_file in nt_input.glob('*.md'):
        head, content = file_divide(nt_file)
        tags, _, _, _ = parse_head(head)
        for tag in tags:
            tmp_tags.append(tag.strip().replace('/', '-'))

    tmp_tags = list(set(tmp_tags))
    print(tmp_tags)

    for tag in tmp_tags:
        if not Tag.query.filter(Tag.name == tag).all():
            print('inject {}'.format(tag))
            tag = Tag(name=tag)
            db.session.add(tag)
        else:
            print('!!!!!!!!!!------{} Duplicate!-------!!!!!!!!!!'.format(tag))
    db.session.commit()


def insert_blogs():
    for nt_file in nt_input.glob('*.md'):
        head, content = file_divide(nt_file)
        tags, title, created, modified = parse_head(head)
        post = Post(
            title=title,
            content=fmtcontent(content),
            created=created,
            modified=modified,
            category=Category.query.filter(Category.name == 'Default').first()
        )

        for tag in tags:
            ntag = Tag.query.filter(Tag.name == tag.strip().replace('/', '-')).first()
            post.tags.append(ntag)

        db.session.add(post)
    db.session.commit()
