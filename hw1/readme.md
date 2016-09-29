# Homework 1

This directory will contain all the original data for HW1.  Below is the sequence of how the homework was completed.
- *9/18/2016* The files from the git repo were copied to a working directory

`sudo cp -r ../course_repo/coursedata/hw1-snaqTimeTests/ hw1`  

- *9/18/2016* A shell script was created `normalizeFileNames.sh` to change all log and out file names from format
   `timetesty_snaq.xxx` to `timetest0y_snaq.xxx` where "y" is a digit between 1 and 9.

`sh normalizeFileNames.sh`
- *9/25/2016* A shell script was created summarizeSNaQres.sh to summarize the results of the snaq runs.  The file summary.csv contains three fields analysis, hmax, and CPUtime for each run.

`sh summarizeSNaQres.sh`
