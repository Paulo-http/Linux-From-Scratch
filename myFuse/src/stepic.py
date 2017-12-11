# stepic - Python image steganography
# Copyright (C) 2007 Lenny Domnitser
#http://domnit.org/stepic/

import warnings
try:
    import Image
except:
    warnings.warn('Could not find PIL. Only encode_imdata and decode_imdata will work.',
                  ImportWarning, stacklevel=2)

__all__ = ('encode_imdata','encode_inplace', 'encode',
           'decode_imdata', 'decode',
           'Steganographer')

def encode_imdata(imdata, data):
    datalen = len(data)
    if datalen == 0:
        raise ValueError('data is empty')
    if datalen * 3 > len(imdata):
        raise ValueError('data is too large for image')

    imdata = iter(imdata)

    for i in xrange(datalen):
        pixels = [value & ~1 for value in
                  imdata.next()[:3] + imdata.next()[:3] + imdata.next()[:3]]
        byte = ord(data[i])
        for j in xrange(7, -1, -1):
            pixels[j] |= byte & 1
            byte >>= 1
        if i == datalen - 1:
            pixels[-1] |= 1
        pixels = tuple(pixels)
        yield pixels[0:3]
        yield pixels[3:6]
        yield pixels[6:9]


def encode_inplace(image, data):
    w = image.size[0]
    (x, y) = (0, 0)
    for pixel in encode_imdata(image.getdata(), data):
        image.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

def encode(image, data):
    image = image.copy()
    encode_inplace(image, data)
    return image


def decode_imdata(imdata):
    data = []
    imdata = iter(imdata)
    while True:
        pixels = list(imdata.next()[:3] + imdata.next()[:3] + imdata.next()[:3])
        byte = 0
        for c in xrange(7):
            byte |= pixels[c] & 1
            byte <<= 1
        byte |= pixels[7] & 1
        data.append(chr(byte))
        if pixels[-1] & 1:
            break

    return data


def decode(image):
    return ''.join(decode_imdata(image.getdata()))


class Steganographer:
    def __init__(self, image):
        self.image = image
    def encode(self, data):
        return encode(self.image, data)
    def decode(self):
        return decode(self.image)
