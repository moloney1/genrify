import os
import argparse

import magic

import tag_edit
import last_data

def is_mp3_file(f):
	return magic.from_file(f, mime=True) == "audio/mpeg"

def get_genre_choice(genres):
	# start numbering at one for better friendliness
	for i, choice in enumerate(genres, 1):
		print(f"[{i}]: {choice}")
	print(f"[{len(genres) + 1}]: Tag manually")
	
	choice = int(input(" > "))
	if choice == len(genres) + 1:
		print("Tag this album manually:")
		return get_manual_genre_input()
	else:
		return genres[choice - 1] # account for indexing

def get_manual_genre_input():
	return str(input(" > "))

parser = argparse.ArgumentParser(description="Genre setter")
parser.add_argument("library")
parser.add_argument("--interactive", "-i", action="store_true")
parser.add_argument("--nolastfm", "-n", action="store_true")
parser.add_argument("--limit", "-l", type=int)
args = parser.parse_args()

print(args)

genre_lookup = {}
for root, dirs, files in os.walk(args.library, topdown=False):
	for name in files:
		path = os.path.join(root, name)
		# print(f"{path} - {is_mp3_file(path)}")
		if is_mp3_file(path):
			artist, _, album = tag_edit.get_current_data(path)

			# skip this file if it is missing necessary tags
			if artist == None or album == None:
				print("Skipping {name} due to missing essential information.")
				continue

			if not album in genre_lookup:
				if not args.nolastfm:
					# limit how many selections to display 
					# only relevant for interactive mode
					limit = 5 if not args.limit else args.limit
					# get top tags from last.fm
					genres = last_data.get_top_tags(artist, album, limit=limit)
					if args.interactive:
						print(f"Choose a genre for {artist} - {album}:")
						genre = get_genre_choice(genres)
					else:
						genre = genres[0] 
				else:
					# skip last.fm query and get manual input
					print(f"Choose a genre for {artist} - {album}:")
					genre = get_manual_genre_input()

				tag_edit.edit_genre(path, genre)
				genre_lookup[album] = genre
			else:
				tag_edit.edit_genre(path, genre_lookup[album])	
				print(album)


