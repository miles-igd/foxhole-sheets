import argparse
import cv2
import json

from sheets.bot import run
from sheets.prepare import process

parser = argparse.ArgumentParser(description='FoxholeSheets CLI')
parser.add_argument('type', metavar='T', type=str,
                    help='bot/input [Start a bot or input an image]')
parser.add_argument('-i', dest='input',
                    help='input filepath')
parser.add_argument('-o', dest='output',
                    help='output filepath')
parser.add_argument('-fo', dest='foutput',
                    help='image output filepath')
parser.add_argument('-ident', dest='ident', action='store_true',
                    help='identify?')

args = parser.parse_args()

if args.type == "bot":
    run()
elif args.type == "input":
    im = cv2.imread(args.input)
    identify = bool(args.ident)
    data, out = process(im, identify=identify)

    output = args.output or "stockpile.json"

    if args.foutput:
        cv2.imwrite(args.foutput, out)

    with open(output, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)