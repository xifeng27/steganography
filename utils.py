# -*- coding: utf-8 -*-


def loop_pixels(image):
    pixels = image.load()
    for x in range(0, image.size[0]):
        for y in range(0, image.size[1]):
            yield pixels[x, y]


def reset_channel(channel, modulo):
    return channel - channel % modulo
