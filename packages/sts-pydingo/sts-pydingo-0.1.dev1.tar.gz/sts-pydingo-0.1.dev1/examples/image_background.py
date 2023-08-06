#!/usr/bin/env python3

import argparse

import pydingo as pdg

parser = argparse.ArgumentParser()
parser.add_argument('host', nargs = '?')
parser.add_argument('--port', type = int)
parser.add_argument('--policy')

args = parser.parse_args()

with pdg.Client(args.host, args.port) as cli:
    if (args.policy is not None):
        cli.set_image_background_policy(args.policy)

    im_bg = cli.image_background()
    im_bg.show()
