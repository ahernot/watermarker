import os

import auxiliary_functions as AuxFunc
import coordinator as Coordinator
import datetime as dt



IMAGE_DIRPATH = './resources/images/'
OUTPUT_DIRPATH = './output/'
IMAGE_EXTENSIONS = ['jpeg', 'jpg', 'png', 'tiff', 'heic']  # heic?



def add_watermark_batch(
        watermark_path: str,
        watermark_size: tuple or int or float = (None, None),
        watermark_position: tuple = (1.0, 1.0),
        image_size: tuple or int or float = (1.0, 1.0),
        **kwargs):

    # Get list of images
    file_list = AuxFunc.get_files(IMAGE_DIRPATH)

    # Generate output dir
    output_dir = OUTPUT_DIRPATH + dt.datetime.now().strftime('%Y%m%d-%H%M%S-batch/')
    os.makedirs(output_dir)

    # Run through files
    for filename in file_list:

        # Skip non-image files
        extension = filename.split('.')[-1]
        if extension.lower() not in IMAGE_EXTENSIONS: continue
        filename_name = '.'.join(filename.split('.')[:-1])

        # Generate image path
        image_path = IMAGE_DIRPATH + filename
        output_path = output_dir + filename_name + '-watermarked.' + extension

        # Process image
        Coordinator.add_watermark(
            image_path=image_path,
            watermark_path=watermark_path,
            output_path=output_path,
            watermark_size=watermark_size,
            watermark_position=watermark_position,
            image_size=image_size,
            **kwargs
        )
