
from argparse import ArgumentParser
from glob import glob
from os.path import abspath, basename
from PyPDF2 import PdfFileReader, PdfFileWriter

parser = ArgumentParser(description="Merges together a bunch of pdf files.")

parser.add_argument("-i", "--input-path", dest="input_path", default=".", help="Read source pdfs from PATH.", metavar="PATH")
parser.add_argument("-o", "--output-path", dest="output_path", default="merged.pdf", help="Write merged pdf to PATH. Default: './merged.pdf'.", metavar="PATH")
parser.add_argument("-m", "--modulo", type=int, dest="modulo", help="Adds pages to the end of each document to fulfil (nPages %% MODULO == 0) for each merged document.", metavar="MODULO")
parser.add_argument("--pages-csv", dest="pages_csv_path", help="Write input file page counts into 'PATH.csv'. ('Do I really want to include that in my file?)", metavar="PATH")
parser.add_argument("--pages-csv-separator", dest="pages_csv_separator", default=";", help="Use given CSV separator. Defaults to ';'.")
parser.add_argument("-v", "--verbose", dest="verbose", help="Turn on verbose output.", action="store_true")

args = parser.parse_args()

input_path = abspath(args.input_path)
output_path = abspath(args.output_path)
modulo = args.modulo
pages_csv_path = abspath(args.pages_csv_path) if args.pages_csv_path else None
pages_csv_separator = args.pages_csv_separator
verbose = args.verbose

input_file_paths = glob("%s/*.pdf" % input_path)

if not input_file_paths:
    print("No input files found in '%s'. Exiting." % input_path)
    exit(1)

pages_csv_file = None
if pages_csv_path:
    pages_csv_file = open(pages_csv_path, "w")
    pages_csv_file.write("File%sPages\n" % pages_csv_separator)

output_document = PdfFileWriter()

for input_path in input_file_paths:

    input_file_path = abspath(input_path)
    input_file_name = basename(input_file_path)

    if input_file_path in [output_path]:
        continue

    if verbose:
        print("Reading in '%s'..." % input_file_name)

    input_document = PdfFileReader(open(input_file_path, 'rb'), strict=False)

    if pages_csv_file:
        pages_csv_file.write("%s%s%i\n" % (input_file_name, pages_csv_separator, input_document.getNumPages()))

    output_document.appendPagesFromReader(input_document)

    if modulo and input_document.getNumPages() % modulo != 0:

        missing_pages = modulo - (input_document.getNumPages() % modulo)

        if verbose:
            print("   Adding %i blank pages to %i-sided document" % (missing_pages, input_document.getNumPages()))

        for i in range(0, missing_pages):
            output_document.addBlankPage()

if pages_csv_file:
    pages_csv_file.close()
    if verbose:
        print("Wrote pages-csv to '%s'" % pages_csv_path)

if verbose:
    print("Writing merged pdf to '%s'..." % output_path)

output_stream = open(output_path, "wb")
output_document.write(output_stream)
output_stream.close()

if verbose:
    print("Done!")
