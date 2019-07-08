import sys
import warnings

import mutagen.mp3
import mutagen.flac

# param mp3file - path of mp3file
# param genre - str containing genre to edit to 
def edit_genre_mp3(mp3file, genre):
	artist, title, _ = get_current_data_mp3(mp3file)
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
		print(f"No genre found for {artist}-{title}. Added genre tag: {genre}")
	md.save()

# tags are stored as list of tuples e.g. [("artist","whatever"),...]
# FLAC field names are case insensitive
# FLAC also allows for multiple genres but assume only one for now
def edit_genre_flac(flacfile, genre):
	artist, title, _ = get_current_data_flac(flacfile)
	md = mutagen.flac.FLAC(flacfile)

	cur_gen = ""
	# check the current genre
	for tag in md.tags:
		if tag[0].upper() == "GENRE":
			cur_gen = tag[1]
			md.tags.remove(tag)
	
	if cur_gen:
		if cur_gen == genre:
			print(f"{artist}-{title} already tagged {genre}. No action taken")
		else:
			print(f"{artist}-{title}: genre changed from {cur_gen} to {genre}")
	else:
		print(f"No genre found for {artist}-{title}. Added genre tag: {genre}")
	md.tags.append(("GENRE", genre))

	md.save()
	

# take file path as param instead of EasyMP3 object
# so that we can give appropriate warning on failure
def get_current_data_mp3(mp3file):
	md = mutagen.mp3.EasyMP3(mp3file)
	try:
		return (md.tags["artist"][0], 
				md.tags["title"][0],
				md.tags["album"][0])
	except:
		warnings.warn(f"File {mp3file} is missing tags.")
		return (None, None, None)
	

def get_current_data_flac(flacfile):
	md = mutagen.flac.FLAC(flacfile)
	# dict comp to convert all keys to uppercase
	tags_dict = {key.upper() : value for key, value in dict(md.tags).items()}
	try:
		return (tags_dict["ARTIST"][0],
				tags_dict["TITLE"][0],
				tags_dict["ALBUM"][0])
	except:				
		warnings.warn(f"File {flacfile} is missing tags.")
		return (None, None, None)


def dump_tags(mp3file):
	md = mutagen.mp3.EasyMP3(mp3file)
	print(md.tags)

if __name__ == "__main__":
	#edit_genre(sys.argv[1], "Classical")
	#dump_tags(sys.argv[1])
	#edit_genre_flac(sys.argv[1], "Roc")
	#md = mutagen.mp3.EasyMP3("TestAlbum/Gone.mp3")
	#print(get_current_data(md))
	print(get_current_data_flac(sys.argv[1]))
