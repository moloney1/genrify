import os
import argparse
import pprint

import requests

BASE_URL = "http://ws.audioscrobbler.com/2.0/"
APIKEY = os.environ.get('LASTFM_API_KEY')

pp = pprint.PrettyPrinter(indent=4)


def base_request():
    payload = {
        "method": "album.gettoptags",
        "api_key": APIKEY,
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
    res = _send_get_request(BASE_URL, params=payload)
    data = res.json()
    if "error" in data:
        print(f"Error finding tags for {artist}-{album}: {data['message']}")
        return None
    toptags = data["toptags"]["tag"]
    limit = min(len(toptags), limit)
    tags = []
    for i in range(0, limit):
        tags.append(toptags[i]["name"].title())  # return in Title Case
    return tags


def _send_get_request(*args, **kwargs):
    if not APIKEY:
        raise EnvironmentError(
                'last.fm api key required in '
                'LASTFM_API_KEY environment variable'
        )
    return requests.get(*args, **kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Top tags")
    parser.add_argument("artist")
    parser.add_argument("album")
    args = parser.parse_args()

    tags = get_top_tags(args.artist, args.album)
    print(tags)
