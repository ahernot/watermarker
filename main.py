import coordinator as C


if __name__ == '__main__':
    C.add_watermark(
        image_path='./resources/images/IMG_5613.JPG',
        watermark_path='./resources/watermarks/copyright-whitetransp.tiff',
        watermark_size=(None, 0.1),
        watermark_position=(50, 1.0),
        image_size=1500,
        opacity=0.35
    )
