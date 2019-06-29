import sys

import mutagen.mp3

# param mp3file - path of mp3file
# param genre - str containing genre to edit to 
def edit_genre(mp3file, genre):
	md = mutagen.mp3.EasyMP3(mp3file)
	artist, title, _ = get_current_data(md)

	try:
		cur_gen = md.tags["genre"][0]
		md.tags["genre"] = genre
		print(f"{artist}-{title}: genre changed from {cur_gen} to {genre}")
	except:
		md.tags["genre"] = genre
		print("No genre found for {artist}-{title}")
		print("Added genre tag: {genre}")
	md.save()

def get_current_data(md):
	if isinstance(md, str):
		md = mutagen.mp3.EasyMP3(md)
	try:
		return (md.tags["artist"][0], 
				md.tags["title"][0],
				md.tags["album"][0])
	except:
		raise Exception('File missing essential information.')
	
def dump_tags(mp3file):
	md = mutagen.mp3.EasyMP3(mp3file)
	print(md.tags)

if __name__ == "__main__":
	#edit_genre(sys.argv[1], "Classical")
	dump_tags(sys.argv[1])
	#md = mutagen.mp3.EasyMP3("TestAlbum/Gone.mp3")
	#print(get_current_data(md))
