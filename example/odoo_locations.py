#! /usr/bin/env python

import tempfile
import subprocess
import sys

shelves = ['dummy']
sections = ['P']
etages = [f'{etage}' for etage in range(0,9)]
location = [f'{loc}0' for loc in range(0,4)]

def main():

    strings = []

    for a in shelves:
        for b in sections:
            for c in etages:
                for d in location:
                    strings.append(f"FB1-{b}{c}{d}")


    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as tmp:
        for s in strings:
            tmp.write(s + "\n")
        temp_path = tmp.name

    result = subprocess.run(
        ["./mkzpl.py", "--file", temp_path, "-r", "10", "-c", "2"],
    )

    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)


if __name__ == '__main__':
    main()
