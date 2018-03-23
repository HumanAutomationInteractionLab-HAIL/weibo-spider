from lxml import html
from time import time, sleep
import requests
import signal
import json
import re

request_interval = 60 / 240
# Apparently, something between 300 and 400 requests per minute is their limit.
# Header switching does not help, they block by ip.
# Proxies are needed in order to overcome the limit.

# platforms = ['dreamcast', 'ps', 'ps2', 'ps3', 'ps4', 'xbox', 'xbox360', 'xboxone', 'n64', 'gamecube', 'wii', 'wii-u', 'switch', 'gba', 'ds', '3ds', 'psp', 'vita', 'pc']
platforms = ['dreamcast', 'ps', 'n64'] # test set

site = 'http://www.metacritic.com'
urls = ['%s/browse/games/release-date/available/%s/date' %(site, platform) for platform in platforms]
game_links = []
games = []

def init(_last_request, _request_lock):
	global last_request
	global request_lock
	last_request = _last_request
	request_lock = _request_lock
	
def download(url, retries = 0):
	result = None
	with request_lock:
		while time() - last_request.value < request_interval:
			#CPU melting albeit much more granular solution
			pass
		else:
			last_request.value = time()
	print('downloading %s' %url)
	try:
		page = requests.get(url, headers = {'User-Agent': 'whatever'})
		if page.status_code == requests.codes.ok:
			result = html.fromstring(page.content)
		elif retries > 0:
			if page.status_code == 429:
				wait_for = float(page.headers['Retry-After'])
				print('429. waiting for %2.2f seconds' %wait_for)
				sleep(wait_for)
			result = download(url, retries - 1)
		else:
			print ('Warning: bad response code. Dropping the request')
	except requests.exceptions.RequestException as e:
		print('requests exception: %s' %e)
	return result

def extract(root, path, template = '%s', default = ''):
	result = default
	tmp = root.xpath(path)
	if len(tmp) > 0:
		result = template %(tmp[0].strip())
	return result

def extract_number(root, path, template = '%s', default = 0):
	result = extract(root, path, template, default = str(default))
	result = int(re.findall('\d+', result)[0])
	return result

def game_list_parse(url, retries = 0): # retries = 10 
	signal.signal(signal.SIGINT, signal.SIG_IGN)
	result = None
	main_page = download(url, retries) # Download game list
	if main_page is not None:
		result = {'links': [], 'next': None}
		links = main_page.xpath('//div[@class="product_wrap"]/div[@class="basic_stat product_title"]/a')
		result['links'] = [extract(link, '@href', site + '%s') for link in links]
		result['next'] = extract(main_page, '//span[@class="flipper next"]/a/@href', site + '%s', default = None)
	else:
		print('main page downloading failed')
	return result

def game_page_parse(url, retries = 0):
	signal.signal(signal.SIGINT, signal.SIG_IGN)
	main_page = download(url, retries)
	result = None
	if main_page is not None:
		content = main_page.xpath('body/div[1]/div[@class="site_gutters"]/div[@class="site_gutters"]/div[@class="site_gutters"]/div[@class="site_gutters"]/div[@class="site_gutters"]/div/div/div/div/div[1]/div')
		content = content[0] if len(content) == 1 else main_page
		game = {}
		game['title'] = extract(content, '//div[@class="product_title"]/a/span/h1/text()')
		game['platform'] = extract(content, '//div[@class="product_title"]/span/a/span/text()|//div[@class="product_title"]/span/span/text()')
		game['released'] = extract(content, '//li[contains(@class, "release_data")]/span[@class="data"]/text()')
		game['developer'] = extract(content, '//li[@class="summary_detail developer"]/span[@class="data"]/text()')
		game['rating'] = extract(content, '//li[@class="summary_detail product_rating"]/span[@class="data"]/text()')
		game['genres'] = content.xpath('//li[@class="summary_detail product_genre"]/span[@class="data"]/text()')
		game['metascore'] = extract(content, '//div[@class="section product_scores"]/div[@class="details main_details"]/div/div/a/div/span/text()', default = 'tbd')
		game['critic_review_count'] = extract_number(content, '//div[@class="section product_scores"]/div[@class="details main_details"]/div/div/div[@class="summary"]/p/span[@class="count"]/a/span/text()')
		game['userscore'] = extract(content, '//div[@class="section product_scores"]/div[@class="details side_details"]/div[@class="score_summary"]/div/a/div/text()', default = 'tbd')
		game['user_ratings_count'] = extract_number(content, '//div[@class="section product_scores"]/div[@class="details side_details"]/div[@class="score_summary"]/div/div[@class="summary"]/p/span[@class="count"]/a/text()')
		game['user_review_count'] = extract_number(content, 'div[@class="module critic_user_reviews"]/div/div[2]/div[@class="body"]/div/div/ol/li[1]/div/span[@class="data"]/a/span/span[2]/text()')
		game['reviews'] = {'critic': [], 'user': []}
		for key in game['reviews'].keys():
			if game['%s_review_count' %key] > 0:
				review_url = url + '/%s-reviews' %key
				while review_url != '':
					reviews_page = download(review_url, retries)
					review_url = ''
					if reviews_page is not None:
						review_url = extract(reviews_page, '//span[@class="flipper next"]/a/@href', template = site + '%s')
						reviews = reviews_page.xpath('//div[@class="module reviews_module %s_reviews_module"]/div[@class="body product_reviews"]/ol[@class="reviews %s_reviews"]/li[contains(@class, "review %s_review")]' %(key, key, key))
						for review in reviews:
							an_actual_review = review.xpath('div/div/div/div/div/div[1]/div[1]/div')
							if len(an_actual_review) == 2:
								source = extract(an_actual_review[0], 'div[1]/a/text()')
								if source == '':
									source = extract(an_actual_review[0], 'div[1]/%stext()' %('span/' if key == 'user' else ''))
								game['reviews'][key].append({
									'source' : source,
									'date' : extract(an_actual_review[0], 'div[2]/text()'),
									'score' : extract(an_actual_review[1], 'div/text()'),})
		result = game
	else:
		print('main page downloading failed')
	return result
