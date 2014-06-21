from collections import defaultdict

import os
import re

import optparse

FILE_SIZE_LIMIT = 100 * 1024 * 1024
WORD_SIZE_LIMIT = 20
WORD_SIZE_MIN = 4




parser = optparse.OptionParser()

parser.add_option("-o", "--output", dest="filename", help="File to write the wordlist to", metavar="FILE", default="wordlist.txt")
parser.add_option("-v", "--verbose", dest="verbose", default=False, help="Show verbose information")

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
    ext = os.path.splitext(file)

    print "Processing file: " + file
    process_generic(file)


def process_generic(file):
    """
    Processes the file, extracting all words.
    """
    size = os.path.getsize(file)
    if size > FILE_SIZE_LIMIT:
        print "[Ignoring file %s: Too big]" % file
        return

    content = open(file, "r").read()

    if '\0' in content:
        print "[Ignoring file %s: Binary]" % file
        return

    matches = re.findall(r"[a-zA-Z0-9\-\']+", content)
    for m in matches:
        if len(m) > WORD_SIZE_LIMIT or len(m) < WORD_SIZE_MIN:
            continue
        words[m] += 1


traverse(rootdir)

print words

wordlist = sorted(words, key=lambda k: words[k], reverse=True)
print wordlist
print words["Feature"]


for w in wordlist:
    print w + ": " + str(words[w])