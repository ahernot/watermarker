import os
import json
from fractions import Fraction


# dictionary with """ newKey: [oldKey1, oldKey2, …] """
EXIF_TAGS = {
    'fileSizeOriginal': ['File:FileSize'],

    #'autor': 'Anatole Hernot',
    'dateTimeOriginal': ['EXIF:DateTimeOriginal'],
    'offsetTimeOriginal': ['EXIF:OffsetTimeOriginal'],
    #'dateFormatted': '2021.01.01',
    #'location': 'Unnamed Location',
    'camera': ['EXIF:Model'],
    #'tags': ['tag'],

    'settingISO': ['EXIF:ISO'],
    #'settingShutterSpeedSeconds': '1/60',  # to convert back to a fraction
    'settingFNumber': ['EXIF:FNumber'],
    'settingFocalLength': ['EXIF:FocalLength'],

    #'aspectRatio': '3:2',  # tuple now
    #'imageWidth': 600,
    #'imageHeight': 400,
    #'megapixels': 600 * 400,
    'imageWidthOriginal': ['EXIF:ExifImageWidth'],
    'imageHeightOriginal': ['EXIF:ExifImageHeight'],
    #'megapixelsOriginal': 4000 * 6000
}


def generate_image_dictionary(metadata: dict):

    exif_dict = dict()

    exif_dict['fileNameOriginal'] = 'myFile'
    exif_dict['fileSize'] = ''  # after postprocessing
    exif_dict['filePathOriginal'] = ''

    exif_dict['author'] = 'Anatole Hernot'
    exif_dict['location'] = 'Unknown Location'
    #exif_dict['tags'] = ['tag']

    # Fill simple tags
    for tag in EXIF_TAGS:

        exif_tags = EXIF_TAGS[tag]
        val = None  # default value

        # Try getting value, in order of priority
        for exif_tag in exif_tags:
            try: val = metadata[exif_tag]
            except: pass
        
        exif_dict[tag] = val

    # dateFormatted
    exif_dict['dateFormatted'] = ''


    # settingShutterSpeed
    try:
        shutter_speed_float = metadata['EXIF:ExposureTime']
        shutter_speed_frac = Fraction(shutter_speed_float) .limit_denominator(10**5)
        exif_dict['settingShutterSpeedSeconds'] = str(shutter_speed_frac)
    except:
        exif_dict['settingShutterSpeedSeconds'] = None

    # aspectRatio
    try:
        ar_frac = Fraction(exif_dict['imageWidthOriginal'], exif_dict['imageHeightOriginal']) .limit_denominator(10**5)
        exif_dict['aspectRatio'] = (ar_frac.numerator, ar_frac.denominator)
    except:
        exif_dict['aspectRatio'] = None
    
    #'imageHeight': 400,
    #'megapixels': 600 * 400,

    # megapixelsOriginal
    try:
        exif_dict['megapixelsOriginal'] = round(exif_dict['imageWidthOriginal'] * exif_dict['imageHeightOriginal'] / 1e6, 1)
    except:
        exif_dict['megapixelsOriginal'] = None

    return exif_dict



class ExifDict:

    def __init__(self, metadata: dict):
        self.data = generate_image_dictionary(metadata)

    def save(self, dirpath: str):
        json_path = dirpath + 'image.json'
        with open(json_path, 'w', encoding='utf-8') as dump:
            json.dump(self.data, dump, indent=4)
