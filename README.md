# Genrify

This is a CLI tool for editing genre tags in music files.

## Motivation

### Problem
When you download an album it tends to have really vague genre tags. For example, some Post-punk album will be tagged as "Rock", while some other album is tagged as "Metal" when it's obviously Progressive tech-death :man_facepalming: :man_facepalming: :man_facepalming:

This renders queuing/playing songs by genre mostly useless.

### Solution
This tool uses the [mutagen](https://mutagen.readthedocs.io/en/latest/) library to find a track's metadata, and asks the [Last.fm API](https://www.last.fm/api/) what genres it's most commonly tagged as. It then sets the genre tag to the most common one by default, but has the option to choose a genre from the list interactively or override it completely. The Last.fm query can also be skipped in favour of tagging albums manually.

## Usage

For now get a last.fm API key and put it into a creds/creds.py file.

```
python genrify.py [-h] [--interactive] [--nolastfm] [--limit LIMIT] library
```

* -h shows help
* --interactive | -i allows choosing from <LIMIT> genres
* --limit | -l <LIMIT> sets the limit to use in interactive mode, default is 5.
* --nolastfm skips the last.fm query and allows users to tag manually.
* library is either a music library (directory) or a single music file.

## Features

- [x] Finding top tags by artist - album
- [x] Interactive genre choosing per album
- [x] manual input option
- [x] API error/bad input handling
- [x] FLAC support
- [ ] wav support (+other formats?)
- [ ] quiet/verbose output option

