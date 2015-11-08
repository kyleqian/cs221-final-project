from bs4 import BeautifulSoup
from bs4.element import NavigableString
import requests
import collections
import json

def get_lyrics_urls():
	urls = {
		'country': 'http://www.songlyrics.com/news/top-genres/country-music/',
		'hiphoprap': 'http://www.songlyrics.com/news/top-genres/hip-hop-rap/',
		'pop': 'http://www.songlyrics.com/news/top-genres/pop/'
	}

	lyrics_urls = collections.defaultdict(list)

	for genre in urls:
		soup = BeautifulSoup(requests.get(urls[genre]).text)

		if not soup.select('table.tracklist'):
			print 'BLOCKED'
			break

		for i,row in enumerate(soup.select('table.tracklist tr')):
			if i == 0: continue

			tds = row.select('td')
			lyrics_urls[genre].append(tds[2].a['href'])

	with open('lyrics_urls.json', 'w') as f:
		f.write(json.dumps(lyrics_urls))

def get_lyrics():
	lyrics = collections.defaultdict(list)

	lyrics_urls = json.loads(open('lyrics_urls.json', 'r').read())

	for genre in lyrics_urls:
		# song level
		for i,url in enumerate(lyrics_urls[genre]):
			if not url: continue

			lyrics_list = []

			soup = BeautifulSoup(requests.get(url).text)

			if not soup.select('#songLyricsDiv') and soup.select('.pagetitle'): continue

			c = False
			while not soup.select('#songLyricsDiv'):
				print 'BLOCKED'
				print 'Processing song', i, 'in genre', genre, "|", url
				ri = raw_input(">>")
				if ri == 'c':
					c = True
					break
				soup = BeautifulSoup(requests.get(url).text)

			if c: continue

			for a in soup.select('#songLyricsDiv')[0].contents:
				if isinstance(a, NavigableString) and not a.string.isspace():
					lyrics_list.append(a.string.strip())

			lyrics[genre].append(lyrics_list)

	with open('lyrics.json', 'w') as f:
		f.write(json.dumps(lyrics))

def check_lyrics():
	with open('lyrics.json', 'r') as f:
		lyrics = json.loads(f.read())
		print len(lyrics)
		for genre in lyrics:
			print len(lyrics[genre])

# get_lyrics_urls()
# get_lyrics()
check_lyrics()