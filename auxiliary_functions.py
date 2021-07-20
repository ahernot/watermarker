import os
import cv2
import numpy as np

# DO NOT IMPORT PREFERENCES


def generate_dirs(dirpath: str):
    try:
        os.makedirs(dirpath)
    except FileExistsError:
        pass

def clamp(val, min_val, max_val):
    if min_val > max_val: min_val, max_val = max_val, min_val
    return max(min_val, min(val, max_val))

def imread_rgba(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    height, width, depth = img.shape
    if depth == 3:
        img = np.concatenate((
            img,
            np.ones((height, width, 1), dtype=img.dtype) * 255),
            axis=2
        )
    return img

class FloorDict:
    """
    Propagates value until next keypoint
    included on left, excluded on right
    """

    def __init__(self, breaks: list):
        # breaks = [ (0,10) , (1,0) , (7, 15) , (12,70) , (14,-4) ]

        breaks.sort()
        self.__keypoints, self.__keyvals = zip(*breaks)
        self.__len = len( self.__keypoints )

    def __getitem__(self, key: int or float):

        for i in range(self.__len - 1):
            bound_left = self.__keypoints [i]
            bound_right = self.__keypoints [i + 1]

            if key >= bound_left and key < bound_right:
                return self.__keyvals[i]
        
        if key >= self.__keypoints [-1]:
            return self.__keyvals [-1]

        # Key on the left of first point
        return None

# f = FloorDict( [ (0,10) , (1,0) , (7, 15) , (12,70) , (14,-4) ] )
# print(f[0.2023])
