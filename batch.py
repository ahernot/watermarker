#!/usr/bin/env python

import os
import posix
import json #TEMP

import preferences
from process_logger import Logger
from file import MediaFile
from image import WebsiteImage, ImageLayered
from exif_formatter import ExifDict
from auxiliary_functions import generate_dirs, imread_rgba



def run(path: str):

    # Initialise logger
    logger = Logger(path)

    with os.scandir(path) as albums:
        for album in albums:

            # Check if album is directory
            if not album.is_dir():
                continue

            with os.scandir(album.path) as files:
                for file in files:

                    # Check path type
                    if not file.is_file():
                        continue

                    # Create MediaFile object
                    media_file = MediaFile(file)

                    # Check image file type
                    if (media_file.extension).lower() not in preferences.EXTENSIONS:
                        continue

                    # Check if already processed
                    if logger.is_processed(album.name, media_file.name_full):
                        continue

                    # Generate destination path
                    dest_path = f'../../resources/albums/_tests/{album.name}/{media_file.name}/'
                    generate_dirs( dest_path )

                    # Resize image
                    img_r = WebsiteImage( media_file.path )

                    # Watermark image
                    img_w = ImageLayered( img_r.image )
                    watermark = imread_rgba( preferences.WATERMARK_PATH )
                    for watermark_info in preferences.WATERMARKS:
                        img_w.add_watermark(watermark, *watermark_info)
                    
                    # Export image and masks (in all sizes)
                    img_w.export(dirpath=dest_path)

                    # Read exif data and save json in destination path
                    exif = ExifDict( media_file.exif )
                    exif.save(dirpath=dest_path)

                    # Log file as processed
                    logger.log_processed(album.name, media_file.name_full)

    # Write log
    logger.save()
    del logger

# watermarking program will be copied over from my watermarking utility
# random opacity in range (0.3-0.8) for watermark?
# random opacity for mask?
