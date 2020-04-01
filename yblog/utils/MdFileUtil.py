from pathlib import Path
import re
from datetime import datetime, timedelta


class MdFile(object):

    def __init__(self, mdfile: str):
        self.mdpath = Path(mdfile)
        self.file_name = self.mdpath.stem
        self.file_content = None

        self.head_data = ''
        self.title = ''
        self.tags = []
        self.created = None
        self.modified = None

        self.content = None
        self.read_file()

    def to_dict(self):
        return {
            "md_name": self.file_name,
            "md_title": self.title,
            "md_created": self.created,
            "md_modified": self.modified,
            "md_tags": self.tags,
            "md_content": self.content
        }

    def read_file(self):
        with open(self.mdpath, 'r', encoding='utf-8') as f:
            self.file_content = f.readlines()

    def divided_head(self):
        self.head_data = []
        _tmp = [_line.strip() for _line in self.file_content[0:10]]
        line = _tmp.pop(0)
        if line == "---":
            index = 1
            while _tmp:
                line = _tmp.pop(0)
                index += 1
                if line == "---":
                    self.head_data = [meta.strip() for meta in self.file_content[1:index - 1] if meta.strip()]
                    self.content = "".join(self.file_content[index:])
                    break
            pass
        else:
            pass

    def parse_head(self):
        for line in self.head_data:
            if line.startswith('title'):
                self.title = line.replace('title: ', '').strip().replace('\\', '-')
            elif line.startswith('created'):
                self.created = utc2local(line[10:-1])
            elif line.startswith('modified'):
                self.modified = utc2local(line[11:-1])
            elif line.startswith('tags'):
                self.tags = re.search(r'\[(.*)\]', line).group(1).split(',')
                self.tags = [tag.replace('/', '-') for tag in self.tags]
            else:
                pass

    def get_start(self):
        self.divided_head()
        self.parse_head()
        return self.to_dict()


def utc2local(utcstr: str):
    utc_date = datetime.strptime(utcstr, "%Y-%m-%dT%H:%M:%S.%fZ")
    local_date = utc_date + timedelta(hours=8)
    return datetime.strftime(local_date, '%Y-%m-%d %H:%M:%S')


md_instance = """---
tags: [Linux/Develop, System, V2ray]
title: This is a title
created: '2019-10-11T08:28:52.029Z'
modified: '2020-02-15T14:37:12.812Z'
---

# This is a H1 title"""

if __name__ == '__main__':
    mdtest_file = "D:\\Test\\Git常用命令.md"
    md = MdFile(mdtest_file)
    print(md.get_start())
