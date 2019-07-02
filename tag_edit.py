import sys
import warnings

import mutagen.mp3

# param mp3file - path of mp3file
# param genre - str containing genre to edit to 
def edit_genre(mp3file, genre):
	artist, title, _ = get_current_data(mp3file)
	md = mutagen.mp3.EasyMP3(mp3file)

	try:
		cur_gen = md.tags["genre"][0]
		if cur_gen == genre:
			print(f"{artist}-{title} already tagged {genre}. No action taken")
		else:
			md.tags["genre"] = genre
			print(f"{artist}-{title}: genre changed from {cur_gen} to {genre}")
	except:
		md.tags["genre"] = genre
		print("No genre found for {artist}-{title}. Added genre tag: {genre}")
	md.save()

# take file path as param instead of EasyMP3 object
# so that we can give appropriate warning on failure
def get_current_data(mp3file):
	md = mutagen.mp3.EasyMP3(mp3file)
	try:
		return (md.tags["artist"][0], 
				md.tags["title"][0],
				md.tags["album"][0])
	except:
		warnings.warn(f"File {mp3file} is missing tags.")
		return (None, None, None)
	
def dump_tags(mp3file):
	md = mutagen.mp3.EasyMP3(mp3file)
	print(md.tags)

if __name__ == "__main__":
	#edit_genre(sys.argv[1], "Classical")
	dump_tags(sys.argv[1])
	#md = mutagen.mp3.EasyMP3("TestAlbum/Gone.mp3")
	#print(get_current_data(md))
