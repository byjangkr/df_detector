#!/bin/bash

# Usage : scp_ext_dsf_feat.sh dsf_img_directory output_file

dsf_img_dir=$1
out_file=$2

[ -z "$dsf_img_dir" ] && echo "error!! need to dsf_img_directory" && exit 1;
[ -z "$out_file" ] && echo "error!! need to output_file" && exit 1;

cd df_detector
find $dsf_img_dir -iname "*.dsf" > $dsf_img_dir/dsfimglist.log

touch $out_file
while read line
do
  dsf_img_file=$line
  target_file=$(echo $line | sed 's#.*/\([A-Za-z_0-9]*\)\.dsf#\1#g')
  
  echo -n "$target_file " >> $out_file
  ext_dsffeat_dsfimg.py $dsf_img_file >> $out_file

done < $dsf_img_dir/dsfimglist.log

: << 'END'
usage: ext_dsffeat_dsfimg.py [-h] [-m OUTMODE] [-o OUTFILE] dsf_img_file

positional arguments:
  dsf_img_file  input dsfimg file name

optional arguments:
  -h, --help    show this help message and exit
  -m OUTMODE    the mode of output : outscreen (default), pckout, txtappend
  -o OUTFILE    the output file name for pckout or txtappend of outmode
END
