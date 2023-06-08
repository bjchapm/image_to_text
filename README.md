# image_to_text

```
usage: extract_txt.py [-h] [-v] [-i INFOLDER] [-o OUTFOLDER] [-s]

options:
  -h, --help            show this help message and exit
  -v, --verbose         verbose output
  -i INFOLDER, --infolder INFOLDER
                        input folder containing PDFs to scan
  -o OUTFOLDER, --outfolder OUTFOLDER
                        folder at same level as input folder for output text files. It will be
                        created if necessary. Existing output files with same names will be silently
                        overwritten.
  -s, --skip            skip files already converted and in output directory. Default is to
                        reprocess them and silently overwrite.
```

This is a thin layer on top of tesseract that processes a folder of images of
scanned text and creates another folder of OCR'd text files, using the
[https://github.com/tesseract-ocr/tesseract](Tesseract) OCR engine.

It requires:

* tesseract
* pytesseract
* pdf2image 
* PIL

and probably some other things I have forgotten.

## Example

You can test functionality of the script with:

`./extract_txt.py -v -i test -o output`

This will create `output` with text versions of the four input files located in `test`.
