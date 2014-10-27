# Pyet
====

Pyet is a toy interpreter for a [restricted](#restrictions) subset of the language [Piet](http://www.dangermouse.net/esoteric/piet.html) written in Python.

Pyet is also a testbed for me to learn and apply Python best practices, and as a result its structure may shift substantially from commit to commit.

## Usage

The main Pyet script doesn't directly read image files, instead reading in a custom text representation of a Piet image. You can convert your Piet image file to a Pyet text representation using image_to_source.py as follows:
```
python3 image_to_source.py source.[jpg|png|gif] > source.pyet
```
Once you have your Pyet program, you can interpret it:
```
python3 pyet.py source.pyet
```

For more options, use the `-h` flag:
```
python pyet.py -h
Usage: python pyet.py [options] source_file

Options:
  -h, --help   show this help message and exit
  -d, --debug  print debugging information
```
## Restrictions

Pyet does not yet support:
* The "in" commands (char or int).
* Specifying a codel size. Codels are 1 pixel.
* Color blocks larger than ~1000 codels.

## Requirements

* Python 3.X
* [Pillow](http://pillow.readthedocs.org/) if you'd like to run image_to_source.py to convert an image to a Pyet source file
