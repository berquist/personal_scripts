#!/usr/bin/python

# cubeconvert.py - converts .cube files from electrons per au
# to electrons per angstrom.
# Call with: python cubeconvert.py input-file [output-file-name]

import sys, re
file1 = open(sys.argv[1], 'r')

if len(sys.argv) >= 3:
    out_file_name = sys.argv[2]
else:
    out_file_name = sys.argv[1] + "_in_e_per_angstrom.cube"
    output_file = open(out_file_name, 'w')
    list_of_lines = file1.readlines()
    
    regexp1 = re.compile("^\s+([0-9.\-]+)E([0-9.\-]+)\s+([0-9.\-]+)E([0-9.\-]+)\s+([0-9.\-]+)E([0-9.\-]+)\s+")

    max = 0
    min = 0
    sum = 0
    number_of_values = 0
                        
    for line in list_of_lines:
        if regexp1.match(line):
            numbers = line.split()
            for number in numbers:
                output_file.write("  %0.5E" % (float(number)*6.725627) )
                output_file.write("\n")
        else:
            output_file.write(line)

output_file.close()
