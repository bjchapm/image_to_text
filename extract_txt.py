#!/usr/bin/env python3

###
# Ben Chapman
# 2023 Runs pytesseract on a folder with pdf, png, jpg, and tiff files. Outputs
# plaintext files in an output directory. Multi-page pdf and tiff are
# supported. Several packages need to be previously installed
#
# MIT license as described in LICENSE.txt in folder.
###

import time
from statistics import mean
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import glob
import sys
import os
import argparse

timings = []
image_extensions = ('pdf', 'png', 'jpg', 'jpeg', 'tif', 'tiff')

def process_files(image_files, outfolder, skip=False, verbose=False):
    for image_file in image_files:
        start_time = time.time()
        ocr_doc = ''
        images = []
        out_file, ext = os.path.splitext(os.path.basename(image_file))
        out_file = out_file + '.txt'
        out_file = os.path.join(outfolder, out_file)
        if os.path.exists(out_file) and skip:
            if verbose: print(f"Skipping {out_file}.")
            continue
        if image_file.lower().endswith('pdf'):
            images = convert_from_path(image_file, dpi=500)
        elif image_file.lower().endswith(('tif', 'tiff')):
            mytiff = Image.open(image_file)
            for i in range(mytiff.n_frames):
                mytiff.seek(i)
                # required to convert from TIFF to PIL internal
                images.append(mytiff.convert())
        else:
            # Single-page jpg, png, or similar
            images.append(Image.open(image_file))

        for image in images:
            ocr_page = pytesseract.image_to_string(image, lang='eng')
            ocr_doc += ocr_page

        with open(out_file, 'w') as f:
            f.write(ocr_doc)

        elapsed = time.time() - start_time
        timings.append(elapsed)
        if verbose:
            print('--- {:.2f} seconds to OCR {} ---'.format(elapsed, image_file))
        else:
            print("OCR'd {}".format(image_file))

    return timings

def summarize_output(timings):
    avg = 0
    print('===== Finished =====')
    if len(timings) == 0:
        print("No files processed.")
    elif len(timings)>1:
        avg = mean(timings)
    else:
        avg = timings[0]
    if avg>0:
        print('Average time per file: {:.2f}'.format(avg))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="verbose output", action="store_true")
    parser.add_argument("-i", "--infolder", help="input folder containing PDFs to scan")
    parser.add_argument("-o", "--outfolder",
                        help="""folder at same level as input folder
    for output text files. It will be created if necessary.
    Existing output files with same names will be silently overwritten.""")
    parser.add_argument("-s", "--skip",
                        help="""skip files already converted and in output directory. Default is 
    to reprocess them and silently overwrite.""", action="store_true",default=False)
    args = parser.parse_args()
    if not os.path.isdir(args.infolder):
        print('ERROR: Input folder %s not found! Halting.' % args.infolder)
        sys.exit(1)
    if not os.path.isdir(args.outfolder):
        if args.verbose:
            print('Creating %s output folder.' % args.outfolder)
        os.mkdir(args.outfolder)
    files = glob.glob(os.path.join(args.infolder, '*'))
    outfolder = args.outfolder
    image_files = [x for x in files if x.lower().endswith(image_extensions)]
    timings = process_files(image_files, outfolder, skip=args.skip, verbose=args.verbose)
    summarize_output(timings)

