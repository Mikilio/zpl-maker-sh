#! /usr/bin/env python

import subprocess

shelves = ['1','2','3','4']
sections = ['A','B','C']
etages = [f'N{etage}' for etage in range(0,7)]
location = ['01','02','03','04']

def main():

    strings = []

    for a in shelves:
        for b in sections:
            for c in etages:
                for d in location:
                    strings.append(f"S2S-{a}-{b}-{c}-{d}")

    result = subprocess.check_output(
        ["./mkzpl.py", "-r 5", "-c 2"] + strings,
        text=True
    )
    print(result)

if __name__ == '__main__':
    main()
