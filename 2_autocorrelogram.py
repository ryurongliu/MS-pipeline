
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import signal
import csv


"""Turns centroided MIDAS files into plots and .txt files sorted by abundance"""

data_folder = "2_centroided_data"
plots_folder = "3_autocorrelogram_plots"
sorted_folder = "4_autocorrelogram_sorted"

filenames = os.listdir(data_folder)
filenames = [name for name in filenames if name.endswith('.txt')]

#number of peaks for plot
npeaks = 100

#autocorrelation
def autocorrelogram(data):
	mz = data[:,0]
	intensity = data[:,1]

	intensity = intensity[mz<500]
	mz = mz[mz<500]

	threshold = 0
	mz = mz[intensity >= threshold]
	intensity = intensity[intensity >= threshold]

	near_integer = np.abs(mz-np.rint(mz))<0.1
	mz = mz[near_integer]
	intensity = intensity[near_integer]

	intensity = np.ones(intensity.shape)

	hist_step = 0.002
	n_bins = int(np.max(mz)/hist_step)+1
	hist = np.zeros(n_bins)
	for i in range(len(mz)):
	    hist[int(mz[i]/hist_step)] += intensity[i]

	# dmz_bins = 5000
	# autocorrelogram = np.zeros((dmz_bins, n_bins))
	# for i in range(dmz_bins):
	#     autocorrelogram[i,:] = hist * np.concatenate([hist[i:], np.zeros(i)])

	dmz_range = 200 #up to 200 amu
	dmz_bins = int(dmz_range/hist_step)
	print(f"using {dmz_bins} bins")
	autocorrelogram = np.zeros(dmz_bins)
	for i in range(dmz_bins):
	    autocorrelogram[i] = np.sum(hist * np.concatenate([hist[i:], np.zeros(i)]))

	result = np.zeros((dmz_bins-1,2))
	result[:,0] = np.arange(dmz_bins-1)*hist_step
	result[:,1] = autocorrelogram[1:]
	return result


#create plots folder
if not os.path.exists(f'{plots_folder}'):
    os.makedirs(f'{plots_folder}')

k = 1
for data_filename in filenames:
	print(f"{k}/{len(filenames)}:\t{data_filename}")
	data = np.genfromtxt(f"{data_folder}/{data_filename}")
	data = autocorrelogram(data)

	fig_filename = f"{plots_folder}/{data_filename.split('.')[0]}.png"
	txt_filename = f"{sorted_folder}/{data_filename.split('.')[0].replace('centroided_data', 'sorted_mass_abundances')}.txt"
    

	peaks = signal.find_peaks(data[:,1])[0]
	if len(peaks)>npeaks:
		h = sorted([data[i,1] for i in peaks])
		thresh = h[-npeaks]
		peaks = signal.find_peaks(data[:,1],height=thresh)[0]
        
    #sorting
	abundances_sorted = sorted(data[:, 1])
	indices = np.argsort(data[:,1])
	masses_sorted = np.take_along_axis(data[:,0], indices, 0)
	abundances_sorted = np.flip(abundances_sorted)
	masses_sorted = np.flip(masses_sorted)

	plt.clf()
	plt.plot(data[:,0],data[:,1],'-',linewidth=0.5)
	plt.yscale('log')
    
    #write to .txt file
	with open(txt_filename, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(["Abundance", "Mass"])
		for i in range(len(data[:, 1])):
			if masses_sorted[i] >= 2. and abundances_sorted[i] > 0.:  #filter out masses below 2 amu
				writer.writerow([str(abundances_sorted[i]) + '\t' + f"{masses_sorted[i]:.3f}"])
                       

	for i in peaks:
		plt.annotate(f"{data[i,0]:.3f}",(data[i,0],data[i,1]),fontsize=3,rotation=90,rotation_mode='anchor')

	# plt.xlabel(colnames[i])
	# plt.ylabel(colnames[j])
	plt.savefig(fig_filename,dpi=300)
	k+=1


