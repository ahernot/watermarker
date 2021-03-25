# Layer merging solution from https://stackoverflow.com/questions/40895785/using-opencv-to-overlay-transparent-image-onto-another-image
import cv2

import auxiliary_functions as AuxFunc



# TODO
# padding should also crop on sides when watermark too big for image
# allow negative watermark_position
# careful about rounding in set_size (): issues? no, there shouldn't be any
# allow crop to be percentages? use? IDTS…
def add_watermark(
        image_path: str,
        watermark_path: str,
        output_path: str,
        watermark_size: tuple or int or float = (None, None),  # can only be positive
        watermark_position: tuple = (1.0, 1.0),  # can be positive or negative
        image_size: tuple or int or float = (1.0, 1.0),  # can only be positive
        **kwargs) -> bool:
    """
    Add watermark to image. Remove EXIF tags (because only image is taken).

    watermark size is relative to cropped image
    resizing happens once watermark has been applied

    :param image_path:
    :param watermark_path:
    :param output_path: Output save path
    :param watermark_size: Tuple of percentages/pixels: (width-percentage, height-percentage), leave one as None for proportions // , or pixel value (for largest axis)
    :param watermark_position: Tuple of percentages/pixels: (width-percentage, height-percentage) from top left
    :param image_size: Tuple of percentages/pixels, or pixel value (for largest axis)
    :param kwargs: 'opacity': 0. < float < 1 | 'crop': image crop, in pixels (left, right-1, top, bottom-1) - Vector4(int), applied before any resizing // can be negative for ends of bounds
    :return:
    """

    # Read kwargs
    mask_opacity = 0.35
    if 'opacity' in kwargs:
        mask_opacity = kwargs['opacity']

    image_crop = (None, None, None, None)
    if 'crop' in kwargs:  # image crop in *kwargs is also either negative or positive
        image_crop = kwargs['crop']

    # Load image and watermark
    image, i_height, i_width, i_depth = AuxFunc.imread_rgba(image_path)
    watermark, w_height, w_width, w_depth = AuxFunc.imread_rgba(watermark_path)

    # Crop image on original size (change aspect ratio)
    image = image[image_crop[0]:image_crop[1], image_crop[2]:image_crop[3]]

    # Calculate & apply new sizes (keep aspect ratio)
    i_width, i_height = AuxFunc.set_size(i_width, i_height, image_size)
    w_width, w_height = AuxFunc.set_size(w_width, w_height, watermark_size, (i_width, i_height))
    image_resized = cv2.resize(image, (i_width, i_height), interpolation=cv2.INTER_AREA)
    watermark_resized = cv2.resize(watermark, (w_width, w_height), interpolation=cv2.INTER_AREA)

    # Calculate watermark position as (start:stop, start:stop) of resized image

    # cv2.imwrite(output_path+'overlay.png', image[:w_height, :w_width])
    # stick to leading edge

    # Pad watermark
    watermark_layer = AuxFunc.pad(watermark_resized, i_width, i_height, w_width, w_height, watermark_position)

    # Merge layers
    w_img = watermark_layer[:, :, :3]
    w_mask = watermark_layer[:, :, 3:] / 255.

    w_mask_mask = w_mask > 0.1  # threshold
    w_mask[w_mask_mask] = mask_opacity

    image_resized = ((1.0 - w_mask) * image_resized)[:, :, :3] + w_mask * w_img

    # Save image (RGB, no alpha channel)
    cv2.imwrite(output_path, image_resized)

    return True  # success

