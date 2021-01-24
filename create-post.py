#!/usr/bin/env python
# coding:utf-8

__author__ = 'toutf8'

import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

# replace to vim or others if your like
# EDITOR = ['MarkdownPad2.exe']
EDITOR = ['code']

if __name__ == '__main__':
    post_name = input("Post'title: ")
    

    post_path = 'post/{year}/{date_format}-{post_name}.md'.format(
        year=datetime.now().year,
        date_format=datetime.now().strftime('%Y-%m-%d'),
        post_name=post_name.replace(' ', '-')
    )

    subprocess.call(['hugo', 'new', post_path])

    # replace template value
    post_rel_path = os.path.join('content', post_path)
    post_rel_path = Path(post_rel_path).as_posix()
    with open(post_rel_path, 'r') as f:
        content = f.read()

    url = '/{date_format}/{post_name}'.format(
        date_format=datetime.now().strftime('%Y/%m/%d'),
        post_name=post_name.replace(' ', '-')
    )

    article_url = 'url: "%s/"' % url

    replace_patterns =[
        (re.compile(r'title:(.*)'), 'title: "%s"' % post_name),
        # (re.compile(r'url:(.*)'), 'url: "%s/"' % url),
        (re.compile(r'\n---'), r'\n%s\n---' % article_url),
    ]

    for regex, replace_with in replace_patterns:
        content = regex.sub(replace_with, content)

    with open(post_rel_path, 'w') as f:
        f.write(content)

    subprocess.Popen(EDITOR + [post_rel_path])

