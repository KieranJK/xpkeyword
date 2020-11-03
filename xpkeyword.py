from PIL import Image
import piexif


def decode(t):
    """
    Takes a exif XPKeywords tag and decodes it to a text string
    """
    b = bytes(t)
    return b[:-2].decode('utf-16-le')


def encode(s):
    """
    Takes a text string and encodes it as an exif XPKeywords tag
    """
    b = s.encode('utf-16-le') + b'\x00\x00'
    return tuple([int(i) for i in b])


def get_tags(file):
    """
    Reads the exif XPKeyword tags of an image and returns them as a stirng
    """
    im = Image.open(file)
    exif_dict = piexif.load(im.info["exif"])
    keyword = exif_dict["0th"][piexif.ImageIFD.XPKeywords]
    keyword = decode(keyword)
    im.close()
    return keyword


def write_tags(file, string):
    """
    Writes exif XPKeyword tags to an image
    """
    im = Image.open(file)
    keyword = encode(string)
    exif_dict = piexif.load(im.info["exif"])
    exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keyword
    exif_bytes = piexif.dump(exif_dict)
    im.save(file, exif=exif_bytes)
