from bs4 import BeautifulSoup
import requests

urls = [
	'http://www.songlyrics.com/news/top-genres/country-music/',
	'http://www.songlyrics.com/news/top-genres/hip-hop-rap/',
	'http://www.songlyrics.com/news/top-genres/pop/'
]

for url in urls:
	soup = BeautifulSoup(requests.get(url).text)
	for a in soup.select('.tracklist a:not(.class)'):
		print a
		break


	break