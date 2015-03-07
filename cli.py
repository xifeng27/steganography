# -*- coding: utf-8 -*-

import bitarray
import click
from PIL import Image

from utils import loop_pixels, reset_channel


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename')
@click.argument('message')
@click.option('--output', default=None)
@click.option('--modulo', default=2)
def encode(filename, output, message, modulo):
    if output is None:
        output = filename

    # get the pixel data
    image = Image.open(filename)
    data = image.getdata()

    bits = bitarray.bitarray()
    bits.fromstring(message)
    bits_list = bits.tolist()

    click.echo(bits.to01())

    # loop through the image and set the data
    index = 0
    max_index = len(bits_list)
    for x in range(0, image.size[0]):
        for y in range(0, image.size[1]):
            pixel = list(data.getpixel((x, y)))
            for i in range(len(pixel)):
                pixel[i] = reset_channel(pixel[i], modulo)
                if index < max_index:
                    pixel[i] += bits_list[index]
                index += 1
            data.putpixel((x, y), tuple(pixel))

    image.putdata(data)
    image.save(output)


@cli.command()
@click.argument('filename')
@click.option('--modulo', default=2)
def decode(filename, modulo):
    image = Image.open(filename)
    data = image.getdata()

    bits = bitarray.bitarray()

    # loop through the image and set the data
    for x in range(0, image.size[0]):
        for y in range(0, image.size[1]):
            pixel = data.getpixel((x, y))
            for i in range(len(pixel)):
                bits.append(pixel[i] % modulo)

    click.echo(bits.tostring())



if __name__ == '__main__':
    cli()
