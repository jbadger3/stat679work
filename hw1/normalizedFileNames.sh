#change all file names
#`timetesty_snaq.log` to `timetest0y_snaq.log` where "y" is a digit between 1 and 9.
#Similarly, change `timetesty_snaq.out` to `timetest0y_snaq.out`.

declare -i counter=1
for filename in hw1-snaqTimeTests/log/timetest?_snaq.log
do
  #echo $filename
  #echo $counter
  mv $filename 'hw1-snaqTimeTests/log/timetest0'$counter'_snaq.log'
  let counter=counter+1
done

let counter=1

for filename in hw1-snaqTimeTests/out/timetest?_snaq.out
do
  #echo $filename
  #echo $counter
  mv $filename 'hw1-snaqTimeTests/out/timetest0'$counter'_snaq.out'
  let counter=counter+1
done
