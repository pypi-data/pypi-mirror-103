import PIL.Image
import PIL.TiffTags

def dumpexif(im, fix = True):
    exif = im.getexif()

    if fix:
        ImageWidthExifTag = 0x0100
        if (ImageWidthExifTag not in exif):
            exif[ImageWidthExifTag] = im.width

        ImageLengthExifTag = 0x0101
        if (ImageLengthExifTag not in exif):
            exif[ImageLengthExifTag] = im.height

    for tag, value in exif.items():
        if isinstance(value, bytes):
            value = value.decode('utf-8')

        tag_info = PIL.TiffTags.lookup(tag)
        print(f'{tag_info.name}: {value}')
