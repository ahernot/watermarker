import os
import cv2
import numpy as np


def clamp(val, bound_lower = None, bound_upper = None):
    """
    Clamp value between lower and upper bounds. Can also be programmed using min/max.
    :param val:
    :param bound_lower:
    :param bound_upper:
    :return:
    """
    if bound_lower and val < bound_lower:
        return bound_lower
    elif bound_upper and val >= bound_upper:
        return bound_upper


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
def set_size(width: int, height: int, target_size: tuple or int or None, reference_size: tuple or None = None) -> (int, int):
    """
    Set image/watermark size based on bounding container and resizing requirement.
    :param width: Original width
    :param height: Original height
    :param target_size: Target size
    :param reference_size: Size of the bounding box container (affects percentage sizes and max size)
    :return: New size
    """

    # Calculate aspect ratio
    current_ratio = width / height

    # Unpack reference size
    if reference_size in (None, (None, None)):  # set to current size
        r_width, r_height = width, height
    else:
        r_width, r_height = reference_size

    # Unpack target_size (resize instructions)
    if target_size in (None, (None, None)):  # preserve dimensions
        t_width, t_height = 1.0, 1.0
    elif type(target_size) in (int, float):  # set the largest dimension (if only one size value given)
        if current_ratio >= 1:
            t_width, t_height = target_size, None
        else:
            t_width, t_height = None, target_size
    else:  # regular unpack
        t_width, t_height = target_size

    # Read target_size as percentages (if values <= 1)
    if (t_width is not None) and (t_width <= 1):
        t_width *= r_width
    if (t_height is not None) and (t_height <= 1):
        t_height *= r_height

    # Calculate max dimensions
    max_width, max_height = calc_max_size(r_width, r_height, width, height)

    # Apply max dimensions
    if t_width is not None:
        t_width = min(t_width, max_width)
    elif t_height is not None:
        t_height = min(t_height, max_height)

    # Fill None with aspect ration constraint
    if t_width is None:
        t_width = current_ratio * t_height
    elif t_height is None:
        t_height = t_width / current_ratio

    return round(t_width), round(t_height)



def calc_position(i1_width, i1_height, i2_width, i2_height, i2_position):
    # image 2 inside of image 1
    # i2 = watermark

    # Read position as axis percentage or pixels
    pos_x_percent = i2_position[0]
    pos_y_percent = i2_position[1]
    if pos_x_percent > 1:
        pos_x_percent = pos_x_percent / i1_width
        pos_x_percent = clamp(pos_x_percent, 0., 1.)  # percentage from center of container, going to limits within image_1
    if pos_y_percent > 1:
        pos_y_percent = pos_y_percent / i1_height
        pos_y_percent = clamp(pos_y_percent, 0., 1.)

    # Calculate i1_bounding_box dimensions
    width_r = i1_width - i2_width
    height_r = i1_height - i2_height

    # Compute image 2 bounding box
    i2_width_half = i2_width / 2
    i2_height_half = i2_height / 2

    i2_bounding_box = [0] * 4  # left right up down
    i2_bounding_box[0] = round(width_r * pos_x_percent - i2_width_half)
    i2_bounding_box[1] = i2_bounding_box[0] + i2_width
    i2_bounding_box[2] = round(height_r * pos_y_percent - i2_height_half)
    i2_bounding_box[3] = i2_bounding_box[2] + i2_height

    #padding[0] = int(width_r * pos_x_percent)  # left
    #padding[1] = width_r - padding[0]  # right
    #padding[2] = int(height_r * pos_y_percent)  # top
    #padding[3] = height_r - padding[2]  # bottom

    """watermark_layer = watermark_resized.copy()

    # Pad width
    margin_left = np.zeros((w_height, padding[0], 4), dtype=float)  # height width depth
    margin_right = np.zeros((w_height, padding[1], 4), dtype=float)
    # Concatenate (bring width to i_width)
    watermark_layer = np.concatenate((margin_left, watermark_layer, margin_right), axis=1)

    # Pad height
    margin_top = np.zeros((padding[2], i_width, 4), dtype=float)
    margin_bottom = np.zeros((padding[3], i_width, 4), dtype=float)
    # Concatenate (bring height to i_height)
    watermark_layer = np.concatenate((margin_top, watermark_layer, margin_bottom), axis=0)"""

    return i2_bounding_box




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
