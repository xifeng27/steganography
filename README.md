# Steganography

From [Wikipedia](https://en.wikipedia.org/wiki/Steganography):

> Steganography is the art or practice of concealing a file, message, image, or video within another file, message, image, or video.

This is a Python implementation of Steganography. Currently, any file can be hidden inside any *lossless* image---such as PNG or BMP.

```python
python cli.py encode example.png --input=file.txt
```
