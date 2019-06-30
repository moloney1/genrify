import os
import argparse

import magic

import genrify
import last_data

def is_mp3_file(f):
	return magic.from_file(f, mime=True) == "audio/mpeg"

parser = argparse.ArgumentParser(description="Genre setter")
parser.add_argument("library")
parser.add_argument("--last-fm", action="store_true")
parser.add_argument("--interactive", "-i", action="store_true")
args = parser.parse_args()
print(args)

genre_lookup = {}
for root, dirs, files in os.walk(args.library, topdown=False):
	for name in files:
		path = os.path.join(root, name)
		# print(f"{path} - {is_mp3_file(path)}")
		if is_mp3_file(path):
			artist, _, album = genrify.get_current_data(path)
			if not album in genre_lookup:
				genres = last_data.get_top_tags(artist, album)
				if args.interactive:
					print(f"Choose a genre for {artist} - {album}:")
					for i, choice in enumerate(genres, 1):
						print(f"[{i}: {choice}]")
					genre = genres[int(input(" > ")) - 1]

					pass
				else:
					genre = genres[0] # TODO allow interactive choosing || manual override etc

				genrify.edit_genre(path, genre)
				genre_lookup[album] = genre
			else:
				genrify.edit_genre(path, genre_lookup[album])	
				print(album)

