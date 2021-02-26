# Layer merging solution from https://stackoverflow.com/questions/40895785/using-opencv-to-overlay-transparent-image-onto-another-image
import cv2

import auxiliary_functions as AuxFunc



# TODO
# check interpolation method for resizing
# add image_crop Vector4 (left right top bottom) in kwargs
# padding should also crop on sides when watermark too big for image
def add_watermark(
        image_path: str,
        watermark_path: str,
        output_path: str,
        watermark_size: tuple or int or float = (None, None),
        watermark_position: tuple = (1.0, 1.0),
        image_size: tuple or int or float = (1.0, 1.0),
        **kwargs):
    """
    Add watermark to image. Remove EXIF tags.
    :param image_path:
    :param watermark_path:
    :param output_path: Output save path
    :param watermark_size: Tuple of percentages/pixels: (width-percentage, height-percentage), leave one as None for proportions // , or pixel value (for largest axis)
    :param watermark_position: Tuple of percentages/pixels: (width-percentage, height-percentage) from top left
    :param image_size: Tuple of percentages/pixels, or pixel value (for largest axis)
    :param kwargs: 'opacity': 0. < float < 1.
    :return:
    """

    # Read kwargs
    mask_opacity = 0.35
    if 'opacity' in kwargs:
        mask_opacity = kwargs['opacity']

    # Load image and watermark
    image, i_height, i_width, i_depth = AuxFunc.imread_rgba(image_path)
    watermark, w_height, w_width, w_depth = AuxFunc.imread_rgba(watermark_path)

    # Calculate new sizes
    i_width, i_height = AuxFunc.set_image_size(i_width, i_height, image_size)
    w_width, w_height = AuxFunc.set_watermark_size(i_width, i_height, w_width, w_height, watermark_size)

    # Resize
    image_resized = cv2.resize(image, (i_width, i_height), interpolation=cv2.INTER_AREA)
    watermark_resized = cv2.resize(watermark, (w_width, w_height), interpolation=cv2.INTER_AREA)

    # Pad watermark
    watermark_layer = AuxFunc.pad(watermark_resized, i_width, i_height, w_width, w_height, watermark_position)

    # Merge layers
    w_img = watermark_layer[:, :, :3]
    w_mask = watermark_layer[:, :, 3:] / 255.

    w_mask_mask = w_mask > 0.1  # threshold
    w_mask[w_mask_mask] = mask_opacity

    image_resized = ((1.0 - w_mask) * image_resized)[:, :, :3] + w_mask * w_img

    # Save image
    cv2.imwrite(output_path, image_resized)
