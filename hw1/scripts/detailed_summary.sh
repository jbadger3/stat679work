#This script will further summarize the snaq data and store the results in the results folder
#as a file named 'detailed_summary.csv'


echo 'analysis,h,CPUtime,Nruns,Nfail,fabs,frel,xabs,xrel,seed,under3460,under3450,under3440' > results/detailed_summary.csv

#loop through each log file. get the name and hybridizations from the log file.
#then get the CPUtime for the analysis and write all values to the summary.csv file
for filename in hw1-snaqTimeTests/log/*
do

  #get the name of the file XXX.log
  analysis=$(basename $filename | cut -d. -f1)

  #get the value of hmax
  hmax=$(grep "hmax = \d\+" "$filename" | grep -o '\d\+')

  #trim the filename to handle both .out and .log files
  trimmed_name=$(basename $filename | sed -E 's/(^.*\.)(.*)/\1\out/')

  #find the Elapsed time line in the file then get the time in seconds
  cpuTime=$(grep -i 'Elapsed time' "hw1-snaqTimeTests/out/$trimmed_name" | grep -Eo '\d+\.\d+')

  #get the successful # of runs '
  n_runs=$(grep -rEo "seconds in (\d+) successful runs" "hw1-snaqTimeTests/out/$trimmed_name" | sed -E 's/^.* in ([0-9]+) .*/\1/')

  #get max # of failed proposals
  #n_fail=$(grep "max number of failed proposals" hw1-snaqTimeTests/log/timetest01_snaq.log | sed -E 's/.* proposals = ([0-9]+).*/\1/')
  #after confering with classmate this sed implementation works better than grep
  n_fail=$(sed -nE 's/.*seconds in ([0-9]+) successful runs/\1/p' hw1-snaqTimeTests/out/$trimmed_name)

  #get "ftolAbs" in the log file (tolerateddifference in the absolute value of the score function, to stop the search)
  f_abs=$(grep "ftolAbs" $filename | cut -d, -f2 | cut -d= -f2)

  #get "ftolRel" in log file
  f_rel=$(grep "ftolAbs" $filename | cut -d, -f2 | cut -d= -f2)

  #get "xtolAbs" in log file
  x_abs=$(grep "xtolAbs" $filename | cut -d= -f2 | cut -d, -f1)

  #get "xtolRel" in log file
  x_rel=$(grep "xtolRel" $filename | cut -d= -f3 | sed -E 's/(.*).$/\1/')

  #get "main seed" for first runs
  seed=$(grep "main seed" $filename | sed -E 's/.* ([0-9]+)/\1/')

  #get -loglik of best network
  #since the loglik is in the last field desired, rev the string first, then cut, and rev back
  logliks=$(grep -E "\-loglik of best" $filename | rev | cut -d ' ' -f 1 | rev | cut -d. -f1)

  under3440=0
  under3450=0
  under3460=0

#creat a loop and keep track of all logliks that fall below specified thresholds
  for number in $logliks
  do
    if [ $number -lt 3440 ]
    then
      ((under3440++))
    fi

    if [ $number -lt 3450 ]
    then
      ((under3450++))
    fi

    if [ $number -lt 3460 ]
    then
      ((under3460++))
    fi
  done

  #append the summary line of the analysis to the summary file
  echo "$analysis,$hmax,$cpuTime,$n_runs,$n_fail,$f_abs,$f_rel,$x_abs,$x_rel,$seed,$under3460,$under3450,$under3440" >> results/detailed_summary.csv

done
