# -*- coding: utf-8 -*-

import sys

import bitarray
import click
import humanize
from PIL import Image


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename')
@click.option('--modulo', default=2)
def info(filename, modulo):
    image = Image.open(filename)
    bits = image.size[0] * image.size[1] * modulo * len(image.getpixel((0, 0)))
    click.echo('Potential data: {x}'.format(x=humanize.naturalsize(bits)))


@cli.command()
@click.argument('filename')
@click.option('--message', default=None)
@click.option('--input', type=click.File('rb'), default=None)
@click.option('--output', default=None)
@click.option('--modulo', default=2)
def encode(filename, input, output, message, modulo):
    bits = bitarray.bitarray()

    if output is None:
        output = filename
    if input is not None:
        bits.frombytes(input.read())
    else:
        bits.frombytes(message.encode('utf_16_be'))

    # get the pixel data
    image = Image.open(filename)
    data = image.getdata()

    total_channels = image.size[0] * image.size[1] * len(image.getpixel((0, 0)))
    total_bits = total_channels * modulo

    bits_list = bits.tolist()

    # loop through the image and set the data
    index = 0
    max_index = len(bits_list)

    if max_index > total_bits:
        click.echo("Target image too small: {target}. Size required: {req}.".format(
            target=humanize.naturalsize(total_bits), req=humanize.naturalsize(max_index),
        ))
        exit(1)

    for x in range(0, image.size[0]):
        for y in range(0, image.size[1]):
            pixel = list(data.getpixel((x, y)))
            for i in range(len(pixel)):
                # reset the channel
                pixel[i] = pixel[i] - pixel[i] % modulo
                if index < max_index:
                    # hide a bit inside the channel
                    pixel[i] += bits_list[index]
                index += 1
            data.putpixel((x, y), tuple(pixel))
        sys.stdout.write("\r%d%%" % (float(index) / float(total_channels) * 100))
        sys.stdout.flush()

    image.putdata(data)
    image.save(output)

    sys.stdout.write("\r\n")
    sys.stdout.flush()


@cli.command()
@click.argument('filename')
@click.argument('output', default=None)
@click.option('--modulo', default=2)
def decode(filename, output, modulo):
    image = Image.open(filename)
    data = image.getdata()

    bits = bitarray.bitarray()

    total_channels = image.size[0] * image.size[1] * len(image.getpixel((0, 0)))
    total_bits = total_channels * modulo

    index = 0

    # loop through the image and set the data
    for x in range(0, image.size[0]):
        for y in range(0, image.size[1]):
            pixel = data.getpixel((x, y))
            for i in range(len(pixel)):
                bits.append(pixel[i] % modulo)
                index += 1
        if output is not None:
            sys.stdout.write("\r%d%%" % (float(index) / float(total_channels) * 100))
            sys.stdout.flush()

    if output is not None:
        with open(output, 'wb') as f:
            f.write(bits.tobytes())
        sys.stdout.write("\r\n")
        sys.stdout.flush()
    else:
        click.echo(bits.tobytes())


if __name__ == '__main__':
    cli()
