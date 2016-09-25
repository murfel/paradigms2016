#!/usr/bin/env python3

import collections
import hashlib
import os
import sys


def find_duplicates(top_dir):
    hash_to_files = collections.defaultdict(set)

    for dirpath, _, files in os.walk(top_dir):
        for filename in files:
            rel_path = os.path.join(dirpath, filename)
            if filename.startswith(('.', '~')) or os.path.islink(rel_path):
                continue
            hasher = hashlib.sha1()
            with open(rel_path, mode='rb') as content:
                while True:
                    data = content.read(1024)
                    if not data:
                        break
                    hasher.update(data)
            hash_to_files[hasher.hexdigest()].add(
                os.path.relpath(rel_path, top_dir))

    for files in hash_to_files.values():
        if len(files) != 1:
            print(':'.join(files))


def main():
    if len(sys.argv) != 2:
        print('Usage: ./find_duplicates.py path/to/directory')
        sys.exit(1)

    top_dir = sys.argv[1]
    find_duplicates(top_dir)

if __name__ == '__main__':
    main()
