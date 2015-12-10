import json
from collections import defaultdict
import string

def main():
	exclude = set(string.punctuation.replace('-', ''))

	lyrics = json.loads(open('lyrics.json', 'r').read())
	new_lyrics = defaultdict(list)

	for genre in lyrics:
		genre_songs = []
		for s in lyrics[genre]:
			new_song = []
			for l in s:
				# new_line = str(l)
				new_line = ''.join([i if ord(i) < 128 else '' for i in l.strip()])
				try:
					new_line = new_line.lower()
				except Exception, e:
					print e
					# print l
				new_line = ''.join(ch for ch in new_line if ch not in exclude)
				new_song.append(new_line)
			genre_songs.append(new_song)
		new_lyrics[genre] = genre_songs

	with open('stripped_lyrics.json', 'w') as f:
		f.write(json.dumps(new_lyrics))

def check_lyrics():
	with open('stripped_lyrics.json', 'r') as f:
		lyrics = json.loads(f.read())
		print len(lyrics)
		for genre in lyrics:
			print len(lyrics[genre])

if __name__ == '__main__':
	# main()
	check_lyrics()