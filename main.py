import coordinator_wrapper as CoordinatorW


# Add batch processing

if __name__ == '__main__':

    CoordinatorW.add_watermark_batch(
        watermark_path='./resources/watermarks/copyright-whitetransp.tiff',
        watermark_size=(None, 0.1),
        watermark_position=(50, 1.0),
        image_size=1500,
        opacity=0.35
    )
