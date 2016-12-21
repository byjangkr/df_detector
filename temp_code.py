#!/usr/bin/env python

import argparse
from func import dfio


#parser = argparse.ArgumentParser()
#parser.add_argument("dsf_file",help="input dsf file name")
#args=parser.parse_args()
dsf_file = 'dsf/F_1_KSM_03_r2.dsf'

#dfio.plotprorepimg(dsf_file)

rep_margin = 20 # rep_margin*10ms
pro_img, rep_img = dfio.loadprorepimg(dsf_file)


