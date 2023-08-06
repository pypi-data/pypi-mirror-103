#!/usr/bin/env python3

import pydingo as pdg

with pdg.Client() as cli:
    print('client connected to {} on port {}'.format(cli.hostname, cli.port))
