#!/usr/bin/env python3

import argparse

import pydingo as pdg

parser = argparse.ArgumentParser()
parser.add_argument('host', nargs = '?')
parser.add_argument('--port', type = int)
parser.add_argument('--frequency', type = float, default = 1)
parser.add_argument('--expiry', type = float, default = 15)
parser.add_argument('--show', type = int)

args = parser.parse_args()

ims = []
with pdg.Client(args.host, args.port) as cli:
    @cli.image_every(args.frequency, args.expiry)
    def callback(im):
        if (len(ims) > 0):
            print()

        pdg.dumpexif(im)
        ims.append(im)

    if (args.show is not None):
        im = ims[args.show]
        im.show()
