from collections import defaultdict

import os
import re

import optparse
import pdfmine


FILE_SIZE_LIMIT = 100 * 1024 * 1024
WORD_SIZE_LIMIT = 20
WORD_SIZE_MIN = 4




parser = optparse.OptionParser()

parser.add_option("-o", "--output", action="store", dest="filename", help="File to write the wordlist to", metavar="FILE", default="wordlist.txt")
parser.add_option("-v", "--verbose", action="store", dest="verbose", default=1, help="Show verbose information (0: nothing, 1: file, 2: debug")
parser.add_option("-f", "--folder", action="store", dest="rootfolder", help="Root folder to start processing recursively")

words = defaultdict(int)


(options, args) = parser.parse_args()



def traverse(rootdir):
    """
    Traverses through the specified directory and its subfolders, processing
    all files found.
    """
    for root, dirs, files in os.walk(rootdir):
        for f in files:
            file = os.path.join(root, f)
            process_file(file)


def process_file(file):
    root, ext = os.path.splitext(file)

    if options.verbose >= 1:
        print "Processing file: " + file

    if ext.lower() == ".pdf":
        process_pdf(file)
    else:
        process_generic(file)

def process_pdf(file):
    """
    Processes PDF files, converting them to text and extracting
    words.
    """
    try:
        text = pdfmine.convert_pdf_to_txt(file)
        process_text(text)
    except:
        print "[Ignoring PDF file %s: Error in the reader]" % file

def process_generic(file):
    """
    Processes the file, extracting all words.
    """
    size = os.path.getsize(file)
    if size > FILE_SIZE_LIMIT:
        if options.verbose >= 1:
            print "[Ignoring file %s: Too big]" % file
        return

    content = open(file, "r").read()
    process_text(content)


def process_text(text):
    """
    Processes the specified text.
    """
    if '\0' in text:
        if options.verbose >= 1:
            print "[Ignoring file %s: Binary]" % file
        return

    matches = re.findall(r"[a-zA-Z0-9\-\']+", text)
    for m in matches:
        if len(m) > WORD_SIZE_LIMIT or len(m) < WORD_SIZE_MIN:
            continue
        words[m] += 1




traverse(options.rootfolder)

wordlist = sorted(words, key=lambda k: words[k], reverse=True)


outfile = open(options.filename, "w")

for w in wordlist:
    outfile.write(w + "\n")
    if options.verbose >= 2:
        print w + ": " + str(words[w])

print "Wordlist %s generated with %d words" % (options.filename, len(wordlist))

outfile.close()

