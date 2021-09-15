import os
from csv import reader
from csv import writer
import glob
from pathlib import Path

#######converts MIDAS files to required .txt files for autocorrelogram.py

#######ASSUMED FORMAT OF MIDAS FILES ****change if necessary!*****:
#######directory = directory for MIDAS files
#######suffname = suffix on MIDAS files, 'MIDAS.csv'
#######num_hlines = number of header lines before numerical data starts, 9
#######breakline_char = first character used in breaklines, '*'

#****format constants 
directory = '1_MIDAS_files'
suffname = 'MIDAS.csv'
num_hlines = 9
breakline_char = '*'



###grab list of MIDAS files
MIDAS_files = glob.glob(directory + '/' + '*' + suffname)

#make 2_centroided_data directory if not already exists
parent = os.getcwd()
Path(parent + "/2_centroided_data").mkdir(parents=True, exist_ok=True)

#make new .txt filenames in CentroidedData directory
txt_files = []
for file in MIDAS_files:
    file = file.replace(directory, "/2_centroided_data")
    file = file.replace(suffname, "centroided_data.txt")
    txt_files.append(parent + file)
    
#get masses and abundances from files
all_masses = []
all_rel_abundances = []
for file in MIDAS_files:
    masses = []
    rel_abundances = []
    with open(file, 'r') as open_file:
        csv_reader = reader(open_file)
        for i in range(num_hlines + 1): #skip header lines
            next(csv_reader)
        for row in csv_reader:
            first = row[0]
            if(first.strip()[0] != breakline_char): #check for breaklines
                masses.append(row[1].strip())
                rel_abundances.append(row[2].strip())
    all_masses.append(masses)
    all_rel_abundances.append(rel_abundances)     

#write masses and abundances to text files
for data in zip(txt_files, all_masses, all_rel_abundances):
    txtfile = data[0]
    masses = data[1]
    rel_abundances = data[2]
    with open(txtfile, 'w') as open_file:
        csvwriter = writer(open_file)
        for i in range(len(masses)):
            csvwriter.writerow([str(masses[i]) + '\t' + str(rel_abundances[i])])
    