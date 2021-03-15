import os
import cv2
import numpy as np


def get_files(directory_path):
    file_list = []
    for (dirpath, dirnames, filenames) in os.walk(directory_path):
        file_list.extend(filenames)
        break
    return file_list


def imread_rgba(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    height, width, depth = img.shape
    if depth == 3:
        img = np.concatenate((
            img,
            np.ones((height, width, 1), dtype=img.dtype) * 255),
            axis=2
        )
    return img, height, width, depth


def calc_max_size(i1_width, i1_height, i2_width, i2_height):
    """
    Calculate maximum size for image 2 inside of image 1 with no overflow and no stretching.
    :param i1_width: bounding image width
    :param i1_height: bounding image height
    :param i2_width: image width
    :param i2_height: image height
    :return: maximum i2 dimensions
    """

    # Calculate ratios
    i1_ratio = i1_width / i1_height
    i2_ratio = i2_width / i2_height

    # Calculate maximum watermark size
    if i2_ratio >= i1_ratio:
        max_width = i1_width
        max_height = i2_width / i2_ratio
    else:
        max_height = i1_height
        max_width = i2_height * i2_ratio

    return i2_width, i2_height




# TODO
# abs(width) for percentage checks
# and width-val for negative values; -1 should remove 1 pixel only
"""def set_watermark_size(i_shape, w_shape, w_resize):

    # Unpack shapes
    i_width, i_height = i_shape
    w_width, w_height = w_shape

    # Set the largest dimension
    if type(w_resize) in (int, float):
        if w_width >= w_height:
            watermark_size = (w_resize, None)
        else:
            watermark_size = (None, w_resize)

    # Preserve dimensions
    if w_resize in (None, (None, None)):
        watermark_size = (1.0, 1.0)

    # Calculate aspect ratios
    i_ratio = i_width / i_height
    w_ratio = w_width / w_height

    # Unpack size tuple
    width, height = w_resize

    # Convert all percentages to pixel counts (if percentages given), using reference_size
    if (width is not None) and (width <= 1):
        width = width * i_width  # read as percentage of image width
    if (height is not None) and (height <= 1):
        height = height * i_height  # read as percentage of image height

    # Calculate maximum watermark size, using reference_size
    if w_ratio >= i_ratio:
        max_width = i_width
        max_height = w_width / w_ratio
    else:
        max_height = i_height
        max_width = w_height * w_ratio

    # Apply max dimensions
    if width is not None:
        width = min(width, max_width)
    if height is not None:
        height = min(height, max_height)

    # Remove None to preserve aspect ratio
    if width is None:
        width = w_ratio * height
    elif height is None:
        height = width / w_ratio

    return int(width), int(height)
"""

"""def set_image_size(i_width, i_height, image_size):

    # Set the largest dimension
    if type(image_size) in (int, float):
        if i_width >= i_height:
            image_size = (image_size, None)
        else:
            image_size = (None, image_size)

    # Preserve dimensions
    if image_size in (None, (None, None)):
        image_size = (1.0, 1.0)

    # Calculate aspect ratio
    i_ratio = i_width / i_height

    # Unpack size tuple
    width, height = image_size

    # Convert all percentages to pixel counts
    if (width is not None) and (width <= 1):
            width = width * i_width  # read as percentage
    if (height is not None) and (height <= 1):
        height = height * i_height  # read as percentage

    # Remove None to preserve aspect ratio
    if width is None:
        width = i_ratio * height
    elif height is None:
        height = width / i_ratio

    return int(width), int(height)"""




def set_size(width, height, target_size, reference_size):
    """
    Set image/watermark size based on bounding container and resizing requirement.
    :param width: Original width
    :param height: Original height
    :param target_size: Target size
    :param reference_size: Size of the bounding box container (affects percentage sizes and max size)
    :return: New size
    """

    # Calculate aspect ratio
    aspect_ratio = width / height

    # Unpack reference size
    r_width, r_height = reference_size

    # Unpack target_size
    if target_size in (None, (None, None)):  # preserve dimensions
        t_width, t_height = 1.0, 1.0

    elif type(target_size) in (int, float):  # set the largest dimension (if only one size value given)
        if aspect_ratio >= 1:
            t_width, t_height = target_size, None
        else:
            t_width, t_height = None, target_size
    else:  # regular unpacking
        t_width, t_height = target_size

    # Read target_size as percentages (if values <= 1)
    if (t_width is not None) and (t_width <= 1):
        width *= r_width
    if (t_height is not None) and (t_height <= 1):
        height *= r_height

    # Calculate max dimensions
    max_width, max_height = calc_max_size(r_width, r_height, width, height)

    # Apply max dimensions
    if width is not None:
        width = min(width, max_width)
    if height is not None:
        height = min(height, max_height)

    # Fill None with aspect ration constraint
    if width is None:
        width = aspect_ratio * height
    elif height is None:
        height = width / aspect_ratio

    return int(width), int(height)




def pad(watermark_resized, i_width, i_height, w_width, w_height, watermark_position):

    # Read position as axis percentage or pixels
    pos_x_percent = watermark_position[0]
    pos_y_percent = watermark_position[1]
    if pos_x_percent > 1:
        pos_x_percent = pos_x_percent / i_width
    if pos_y_percent > 1:
        pos_y_percent = pos_y_percent / i_height

    # Calculate padding dimensions
    width_r = i_width - w_width
    height_r = i_height - w_height
    padding = [0] * 4  # left right up down

    padding[0] = int(width_r * pos_x_percent)  # left
    padding[1] = width_r - padding[0]  # right
    padding[2] = int(height_r * pos_y_percent)  # top
    padding[3] = height_r - padding[2]  # bottom

    watermark_layer = watermark_resized.copy()

    # Pad width
    margin_left = np.zeros((w_height, padding[0], 4), dtype=float)  # height width depth
    margin_right = np.zeros((w_height, padding[1], 4), dtype=float)
    # Concatenate (bring width to i_width)
    watermark_layer = np.concatenate((margin_left, watermark_layer, margin_right), axis=1)

    # Pad height
    margin_top = np.zeros((padding[2], i_width, 4), dtype=float)
    margin_bottom = np.zeros((padding[3], i_width, 4), dtype=float)
    # Concatenate (bring height to i_height)
    watermark_layer = np.concatenate((margin_top, watermark_layer, margin_bottom), axis=0)

    return watermark_layer
