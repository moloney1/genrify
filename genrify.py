import os
import argparse

import magic

import tag_edit
import last_data

def is_mp3_file(f):
	return magic.from_file(f, mime=True) == "audio/mpeg"

def get_genre_choice(genres, prompt=""):
	if prompt: print(prompt)
	# start numbering at one for better friendliness
	for i, choice in enumerate(genres, 1):
		print(f"[{i}]: {choice}")
	print(f"[{len(genres) + 1}]: Tag manually")
	
	choice = input(" > ")
	if choice:
		try:
			choice = int(choice)
		except:
			return get_genre_choice(genres, prompt="Invalid input!")
	else:
		choice = 1

	if choice == len(genres) + 1:
		return get_manual_genre_input("Tag this album manually:")
	else:
		return genres[choice - 1] # account for indexing

def get_manual_genre_input(prompt):
	print(prompt)
	choice = input(" > ")
	if choice:
		return str(choice)
	else:
		return get_manual_genre_input("Genre can't be empty.")

def genrify(path):
	artist, _, album = tag_edit.get_current_data(path)
	name = os.path.basename(path)
	# skip this file if it is missing necessary tags
	if artist == None or album == None:
		print(f"Skipping {name} due to missing essential information.")
		return

	if not album in genre_lookup:
		if not args.nolastfm:
			# limit how many selections to display 
			# only relevant for interactive mode
			limit = 5 if not args.limit else args.limit
			# get top tags from last.fm
			genres = last_data.get_top_tags(artist, album, limit=limit)

			if genres == None or not genres:
				print(f"Skipping {name}: no tags available")
				return

			if args.interactive:
				print()
				prompt = f"Choose a genre for {artist} - {album}:"
				genre = get_genre_choice(genres, prompt=prompt)
			else:
				genre = genres[0] 

		else:
			# skip last.fm query and get manual input
			genre = get_manual_genre_input(f"Choose a genre for {artist} - {album}:")

		tag_edit.edit_genre(path, genre)
		genre_lookup[album] = genre
	else:
		tag_edit.edit_genre(path, genre_lookup[album])	

genre_lookup = {}

parser = argparse.ArgumentParser(description="Genre setter")
parser.add_argument("library")
parser.add_argument("--interactive", "-i", action="store_true")
parser.add_argument("--nolastfm", "-n", action="store_true")
parser.add_argument("--limit", "-l", type=int)
args = parser.parse_args()

print(args)

def main():
	if os.path.isdir(args.library):
		for root, _, files in os.walk(args.library, topdown=False):
			for name in files:
				path = os.path.join(root, name)
				if is_mp3_file(path):
					genrify(path)
	else:
		if is_mp3_file(args.library):
			genrify(args.library)

main()
