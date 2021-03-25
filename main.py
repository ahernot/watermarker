import coordinator_wrapper as CoordinatorW


# Add batch processing

if __name__ == '__main__':

    """
    CoordinatorW.add_watermark_batch(
        watermark_path='./resources/watermarks/copyright-whitetransp.tiff',
        watermark_size=(None, 0.1),
        watermark_position=(50, 1.0),
        image_size=1500,
        opacity=0.35
    )
    """

    """CoordinatorW.add_watermark_batch(
        watermark_path='./resources/watermarks/copyright-whitetransp.tiff',
        watermark_size=(None, 0.13),
        watermark_position=(50, 1.0),
        image_size=1000,
        opacity=0.35  # 0.6
    )"""

    # Panoramas - 2.5 : 1
    """
    CoordinatorW.add_watermark_batch(
        watermark_path='./resources/watermarks/copyright-whitetransp.tiff',
        watermark_size=(0.15, None),
        watermark_position=(50, 1.0),
        image_size=2000,
        opacity=0.35  # 0.6
    )"""

    # Photos horizontal
    CoordinatorW.add_watermark_batch(
        watermark_path='./resources/watermarks/copyright-whitetransp.tiff',
        watermark_size=(0.25, None),
        watermark_position=(50, 1.0),
        image_size=1200,
        opacity=0.7
    )
    # add extraction of watermark overlay




    """CoordinatorW.add_watermark_batch(
        watermark_path='./resources/watermarks/sample-watermark-2.png',
        watermark_size=(None, 0.13),
        watermark_position=(50, 0.9),
        image_size=None,
        opacity=0.35
    )"""

# TODO:
# issue: image-size not respected
# issue: watermark ratio not respected
# blur image behind watermark: mean blur? gaussian?

