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

def check_lyrics(name):
	if name == 'stripped_taylor.json':
		with open(name, 'r') as f:
			lyrics = json.loads(f.read())
			print len(lyrics), 'songs'
			for song in lyrics:
				for line in lyrics[song]:
					print line
	else:
		with open(name, 'r') as f:
			lyrics = json.loads(f.read())
			print len(lyrics)
			for genre in lyrics:
				print len(lyrics[genre])

def taylor_clean():
	exclude = set(string.punctuation.replace('-', ''))
	curr_song = ''
	lyrics = defaultdict(list)
	for l in open('taylor-lyrics.txt', 'r'):
		line = l.strip().split()
		if len(line) > 0:
			if line[0] == '###':
				curr_song = ' '.join(line[1:])
			else:

				### CLEAN LINE
				new_line = ''.join([i if ord(i) < 128 else '' for i in l.strip()])
				try:
					new_line = new_line.lower()
				except Exception, e:
					print e
					# print l
				new_line = ''.join(ch for ch in new_line if ch not in exclude)

				lyrics[curr_song].append(new_line)

	with open('stripped_taylor.json', 'w') as f:
		f.write(json.dumps(lyrics))

if __name__ == '__main__':
	# main()
	# check_lyrics()
	# taylor_clean()
	check_lyrics('stripped_taylor.json')