#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cached_url
import threading
from bs4 import BeautifulSoup
import sys
import os

channels = {'daily_read': 27}

def getPosts(name, start):
	content = cached_url.get('https://t.me/s/%s/%d' % (name, start))
	soup = BeautifulSoup(content, 'html.parser')
	for item in soup.find_all('div', class_='tgme_widget_message'):
		post_id = int(item['data-post'].split('/')[-1])
		post_content = item.find('div', class_='tgme_widget_message_text')
		yield post_id, post_content.text

def loopImp():
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
		# Room of improvement: we can cache the old posts
		# as posts more than 1 day old are not editable
		posts = [y for (x, y) in posts]
		with open('%s.txt', 'w') as f:
			f.write('\n\n\n'.join(posts))
	os.system('git add . > /dev/null 2>&1 && git commit -m commit > /dev/null 2>&1 && git push -u -f > /dev/null 2>&1')

def loop():
	loopImp()
	threading.Timer(60 * 60 * 2, loop).start() 

if not 'once' in sys.argv:
	threading.Timer(1, loop).start()
else:
	loopImp()