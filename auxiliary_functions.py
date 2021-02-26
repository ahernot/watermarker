import cv2
import numpy as np


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


def set_watermark_size(i_width, i_height, w_width, w_height, watermark_size):

    # Set the largest dimension
    if type(watermark_size) in (int, float):
        if w_width >= w_height:
            watermark_size = (watermark_size, None)
        else:
            watermark_size = (None, watermark_size)

    # Preserve dimensions
    if watermark_size in (None, (None, None)):
        watermark_size = (1.0, 1.0)

    # Calculate aspect ratios
    i_ratio = i_width / i_height
    w_ratio = w_width / w_height

    # Unpack size tuple
    width, height = watermark_size

    # Convert all percentages to pixel counts
    if (width is not None) and (width <= 1):
        width = width * i_width  # read as percentage of image width
    if (height is not None) and (height <= 1):
        height = height * i_height  # read as percentage of image height

    # Calculate maximum watermark size
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


def set_image_size(i_width, i_height, image_size):

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
