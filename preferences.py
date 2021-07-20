SOURCE_PATH = '/Users/anatole/Desktop/website-resources/_sampleDir'  # '/Users/anatole/Desktop/website-resources/albums/'
EXTENSIONS = ['jpg', 'jpeg', 'tiff', 'png', 'heic', 'heif']
WATERMARK_PATH = '/Users/anatole/Downloads/watermarks/watermark-white.tiff'  # TO CHANGE

from auxiliary_functions import FloorDict
SIZES = [
    (0.0, 1200),  # aspect ratio ≥0.0  =>  size = 1200px
    (2.5, 2000)  # aspect ratio ≥2.5  =>  size = 2000px
]
SIZES_FD = FloorDict( SIZES )

SIZE_FACTOR_MED = 0.7
SIZE_FACTOR_LOW = 0.4

WATERMARKS = [
    (0.1, 0.0, 1.0, 0.3),  # bottom left
    (0.1, 0.5, 0.5, 0.3),  # middle
    (0.1, 1.0, 0.0, 0.3)  # top right
]
