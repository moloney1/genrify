import warnings
from abc import ABC, abstractmethod

from magic import from_file

import mutagen.mp3
import mutagen.flac


class MusicFile(ABC):
    @staticmethod
    def factory(filepath):
        """
        Return an instance of the appropriate subclass
        based on filetype, or None if the file is not
        a music file or is an unsupported music file
        """
        mime = from_file(filepath, mime=True)
        if "audio" not in mime:
            return None
        if mime == "audio/mpeg":
            return MP3File(filepath)
        elif "flac" in mime:
            return FLACFile(filepath)
        else:
            print(f"{filepath} unsupported filetype {mime}")
            return None

    @abstractmethod
    def get_current_data(self):
        """
        Get current artist, title and album tags as a tuple
        :return: (artist, title, album)
        :rtype: tuple
        """
        pass

    @abstractmethod
    def edit_genre(self, genre):
        """
        Edit the music file's genre tag to 'genre'

        :param genre: desired genre
        :type genre: str
        """
        pass


class MP3File(MusicFile):
    def __init__(self, filepath):
        self.filepath = filepath
        self.md = mutagen.mp3.EasyMP3(self.filepath)

    def get_current_data(self):
        try:
            return (
                self.md.tags["artist"][0],
                self.md.tags["title"][0],
                self.md.tags["album"][0]
            )
        except Exception:
            warnings.warn(f"File {self.filepath} is missing tags.")
            return (None, None, None)

    def edit_genre(self, genre):
        artist, title, _ = self.get_current_data()
        try:
            current_genre = self.md.tags["genre"][0]
            if genre == current_genre:
                print(
                    f"{artist}-{title} already tagged {genre}. "
                    "No action taken"
                )
            else:
                self.md.tags["genre"] = genre
                print(
                    f"{artist}-{title}: genre changed from "
                    f"{current_genre} to {genre}"
                )
        except Exception:
            self.md.tags["genre"] = genre
            print(
                f"No genre found for {artist}-{title}. "
                f"Added genre tag: {genre}"
            )
        self.md.save()


class FLACFile(MusicFile):
    def __init__(self, filepath):
        self.filepath = filepath
        self.md = mutagen.flac.FLAC(filepath)

    def get_current_data(self):
        tags_dict = {
            key.upper(): value
            for key, value
            in dict(self.md.tags).items()
        }
        try:
            return (
                tags_dict["ARTIST"][0],
                tags_dict["TITLE"][0],
                tags_dict["ALBUM"][0]
            )
        except Exception:
            warnings.warn(f"File {self.filepath} is missing tags.")
            return (None, None, None)

    def edit_genre(self, genre):
        artist, title, _ = self.get_current_data()
        current_genre = ""
        # check the current genre
        for tag in self.md.tags:
            if tag[0].upper() == "GENRE":
                current_genre = tag[1]
                self.md.tags.remove(tag)

        if current_genre:
            if current_genre == genre:
                print(
                    f"{artist}-{title} already tagged {genre}. "
                    "No action taken"
                )
            else:
                print(
                    f"{artist}-{title}: genre changed from "
                    f"{current_genre} to {genre}"
                )
        else:
            print(
                f"No genre found for {artist}-{title}. "
                f"Added genre tag: {genre}"
            )

        self.md.tags.append(("GENRE", genre))
        self.md.save()


if __name__ == "__main__":
    # edit_genre(sys.argv[1], "Classical")
    # dump_tags(sys.argv[1])
    # edit_genre_flac(sys.argv[1], "Roc")
    # md = mutagen.mp3.EasyMP3("TestAlbum/Gone.mp3")
    # print(get_current_data(md))
    # print(get_current_data_flac(sys.argv[1]))
    mp3 = MP3File("../tests/test_data/music/animals.mp3")
    print(mp3)
