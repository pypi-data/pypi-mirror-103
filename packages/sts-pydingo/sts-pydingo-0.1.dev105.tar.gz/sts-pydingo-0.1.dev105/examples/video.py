#!/usr/bin/env python3

import argparse

import pydingo as pdg

parser = argparse.ArgumentParser()
parser.add_argument('host', nargs = '?')
parser.add_argument('--port', type = int, default = 8080)

args = parser.parse_args()

with pdg.Client(args.host, args.port) as cli:
    vid = cli.video()
    for vid_frame in vid.decode(video = 0):
        print(vid_frame)
