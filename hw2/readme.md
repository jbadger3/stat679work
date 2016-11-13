## Homework 2 Readme
### Outline:
The python script merge_temp_and_energy_files.py merges data from solar heated water system and solar panel system csv files.
Basic operation of the script takes two command line arguments preceded by -files in order: temperature_file and energy_file.
Energy generation values in Wh are converted to KWh and collated by date with
the daily water temperature data.  All temperature data and collated energy values
are appended to a single file energy_and_temperature.csv.
### Assumptions:
* monthly files are .csv files with lines formatted as follows

###### temperature_file format:

"Plot Title: 10679014 jackson July29"  
"#","Date Time, GMT-05:00","K-Type, °F (LGR S/N:   10679014, SEN S/N: 10679014, LBL: water pipe)"  
1,07/29/16 10:26:34 AM,72.86  
2,07/29/16 11:26:34 AM,73.92  
...  

###### energy_file format
Date/Time,Energy Produced (Wh)  
2016-07-29 00:00:00 -0500,2956  
2016-07-30 00:00:00 -0500,9468  
...  
Total, the_total  

### script(s)
`merge_temp_endergy_data.py`  
*usage*  
- run under shell as follows:  
`./path/to/merge_temp_and_energy_files.py -files temp_file energy_file`
- use -files to specify files
- use --overwrite to overwrite existing output file.  Dangerous!
- use -h for help
- use --test to run module tests

*result*
- energy_and_temperature.csv file at current directory
- if --overwrite option is specified, if energy_and_temperature.csv exists, the contents are overwritten
