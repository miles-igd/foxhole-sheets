import argparse
import cv2
import json
import logging

from sheets.stockpile import Stockpile

parser = argparse.ArgumentParser(description='FoxholeSheets CLI')
parser.add_argument('-i', dest='input',
                    help='stockpile image input filepath')
parser.add_argument('-o', dest='output',
                    help='json output filepath')
parser.add_argument('-fo', dest='foutput',
                    help='image output filepath')
parser.add_argument('-min', dest='min', type=float,
                    help='min_error of image similarity (mse). default 0.03')
parser.add_argument('-ident', dest='ident', action='store_true')

args = parser.parse_args()

input_ = args.input or "stockpile.png"
min_err = args.min or 0.03
im = cv2.imread(input_)
stockpile = Stockpile(im)

output = args.output or "stockpile.json"

if args.ident:
    print(stockpile.unidentified)

if args.foutput:
    cv2.imwrite(args.foutput, out)

with open(output, "w") as f:
    json.dump(stockpile.data, f, indent=4, sort_keys=True)