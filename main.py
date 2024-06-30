import os
import zpl
import argparse
import csv
import sys
import math


height = 100 # in mm
width = 60 # in mm
dpmm = 12.0 # dots per mm
x = 3 # width of narrow bar in dots
padding= 3  #padding around barcode in mm
bar_height = 10
label_height = 4 #TODO calculate

def print_table(rows, cols, strings):
    """Print a table with the specified number of rows and columns."""


    l = zpl.Label(height, width, dpmm = dpmm)
    l.set_default_font( label_height * 0.8, 2)
    max_len = max(len(s) for s in strings)
    bar_width = (34 + max_len*11 ) * x / dpmm #assuming code 128
    required_width = (bar_width + 2 * padding) * cols
    required_height = ( bar_height + 2 * padding + label_height) * rows

    if required_height > height or required_width > width:
        print(f"""
            With the parameters specified it won't fit on your label"
            required height is {required_height}
            required height is {required_height}
        """)
        sys.exit(1)

    for i in range(0, rows):
        for j in range(0, cols):
            try:
                s = strings[i*cols+j]
                l.origin(
                    j * (bar_width + 2 * padding) + padding ,
                    i * (bar_height + 2 * padding + label_height) + padding
                )
                l.barcode(
                    'C',s,
                    height= math.floor(bar_height * dpmm),
                    print_interpretation_line='N'
                )
                l.endorigin()
                l.origin(
                    j * (bar_width + 2 * padding) + padding ,
                    (i+1) * (bar_height + 2 * padding) + (i+0.2)*label_height - padding
                )
                l.textblock( bar_width/2, justification='C' )
                l.write_text(s)
                l.endorigin()
            except IndexError:
                break
    print(l.dumpZPL())
    l.preview(outputfile='./preview.png')


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
    parser.add_argument('-r', type=int, default=5, help='Number of rows (default 5)')
    parser.add_argument('-c', type=int, default=2, help='Number of columns (default 2)')
    parser.add_argument('strings', nargs='*', help='List of strings to display in table')
    parser.add_argument('--csv', type=str, help='Path to a CSV file')

    args = parser.parse_args()

    if args.csv:
        strings, num_rows, num_cols = read_csv(args.csv)
        print(f"CSV Rows: {num_rows}, Columns: {num_cols}")
        print_table(num_rows, num_cols, strings)
    else:
        if not args.strings:
            print("No strings provided. Use --help for usage information.")
            sys.exit(1)
        print_table(args.r, args.c, args.strings)


if __name__ == '__main__':
    main()

