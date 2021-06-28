#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cached_url
import threading
from bs4 import BeautifulSoup
import sys
import os
from telegram_util import parseUrl

channels = {'daily_read': 27, 'muddycat': 1}

def getPosts(name, start):
	content = cached_url.get('https://t.me/s/%s/%d' % (name, start))
	soup = BeautifulSoup(content, 'html.parser')
	for item in soup.find_all('div', class_='tgme_widget_message'):
		post_id = int(item['data-post'].split('/')[-1])
		post_content = item.find('div', class_='tgme_widget_message_text')
		post_content = BeautifulSoup(
			str(post_content).replace('<br/>', '\n'), features='lxml')
		content = parseUrl(post_content.text)
		for d in range(10):
			content = content.replace('\n%s.' % d, '\n%s. ' % d)
			content = content.replace('\n%s.  ' % d, '\n%s. ' % d)
		yield post_id, content

def run():
	for name, start in channels.items():
		os.system('mkdir %s > /dev/null 2>&1' % name)
		posts = {}
		while True:
			original_start = start
			for post_id, post_content in getPosts(name, start):
				start = max(start, post_id + 1)
				if post_id >= original_start:
					posts[post_id] = post_content
			if original_start == start:
				break
		posts = sorted([(x, y) for (x, y) in posts.items()])
		posts = [y for (x, y) in posts]
		with open('%s.md' % name, 'w') as f:
			f.write('\n\n=======\n\n'.join(posts))

if __name__ == '__main__':
    run()