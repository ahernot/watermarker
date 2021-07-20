import posix
import os

from exiftool import ExifTool

class MediaFile:

    def __init__(self, dirEntry: posix.DirEntry):

        self.path = dirEntry.path
        self.name_full = dirEntry.name
        self.name = os.path.splitext(self.name_full) [0]
        self.extension = os.path.splitext(self.name_full) [1] [1:]
        self.exif = self.__get_exif()

    def __get_exif(self):
        with ExifTool() as e:
            metadata = e.get_metadata(self.path)
        return metadata[0]
        