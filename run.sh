#!/bin/bash


#wav_file=sample_data/F_0101_13y1m_1_dys_part.wav
wav_file=sample_data/F_0101_13y1m_1_dys_part_16k.wav
#wav_file=sample_data/F_1_KSM_04.wav

ext_prorep_imgproc.py -t 0.85 $wav_file tmp/result.dsf
