#!/usr/bin/env python

import argparse
from func import dfio


parser = argparse.ArgumentParser()
parser.add_argument("dsf_file",help="input dsf file name")
args=parser.parse_args()

dfio.plotprorepimg(args.dsf_file)
