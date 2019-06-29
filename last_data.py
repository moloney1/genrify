import argparse
import pprint

import requests

from creds.creds import apikey

BASE_URL = "http://ws.audioscrobbler.com/2.0/"

pp = pprint.PrettyPrinter(indent=4)

def base_request():
	payload =  {
		"method": "album.gettoptags",
		"api_key" : apikey,
		"format": "json",
		"autocorrect": 1
	}
	return payload


def get_top_tags(artist, album, limit=5):
	payload = base_request()
	payload.update({
	"artist": artist,
	"album": album
	})
	req = requests.get(BASE_URL, params=payload)
	data = req.json()
	toptags = data["toptags"]["tag"]
	limit = min(len(toptags), limit)
	tags = []
	for i in range(0, limit):
		tags.append(toptags[i]["name"].title())
	return tags

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Top tags")
	parser.add_argument("artist")
	parser.add_argument("album")
	args = parser.parse_args()

	tags = get_top_tags(args.artist, args.album)
	print(tags)

