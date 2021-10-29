import argparse
import cv2
import json
import logging

try:
    from sheets.bot import run
    discord_found = True
except ModuleNotFoundError as e:
    logging.info("discord.py not found -- to run the bot requires discord.py")

from sheets.core import process

parser = argparse.ArgumentParser(description='FoxholeSheets CLI')
parser.add_argument('type', metavar='T', type=str,
                    help='bot/input [Start a bot or input an image]')
parser.add_argument('-i', dest='input',
                    help='stockpile image input filepath')
parser.add_argument('-o', dest='output',
                    help='json output filepath')
parser.add_argument('-fo', dest='foutput',
                    help='image output filepath')
parser.add_argument('-ident', dest='ident', action='store_true',
                    help='unidentified items will be prompted to be identified and saved into the Icons folder')
parser.add_argument('-min', dest='min', type=float,
                    help='min_error of image similarity (mse). default 0.03')

args = parser.parse_args()

if args.type == "bot" and discord_found:
    run()
elif args.type == "input":
    input_ = args.input or "stockpile.png"
    min_err = args.min or 0.03
    im = cv2.imread(input_)
    identify = bool(args.ident)
    data, out = process(im, identify=identify, min_err=min_err)

    output = args.output or "stockpile.json"

    if args.foutput:
        cv2.imwrite(args.foutput, out)

    with open(output, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)