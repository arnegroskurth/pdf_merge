# pdf_merge

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

## AppImage

This tool comes with a build-script to package it up as an [AppImage](https://appimage.org/).

This might seem to be a little over-engineered for such a simple tool but I just wanted to take the chance to play around with this otherwise really promising technology.

```bash
$ ./build/AppImage/build.sh
...

Result: .../build/pdf_merge.AppImage

Success!
```

> This script requires `make` and `wget`

## License

MIT