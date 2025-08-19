#! /usr/bin/env python

import os
import zpl
import argparse
import sys
import math


height = 151 # in mm
width = 104 # in mm
dpmm = 8 # dots per mm
page_margin = 8 # margin of actual label to printing surface in mm
min_padding= 2  #padding around barcode in mm
bar_height = 10
bar_width = 18
label_height = 8 #height of label (influences font size)
label_width = 18 #height of label (influences font size)
vertical = False
prefix = "FB1"

def print_table(strings):
    """Generate ZPL tables split across multiple labels and save to 'output'."""

    if vertical:
        rows = math.floor((height - 2 * page_margin)/ (bar_height + 2 * min_padding + label_height))
        cols = math.floor((width- 2 * page_margin)/ (bar_width + 2 * min_padding))
    else:
        rows = math.floor((height - 2 * page_margin) / (bar_height + 2 * min_padding))
        cols = math.floor((width - 2 * page_margin) / (bar_height + 2 * min_padding + label_width))

    hpadding = min_padding
    vpadding = min_padding

    if vertical:
        vpadding = math.floor(((height - 2 * page_margin)/ rows - ( bar_height + label_height))/2)
        hpadding = math.floor(((width - 2 * page_margin)/ cols - bar_width)/2)
    else:
        vpadding = math.floor(((height - 2 * page_margin)/ rows - bar_height)/2)
        hpadding = math.floor(((width - 2 * page_margin)/ cols - (bar_width + label_width))/2)

    labels_per_page = rows * cols

    with open("output.ZPL", "w", encoding="utf-8") as out_file:
        for page_start in range(0, len(strings), labels_per_page):
            chunk = strings[page_start:page_start + labels_per_page]

            l = zpl.Label(height, width, dpmm=dpmm)

            max_len = max(len(s) for s in chunk)
            x = math.floor(bar_width * dpmm / (34 + (max_len + len(prefix)) * 11))  # Code 128 assumption
            l.zpl_raw(f"^BY{x}")
            l.set_default_font(label_height, label_width / max_len)

            for i in range(rows):
                for j in range(cols):
                    idx = i * cols + j
                    if idx >= len(chunk):
                        break
                    s = chunk[idx]

                    # Barcode
                    if vertical:
                        l.origin(
                            j * (bar_width + 2 * hpadding) + hpadding + page_margin,
                            i * (bar_height + 2 * vpadding + label_height) + vpadding + page_margin
                        )
                    else:
                        l.origin(
                            j * 2 * (bar_width + hpadding) + hpadding + page_margin,
                            i * (bar_height + 2 * vpadding) + vpadding + page_margin
                        )
                    l.barcode(
                        'C', prefix + s,
                        height=math.floor(bar_height * dpmm),
                        print_interpretation_line='N'
                    )
                    l.endorigin()

                    # Text
                    if vertical:
                        l.origin(
                            j * (bar_width + 2 * hpadding) + hpadding + page_margin + (bar_width - label_width) * 0.20,
                            (i + 1) * (bar_height + label_height + 2 * vpadding) + vpadding + bar_height + min_padding + page_margin
                        )
                        l.textblock(label_width, justification='C')
                    else:
                        l.origin(
                            j * (bar_width + label_width + 2*hpadding) + bar_width + hpadding + page_margin,
                            i * (bar_height + 2 * vpadding) + vpadding + (bar_height - label_height) * 0.8 + page_margin
                        )
                        l.textblock(label_width, justification='L')
                    l.write_text(s)
                    l.endorigin()

            # Write ZPL to file
            out_file.write(l.dumpZPL())
            out_file.write("\n")  # separate labels

            # Optional preview per label
            if (page_start // labels_per_page) == 0:
                l.preview(outputfile=f'./preview_{page_start // labels_per_page}.png')

def read_csv(file_path):
    """Read a CSV file and return its contents, number of rows, and number of columns."""
    strings = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        for row in data:
            strings.extend(row)
    num_rows = len(data)
    num_cols = len(data[0]) if data else 0
    return strings, num_rows, num_cols

def main():
    parser = argparse.ArgumentParser(description="Process some strings or a CSV file.")
    parser.add_argument('strings', nargs='*', help='List of strings to display in table')
    parser.add_argument('--file', type=str, help='Path to a file containing all strings')

    args = parser.parse_args()

    if args.file:
        strings = list(open(args.file, "r", encoding="utf-8"))
        print_table(strings)
        return

    if not args.strings:
        print("No strings provided. Use --help for usage information.")
        sys.exit(1)
    print_table(args.strings)


if __name__ == '__main__':
    main()

