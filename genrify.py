import sys

import mutagen.mp3

# param mp3file - path of mp3file
# param genre - str containing genre to edit to 
def edit_genre(mp3file, genre):
	md = mutagen.mp3.EasyMP3(mp3file)
	art, tit = get_current_data(md)

	try:
		cur_gen = md.tags["genre"][0]
		md.tags["genre"] = genre
		print(f"{art}-{tit}: genre changed from {cur_gen} to {genre}")
	except:
		md.tags["genre"] = genre
		print("No genre found for {art}-{tit}")
		print("Added genre tag: {genre}")
	md.save()

# param md - mutagen.mp3.EasyMP3 object 
def get_current_data(md):
	return (md.tags["artist"][0], 
			md.tags["title"][0])
	
def dump_tags(mp3file):
	md = mutagen.mp3.EasyMP3(mp3file)
	print(md.tags)

edit_genre(sys.argv[1], "Classical")
dump_tags(sys.argv[1])
