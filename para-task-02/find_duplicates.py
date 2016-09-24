#!/usr/bin/env python3

import collections
import hashlib
import os
import sys


def find_duplicates(directory):
    file_group = collections.defaultdict(set)

    for dirpath, _, files in os.walk(directory):
        for filename in files:
            rel_path = os.path.join(dirpath, filename)
            if (filename.startswith('.') or filename.startswith('~')
                    or os.path.islink(rel_path)):
                continue
            file_hash = hashlib.sha1()
            with open(rel_path, mode='rb') as content:
                while True:
                    data = content.read(1024)
                    if not data:
                        break
                    file_hash.update(data)
            file_hexdigest = file_hash.hexdigest()
            file_shortname = os.path.relpath(rel_path, directory)
            file_group[file_hexdigest].add(file_shortname)

    for v in file_group.values():
        if len(v) != 1:
            print(':'.join(v))


def main():
    if len(sys.argv) != 2:
        print('Usage: ./find_duplicates.py path/to/directory')
        sys.exit(1)

    directory = sys.argv[1]
    find_duplicates(directory)

if __name__ == '__main__':
    main()
