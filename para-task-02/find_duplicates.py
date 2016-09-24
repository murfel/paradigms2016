#!/usr/bin/env python3

from os import path, sys, walk
from hashlib import sha1


def find_duplicate(directory):
    file_group = dict()

    offset = len(directory)
    for dirpath, dirname, files in walk(directory):
        for filename in files:
            rel_path = path.join(dirpath, filename)
            if (filename.startswith('.') or filename.startswith('~')
                    or path.islink(rel_path)):
                continue
            file_hash = sha1()
            with open(rel_path, mode='rb') as content:
                while True:
                    data = content.read(1024)
                    if not data:
                        break
                    file_hash.update(data)
            file_hash = file_hash.hexdigest()
            if file_hash not in file_group:
                file_group[file_hash] = set()
            file_group[file_hash].add(rel_path[offset:])

    for v in file_group.values():
        if len(v) != 1:
            print(':'.join(v))


def main():
    if len(sys.argv) != 2:
        print('Usage: ./find_duplicate.py path/to/directory/')
        sys.exit(1)

    directory = sys.argv[1]
    find_duplicate(directory)

if __name__ == '__main__':
    main()
