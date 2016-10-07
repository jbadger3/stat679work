#This script will summarize the results from all of the analysis and place
#them in a csv file name summary.csv

#first write the column names for the table into a new file
echo 'analysis,h,CPUtime' > summary.csv



#loop through each log file. get the name and hybridizations from the log file.
#then get the CPUtime for the analysis and write all values to the summary.csv file
for filename in hw1-snaqTimeTests/log/timetest??_snaq.log
do
  #get the name of the file XXX.log
  analysis=$(echo $filename | grep -o 'timetest\d\d_snaq')
  #get the value of hmax
  hmax=$(grep -o  'hmax = \d\+' "$filename" | grep -o  "\d*$")
  #get the digits in the filename
  digits=$(echo $filename | grep -o '\d*_snaq.log$' | grep -o '\d*')
  #find the Elapsed time line in the file then get the time in seconds
  cpuTime=$(grep -i 'Elapsed time' "hw1-snaqTimeTests/out/timetest"$digits"_snaq.out" | grep -Eo '\d+\.\d+')
  #append the summary line of the analysis to the summary file
  echo "$analysis,$hmax,$cpuTime" >> summary.csv

done
