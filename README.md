# Automated Pipeline for MS Analysis 
Processing and analysis pipeline for mass spectrometry data. Specifically works with MIDAS files (example of format included), but can be tweaked to work with any format.   

# Method 

This pipeline 1) centroids the MS data; 2) plots mass vs. abundance and sorts by highest abundance; 3) picks the most prominent peaks; 4) makes Kendrick Mass plots of those most prominent peaks; and 5) compares the most prominent peaks to known compounds. 

# Documentation

[IN PROGRESS]   

SETUP:    
- download all .py files
- make a folder called '1_MIDAS_files'   
- put all MIDAS files into this folder   
  
## 1. Turn MIDAS files into Centroided Data
- run `1_MIDAS_to_centroided_data.py`  
This will create .txt files of centroided data, in a separate folder called '2_centroided_data'
     
## 2. Create autocorrelogram plots and .txt files, sorted by abundance
- run  `2_autocorrelogram.py`  
This will create autocorrelgram plots of mass vs. abundance from the centroided data, in a folder called '3_autocorrelogram_plots'. It will also create .txt files of the masses sorted by abundance, in a folder called '4_autocorrelogram_sorted'. 

## 3. Pick most prominent peaks
- [IN PROGRESS]    

## 4. Make Kendrick Mass plots of most prominent peaks
- [IN PROGRESS]

## 5. Compare peaks to known compounds
- [IN PROGRESS]




