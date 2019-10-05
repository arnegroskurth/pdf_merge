# pdf_merge

[![Build Status](https://travis-ci.org/arnegroskurth/pdf_merge.svg?branch=master)](https://travis-ci.org/arnegroskurth/pdf_merge)

This is a small tool for merging together pdf files.

```
usage: pdf_merge.py [-h] [-i PATH] [-o PATH] [-m MODULO] [--pages-csv PATH]
                    [--pages-csv-separator PAGES_CSV_SEPARATOR] [-v]

Merges together a bunch of pdf files.

optional arguments:
  -h, --help            show this help message and exit
  -i PATH, --input-path PATH
                        Read source pdfs from PATH.
  -o PATH, --output-path PATH
                        Write merged pdf to PATH. Default: './merged.pdf'.
  -m MODULO, --modulo MODULO
                        Adds pages to the end of each document to fulfil
                        (nPages % MODULO == 0) for each merged document.
  --pages-csv PATH      Write input file page counts into 'PATH.csv'. ('Do I
                        really want to include that in my file?)
  --pages-csv-separator PAGES_CSV_SEPARATOR
                        Use given CSV separator. Defaults to ';'.
  -v, --verbose         Turn on verbose output.

```

## Why?

- __Insert blank pages for print__

  I wanted to concatenate a large number of scientific publications into a single pdf ready to be printed at the copy-shop. Additionally, I want to print double-sided and/or in a _n-pages-on-1_-fashion while being able to afterwards separate the individual publications out again without them overlapping within on a single physical piece of paper. The `--modulo MODULO` argument solves this problem.

  E.g.: If you want to print _4-pages-on-1_ double-sided you want to use a modulus of _4 * 2 = 8_.

- __Extract page counts__

  Moreover, I might want to exclude some publications from the print e.g. in case they are just an article within a book that I have as a complete pdf in my bibliography software. Using the `--pages-csv` argument helps to find those input files with unreasonable page counts which I then can exclude from the print.

## AppImage

This tool comes with a build-script to package it up as an [AppImage](https://appimage.org/).

This might seem to be a little over-engineered for such a simple tool but I just wanted to take the chance to play around with this otherwise really promising technology.

```bash
$ ./AppImage/build.sh
...

Result: .../build/pdf_merge.AppImage

Success!
```

> This script requires `make` and `wget`

## License

MIT