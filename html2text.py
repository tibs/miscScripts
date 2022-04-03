#!/usr/bin/env python3

"""Simple utility to convert HTML to text, using pandoc

        usage: html2text [<switches>] infile
               html2text [<switches>] -all [directory [directory ...]]
               html2text -auto [directory [directory ...]]

Switches:
   -all          all recognised files in the named directory or directories
                 (default ".") will be processed.
   -v, -verbose  report what is done to each file, as it is done.
   -force        the output file will overwrite any existing file of that name.
   -delete       the input file will be deleted if it is successfully translated.
   -auto         the same as "-all -verbose -delete".
   -compress, -gzip, -z   compress the result with gzip
   -recurse,  -r          recurse through directories, implies -all

Recognised files are those with suffixes .html, .htm, .doc, .docx and .rtf.
"""

import os
import shutil
import subprocess
import sys

from pathlib import Path
from tempfile import mkdtemp


KNOWN_SUFFIXES = ('.html', '.htm', '.doc', '.docx', '.rtf')


def antiword(infile, textfile):
    """Use antiword to convert the file.
    """
    with open(textfile, 'x') as fd:
        subprocess.run(
            [
                'antiword',
                '-f',                   # formatted text
                '-w', '72',             # text width
                infile,
            ],
            check=True,
            stdout=fd,
        )


# pandoc
# -o <output-file>
# -f <input-file-format>   e.g., html, docx, odt, epub
# -t <output-file-format>  e.g., markdown, rst, commonmark, plain (plain text)
# --fail-if-warnings | --verbose | --quiet
# --wrap=auto|none|preserve  auto is default, should be ok
# --columns=N  default 72
# --reference-links  instead of inline links
# <input-file>


def iconv(in_file, out_file):
    """Use iconv to regularise our text encoding.
    """
    with open(out_file, 'x') as fd:
        subprocess.run(
            [
                'iconv',
                '--unicode-subst="?"',
                '--byte-subst="?"',
                '-t', 'UTF-8',
                '-f', 'UTF-8',
                in_file,
            ],
            check=True,
            stdout=fd,
        )


def pandoc(in_file, out_file, text_format='rst'):
    """Use iconv and pandoc to convert the file.
    """
    subprocess.run(
        [
            'pandoc',
            '-o', out_file,
            '-t', text_format,
            '--fail-if-warnings',
            '--reference-links',
            in_file,
        ],
        check=True,
    )


def convert_file(infile, temp_dir, force=0, verbose=0, delete=0, compress=0):
    """Do the actual work of converting a file.
    """
    suffix = infile.suffix

    if suffix not in KNOWN_SUFFIXES:
        if verbose:
            print(f'.. Ignoring    {infile}')
        return

    textfile = infile.with_suffix(suffix + '.txt')

    if textfile.exists() and not force:
        print(f'Cannot write file {textfile}, it already exists')
        return

    in_format = suffix.lower()[1:]

    if verbose:
        print(f'-- Converting  {infile}')

    if in_format == 'doc':
        # If it really is DOC, then antiword is our best bet
        try:
            antiword(infile, textfile)
        except subprocess.CalledProcessError as exc:
            print(f'ERR {exc}')
            return
    else:
        # Pandoc doesn't cope well with stray characters that aren't sensibly
        # encoded, so run the file through iconv first
        temp_file = Path(temp_dir, infile.name)
        print(f'.. via temporary file {temp_file}')
        try:
            iconv(infile, temp_file)
            pandoc(temp_file, textfile)
        except subprocess.CalledProcessError as exc:
            print(f'ERR {exc}')
            return
        finally:
            temp_file.unlink()

    if compress:
        if verbose:
            print(f'   Compressing {textfile}')
        if force:
            subprocess.run(['gzip', '-f', textfile], check=True)
        else:
            subprocess.run(['gzip', textfile], check=True)

    if delete:
        if verbose:
            print(f'   Deleting    {textfile}')
        infile.unlink()


def process_dir(directory, temp_dir, force=0, verbose=0, delete=0, recurse=0, compress=0):
    """Process the files in a directory.
    """
    if not verbose:
        print(f'++ Directory {directory}')

    for dirpath, dirnames, filenames in os.walk(directory):

        for filename in filenames:
            path = Path(dirpath, filename)
            convert_file(path, temp_dir, force, verbose, delete, compress)

        if recurse:
            for dirname in dirnames:
                process_dir(Path(dirpath, dirname), temp_dir, force, verbose, delete, recurse, compress)


def main():
    """Do it."""

    all_files = False
    force = False
    verbose = False
    delete = False
    recurse = False
    compress = False
    infiles  = []

    args  = sys.argv[1:]

    while args:
        word = args.pop(0)

        if word == "-help" or word == "-h":
            print(__doc__)
            return
        elif word == "-force":
            force = True
        elif word in ("-recurse", "-r"):
            recurse = True
            all_files = True
        elif word in ("-compress", "-gzip", "-z"):
            compress = True
        elif word in ("-verbose", "-v"):
            verbose = True
        elif word == "-delete":
            delete = True
        elif word == "-all":
            all_files = True
        elif word == "-auto":
            all_files = True
            delete = True
            verbose = True
        else:
            infiles.append(word)

    temp_dir = mkdtemp()

    try:
        if all_files:
            if not infiles:
                infiles = ['.']
            for dirname in infiles:
                dirpath = Path(dirname)
                if dirpath.is_dir():
                    process_dir(dirname, temp_dir,
                                force=force, verbose=verbose, delete=delete,
                                recurse=recurse, compress=compress)
                else:
                    print(f'!! Ignoring {dirname}, it is not a directory')
        elif len(infiles) == 1:
            convert_file(Path(infiles[0]), temp_dir,
                         force=force, verbose=verbose, delete=delete, compress=compress)
        elif not len(infiles):
            print('No filename given to process')
            print(__doc__)
        else:
            print('Too many names given without -all switch')
            print(__doc__)
    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main()
