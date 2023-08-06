#!/usr/bin/env python3

import argparse

import pydingo as pdg

parser = argparse.ArgumentParser()
parser.add_argument('host', nargs = '?')
parser.add_argument('--port', type = int)

args = parser.parse_args()

with pdg.Client(args.host, args.port) as cli:
    im = cli.image()
    pdg.dumpexif(im)

    im.show()
