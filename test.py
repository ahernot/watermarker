# from PIL import Image # use opencv cv2 instead
import exiftool
import cv2
import sqlite3

MAIN_DIRECTORY = './'


def load_watermark(path):

    watermark = cv2.imread(path)
    print(watermark)
    pass


path = 
load_watermark(path=pat)
















"""
import subprocess
cmd = ['exiftool', '/Users/anatole/Documents/GitHub/ahernot.github.io/resources/images/sample/IMG_5617.JPG']
output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
print(output)
"""


"""files = [
    '/Users/anatole/Documents/GitHub/ahernot.github.io/resources/images/sample/IMG_5617.JPG'
]
with exiftool.ExifTool() as et:
    metadata = et.get_metadata_batch(files)

print(len(metadata))
print(metadata[0].keys())
for key in metadata[0].keys():
    print(key)
"""
# add to sql database
# and then do some clever processing

#for d in metadata:

    # print("{:20.20} {:20.20}".format(d["SourceFile"], d["EXIF:DateTimeOriginal"]))


# choose watermark placement and size as percentage (of AREA?)
# place watermark, choose transparency
# remove all EXIF information

