#!/bin/bash

# Usage : scp_ext_dsf_img.sh wav_directory output_directory

wav_dir=$1
out_dir=$2

[ -z "$wav_dir" ] && echo "error!! need to wav_directory" && exit 1;
[ -z "$out_dir" ] && echo "error!! need to output_derectory" && exit 1;

rm -rf $out_dir
mkdir $out_dir

find $wav_dir -iname "*.wav" > $out_dir/wavlist.log

while read line
do
  wav_file=$line
  dsf_file=$(echo $line | sed 's#.*/\([A-Za-z_0-9]*\)\.wav#\1.dsf_img#g')

  ext_prorep_imgproc.py -t 0.9 -a 3 -p 30 -o 30 -r 15 "$wav_file" "$outdir"/"$dsf_file"

done < $out_dir/wavlist.log

#ext_prorep_imgproc.py -t 0.9 -a 3 -p 30 -o 30 -r 15 $wav_file $dsf_file
#ext_prorep_imgproc.py -t 0.9 -a 3 -p 30 -o 30 -r 10 $wav_file $dsf_file


: << 'END'
usage: ext_prorep_imgproc.py [-h] [--fmethod FMETHOD] [--smethod SMETHOD]
                             [-t THR] [-a VAD_AGG] [-p VAD_PAD] [-c CLSSQR]
                             [-o OPNSQR] [-r RSIZE] [-e ESIZE] [--vad-plot]
                             [--pro-plot] [--rep-plot]
                             wav_file out_file

positional arguments:
  wav_file           input wave file name
  out_file           output binary file name

optional arguments:
  -h, --help         show this help message and exit
  --fmethod FMETHOD  the METHOD of acoustric feature extraction : mfcc
                     (default), fbank
  --smethod SMETHOD  the METHOD of computing similarity matrix : xcorr
                     (default), eucl
  -t THR             threshold for binarization of image(default=0.9)

VAD option:
  -a VAD_AGG         VAD aggressive number 0~3 (default=0)
  -p VAD_PAD         padding duration of frame for VAD (default=50)

Prolongation option:
  -c CLSSQR          the size of square matrix for closing (default=5)
  -o OPNSQR          the size of square matrix for opening (default=20)

Repetition option:
  -r RSIZE           (RSIZE*10ms) the minimum size of repetition (default=10)
  -e ESIZE           (ESIZE*ESIZE pixel) the size of component for eliminating
                     (default=3)

Plot option:
  --vad-plot         plot the result of VAD (default=Flase)
  --pro-plot         plot the image processing of prolongation (default=Flase)
  --rep-plot         plot the image processing of repetition (default=Flase)
END

