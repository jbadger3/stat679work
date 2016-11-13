#!/usr/bin/env python
import datetime, re, sys, os, argparse
"""This script merges data from a solar heated water system and solar panel system.
The script takes two commad line arguments(files) in order: temperature_file and energy_file.
Energy generation values in Wh are converted to KWh and collated by date with
the daily water temperature data.  All temperature data and collated energy values
are appended to a single file energy_and_temperature.csv.
Assumptions:
* montly files are csv files with lines formated as follows:

temperature_file format:
"Plot Title: 10679014 jackson July29"
"#","Date Time, GMT-05:00","K-Type, °F (LGR S/N: 10679014, SEN S/N: 10679014, LBL: water pipe)"
1,07/29/16 10:26:34 AM,72.86
2,07/29/16 11:26:34 AM,73.92
...

energy_file format:
Date/Time,Energy Produced (Wh)
2016-07-29 00:00:00 -0500,2956
2016-07-30 00:00:00 -0500,9468
...
"""

# use an Argument Parser object to handle script arguments
parser = argparse.ArgumentParser(description="Combine temperature and solar energy data from files.")
parser.add_argument('-files', metavar=('temp_file','energy_file'),nargs='*', help='Paths to temp and energy files. Must be two files [temp_file energy_file] in this order.')
parser.add_argument("--overwrite", action="store_true", help="Overwrite any existing file in output. Use with caution!")
parser.add_argument("--test", action="store_true", help="Tests the module and quits.")
args = parser.parse_args()
# test argument problems early:
if args.test and (args.files or args.overwrite):
    print("ignoring file or overwrite arguments")
if args.files:
    if len(args.files) != 2:
        raise Exception("Files for temperature and energy must be supplied")
    else:
        assert 'Temperature' in args.files[0], 'First agument must be the temp file. File given: %s.'% args.files[0]
        assert 'energy' in args.files[1], 'Second argument must be the energy file. File given: %s.'% args.files[1]
if not args.files and not args.test:
    raise Exception("Arguments to run script not provided. Use -h for help.")




def remove_all_new_line_characters(file_lines):
    r"""Remove all new line characters from passed file_lines and
    return a cleaned list of file lines.
    Assume:
     * file_lines is a list of lines
     * newline characters are not embeded within lines ex.
       ['this,\n,is,imbeded\n','this,is,not\n']
    Examples:

    >>> remove_all_new_line_characters(['line1\n'])
    ['line1']
    >>> remove_all_new_line_characters(['\nline1'])
    ['line1']
    >>> remove_all_new_line_characters(['\n','\nline1\n','line2'])
    ['line1', 'line2']
    """

    clean_lines = [] #store cleaned lines in a list

    for line in file_lines:
        clean_line = line.strip()
        if clean_line != '': #only add non-blank lines to the cleaned list
            clean_lines.append(clean_line)
    return clean_lines

def parse_energy_lines(energy_lines):
    r"""
    Take all lines as a list from the energy file. For each line separate the fields
    into a list.  Convert each times stamp into a datetime and add it to a list of eneryg_days.
    Take each energy value in watt hours, convert it to killowatt hours, and store it in a list
    of killowatt_hours. Return both lists for further processing.
    Assumptions:
    * all newline characters have been previously stripped.
    * The first line is the list of fields for the file and should be skipped.
    * The last line contains the total and should be skipped
    * The time stamp is the first field an of the format '%Y-%m-%d %H:%M:%S %z'
    * The energy is the second field and given in watt hours
    Examples:
    >>> parse_energy_lines(['','2016-11-13 10:30:00 -0500,1000',''])
    ([datetime.datetime(2016, 11, 13, 10, 30, tzinfo=datetime.timezone(datetime.timedelta(-1, 68400)))], [1.0])
    >>> parse_energy_lines(['','2016-11-13 10:30:00 -0500,100',''])
    ([datetime.datetime(2016, 11, 13, 10, 30, tzinfo=datetime.timezone(datetime.timedelta(-1, 68400)))], [0.1])
    >>> parse_energy_lines(['','2016-11-13 10:30:00 -0500,100','2016-11-16 10:30:00 -0500,1000',''])
    ([datetime.datetime(2016, 11, 13, 10, 30, tzinfo=datetime.timezone(datetime.timedelta(-1, 68400))), datetime.datetime(2016, 11, 16, 10, 30, tzinfo=datetime.timezone(datetime.timedelta(-1, 68400)))], [0.1, 1.0])
    """
    energy_days = []
    killowatt_hours = []
    for e_line_num in range(1 ,len(energy_lines)-1): #loop from second line to the end
        e_line = energy_lines[e_line_num]
        e_fields = e_line.split(',') #split the line on commas

        energy_datetime = datetime.datetime.strptime(e_fields[0], '%Y-%m-%d %H:%M:%S %z') # convert timestamp to datetime
        energy_days.append(energy_datetime)

        energy_kw = float(e_fields[1])/1000 #convert energy from wh to kwh
        killowatt_hours.append(energy_kw)
    return energy_days, killowatt_hours

def merge_temp_and_energy_files(args):
    files = args.files #files passed in execution as list

    #open the temp file, read the lines into a list, and strip out all new line and white space
    temperature_file = files[0] #the temp file. verified in args check above
    temperature_file = open(temperature_file, 'r')
    temperature_lines = temperature_file.readlines()
    temperature_lines = remove_all_new_line_characters(temperature_lines)

    #open the energy file, read the lines into a list, and strip out all new line and white space
    energy_file = files[1]
    energy_file = open(energy_file, 'r')
    energy_lines = energy_file.readlines()
    energy_lines = remove_all_new_line_characters(energy_lines)

    #parse the lines from the energy file and return two aligned lists containing
    #ernergy days, and KWh for each day
    energy_days, kilowatt_hours = parse_energy_lines(energy_lines)


    days_counter = 0 #counter to track the index to use from energy_days and kilowatt_hours
    current_energy_day = energy_days[days_counter] # get the first energy date
    first_temp_line = temperature_lines[2] # get the first temp line
    firt_temp_date = datetime.datetime.strptime(first_temp_line.split(',')[1],'%m/%d/%y %I:%M:%S %p') # convert to date

    #align starting date to use from energy_days with the temp file
    while current_energy_day.date() <= firt_temp_date.date():
        days_counter += 1
        assert days_counter - 1 <= len(energy_days),'Failed to align dates of files!'
        current_energy_day = energy_days[days_counter]

    #make fields for new output file. Contains all of temp + energy in KWh
    fields = re.findall(r'"([^"]*)"',temperature_lines[1],re.DOTALL)
    fields.append(',Energy Produced (KWh)')

    #check areg options if overwrite was specified.
    if args.overwrite:
        #overwrite new file and write fields list to file
        out_file = open('energy_and_temperature.csv', 'w')
        out_file.write(','.join(fields))
    else:
        need_first_line = not os.path.exists('energy_and_temperature.csv')
        out_file = open('energy_and_temperature.csv', 'a')
        if need_first_line: out_file.write(','.join(fields)) # write fields if file didn't previously exist

    #go through each temp line and add to file.  Add energy data to end of last line if starting new day
    for t_line_num in range(2, len(temperature_lines)): #line 2 is the first line of data
        t_line = temperature_lines[t_line_num] # get current line
        t_fields = t_line.split(',') # split temp fields
        temperature_day = datetime.datetime.strptime(t_fields[1], '%m/%d/%y %I:%M:%S %p')

        #the temp date should ALWAYS be before or equal to the energy date.  if this is not true stop execution
        assert temperature_day.date() <= current_energy_day.date(), "Date matching failed! Check that the dates for both files match up and are in order."

        if temperature_day.date() == current_energy_day.date(): #add energy data to end of previous line

            if days_counter < len(energy_days) -1: #prevent range out of bounds error
                out_file.write(str(kilowatt_hours[days_counter])) #write energy to end of last line
                #move to next energy day
                days_counter += 1
                current_energy_day = energy_days[days_counter]
        out_file.write('\n') #start the next line
        out_file.write(t_line + ',') #write the temp data to the new line
    out_file.close()

def run_tests():
    print('Running tests:')
    import doctest
    doctest.testmod(verbose=True)
    print('Testing finished.')

if __name__ == '__main__':
    if args.test:
        run_tests()
    else:
        merge_temp_and_energy_files(args)
