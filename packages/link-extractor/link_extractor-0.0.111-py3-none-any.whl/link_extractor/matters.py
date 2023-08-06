from telegram_util import matchKey
from bs4 import BeautifulSoup
import cached_url

def match(sub_link, links):
	if len(sub_link) < 5:
		return
	if sub_link.count('/') != 2:
		return
	for link in links:
		if sub_link in link:
			return link

def getLikes(item):
	while True:
		item = item.parent
		if not item:
			return 0
		for subitem in item.find_all('footer'):
			label = subitem.get('aria-label', '')
			if label.startswith('讚賞 '):
				return int(label.split('讚賞 ')[1].split('、')[0])
	return 0

def filterMatters(links, config, site):
	soup = BeautifulSoup(cached_url.get(site), 'html.parser')
	result = set()
	for item in soup.find_all('a'):
		link = match(item.get('href'), links)
		if not link:
			continue
		if getLikes(item) > 300:
			result.add(link)
	return list(result)
