#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Given an image file, generates an ascii copy for console.

Uses PIL (Python Imaging Library) to do the heavy work.

Requires libjpeg-dev before installing Pil.

"""

__author__ = "David Tran (unsignedzero)"
__copyright__ = "Copyright (C) 2015 David Tran.  All rights reserved."
__credits__ = ["David Tran"]
__email__ = "unsignedzero@gmail.com"
__license__ = "MIT"
__maintainer__ = "David Tran"
__status__ = "Production"
__version__ = "0.1.1"

from argparse import ArgumentParser
from PIL import Image

from rgb_xterm_color_trans import rgb_to_shell_color

### calls external library to map rgb tuple to a color
def pixel_to_color(rgb_value, _):
  """
  Args:
    rgb_value:   (3-tuple int) The rgb value of a pixel

    _:   Ignored variable

  Returns:
    Xterm color string

  Raises:
    See rgb_to_shell_color

  """

  return '\033[48;5;%dm ' % rgb_to_shell_color(rgb_value)

### calls external library to map rgb tuple to ascii greyscale
def pixel_to_greyscape(rgb_value, greyscale):
  """
  Args:
    rgb_value:   (3-tuple int) The rgb value of a pixel

    greyscale:   (str) A string of possible values, in darkest to lightest
      ordering

  Returns:
    Selected pixel

  Raises:
    TypeError

  Calculations:
    average = sum(rgb_value) / 3
    scale_value = average / 256
    step_value = scale_value * len(greyscale)

  """

  return greyscale[int(sum(rgb_value) / 768.0 * len(greyscale))]

### Converts the image file into an ascii "image" string
def transform_image_to_ascii(filename, max_length=40,
                             max_percentage=None, greyscale=""):
  """
  Args:
    filename:   (str) The file this will process.

    max_length:   (int) The max length of the longest side of the image.
      Overridden if max_percentage is not None.

    max_percentage:   (float) The scaled percentage of the input image.

    greyscale:  (str) The set of characters used to select the greyscale.
      If this is None, this will output color.

  Returns:
    Ascii text of image is valid else None.

  Raises:
    See called function and mode.

  Reference:
    http://paulbourke.net/dataformats/asciiart/

  """

  if max_percentage is not None and (
      max_percentage > 1.0 or max_percentage <= 0.0):
    max_percentage = 1.0

  if max_length <= 0:
    max_length = 40

  # Select transformation function
  if greyscale is None:
    color_map_func = pixel_to_color
  elif not greyscale:
    color_map_func = pixel_to_greyscape
    greyscale = (r'''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvun'''
                 r'''xrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. ''')

  with open(filename) as fin:
    image_obj = Image.open(fin)

    width, height = image_obj.size

    if max_percentage is None:
      max_percentage = float(max_length)/min(width, height)

    new_dimensions = (int(width * max_percentage), int(height * max_percentage))
    new_width, new_height = new_dimensions

    new_image_obj = image_obj.resize(new_dimensions, Image.ANTIALIAS)
    new_image_array = new_image_obj.load()

    output_buffer = []
    for y in range(new_height):
      for x in range(new_width):
        color_value = new_image_array[x, y]
        output_buffer.append(color_map_func(color_value, greyscale))
      output_buffer.append('\n')

    return ''.join(output_buffer)

### Processes command line calls
def command_line_process():
  """
  Flags:
    -c. --color:   Sets output to color mode.

    -l=N --len=N --max_length=N:   Sets the max size of the output image
      in either characters or % as a string.

    <files>:   A list of file names that will be processed

  Raises:
    See called functions.

  Returns:
    None
  """

  parser = ArgumentParser(
      description="Given an image file, generates an ascii copy for console.")
  parser.add_argument('--color', '-c',
                      action='store_true', dest='color',
                      help="Set color output")
  parser.add_argument('--max_length', '--len', '-l',
                      action='store', dest='length', default=40,
                      help=('Set max size of output image, '
                            "could be percent, or size, default 40"))
  parser.add_argument('files',
                      metavar='file', type=str, nargs='+',
                      help="The input image files for parsing")


  args = vars(parser.parse_args())

  max_length = None
  max_percentage = None

  try:
    max_length = int(args['length'])
  except ValueError:
    try:
      if '%' in args['length']:
        max_percentage = args['length'].split('%', 1)[0]
    except TypeError:
      raise TypeError("img2sh recieved bad length value %s" % args['length'])

  color_mode = args['color']
  input_color_mode = None if color_mode else ''

  for each_file_name in args['files']:
    print(transform_image_to_ascii(
        filename=each_file_name, max_length=max_length,
        max_percentage=max_percentage, greyscale=input_color_mode))

if __name__ == '__main__':
  command_line_process()
