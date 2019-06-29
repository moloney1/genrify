# Genrify

This is a CLI tool for editing genre tags in MP3 files (and eventually other music files).

## Problem

When you download an album it tends to have really vague genre tags. For example, some Post-punk album will be tagged as "Rock", while some other album is tagged as "Metal" when it's obviously Progressive tech-death :man_facepalming: :man_facepalming: :man_facepalming:

This renders queuing/playing songs by genre mostly useless.

## Solution
This tool uses the [mutagen](https://mutagen.readthedocs.io/en/latest/) library to find a track's metadata, and asks the [Last.fm API](https://www.last.fm/api/) what genres it's most commonly tagged at. It then sets the genre tag to the most common one (interactive choosing to be added).
