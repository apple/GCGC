#!/bin/bash
set -e
# need to `brew install coreutils` to have `greadlink`
input_file=`( greadlink -f  $1 )`
echo input=$input_file
output_dir=$2
echo writing to $output_dir
mkdir -p $output_dir
cd $output_dir
tar -xvf $input_file --strip-components 2
FILES=`( ls *.hdrlog )`
for f in $FILES
do
  echo "Splitting $f file..."
  java -jar /Users/yak/git/HdrLogProcessing/target/processor.jar split -if $f
  rm $f
done
rm READ-wt.25k-*
rm READ-st.25k-*

java -jar /Users/yak/git/HdrLogProcessing/target/processor.jar union -if ".*.hdrlog" -of workload.hdrlog
rm READ-*
rm WRITE-*

