# Homework 1

This directory will contain all the original data for HW1.  Below is the sequence of how the homework was completed.
* Note: all scripts should be run from /hw1

- *9/18/2016* The files from the git repo were copied to a working directory

`sudo cp -r ../course_repo/coursedata/hw1-snaqTimeTests/ hw1`  

- *9/18/2016* A shell script was created `normalizeFileNames.sh` to change all log and out file names from format
   `timetesty_snaq.xxx` to `timetest0y_snaq.xxx` where "y" is a digit between 1 and 9.

`sh scripts/normalizeFileNames.sh` edited: *10/6/2016*
- *9/25/2016* A shell script was created summarizeSNaQres.sh to summarize the results of the snaq runs.  The file summary.csv contains three fields: analysis, hmax, and CPUtime for each run.

`sh scripts/summarizeSNaQres.sh` edited: *10/6/2016*

- *10/6/2016* The file structure of the assignment was updated.  A new folder scripts was created and both previous scripts `normalizeFileNames.sh` and `summarizeSNaQres.sh` were moved to that location. A new folder results was also created and 'summary.csv' was moved to the new location.  All new results will also be stored here

- *10/7/2016* A new script `detailed_summmary.sh` was created to gather a more detailed summary of the snaqTimeTests

`sh scripts/detailed_summary.sh`
