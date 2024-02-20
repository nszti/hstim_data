import os
import numpy as np
import matplotlib.pyplot as plt

# Load the fluorescence traces and iscell array
F = np.load('../suite2p_tiff5/suite2p/plane0/F.npy', allow_pickle=True)
iscell = np.load('../suite2p_tiff5/suite2p/plane0/iscell.npy', allow_pickle=True)

# Define baseline duration
baseline_duration = 310  # Duration in milliseconds

# Specify the output directory
output_dir = '../suite2p_tiff5/baselinesearch'

# create output dir
os.makedirs(output_dir, exist_ok=True)
#ell.
cellcount = 0
# Open a file to save the output
output_file = os.path.join(output_dir, 'roi_output.txt')
with open(output_file, 'w') as file:
    # iterate through all rois
    for cell_index, (fluorescence_trace, (iscell_value, _)) in enumerate(zip(F, iscell)):
        # check iscell==1
        if iscell_value == 1:
            cellcount += 1
            #calc avg. basleline value
            baseline_value = np.mean(fluorescence_trace[:baseline_duration])
            #calc diff within baseline duration
            baseline_diff = ((fluorescence_trace[:baseline_duration] - baseline_value) / baseline_value) * 100
            #calc norm diff
            normalized_differences = ((fluorescence_trace[baseline_duration:] - baseline_value) / baseline_value) * 100
            
            #timepoints
            time_points = np.arange(len(fluorescence_trace))
            normalized_time_points = np.arange(baseline_duration, len(fluorescence_trace))

            # plotting
            plt.figure(figsize=(10, 6))
            #plt.scatter(normalized_time_points, fluorescence_trace[baseline_duration:], color='red', label='Compared points from avg.baseline')
            #plt.scatter(baseline_duration, baseline_value, color='green') #, label='Avg. baseline value'
            #plt.hlines(baseline_value, xmin=0, xmax=baseline_duration, color='green', linestyle='-', linewidth=3, label='Avg. baseline value')
            plt.plot(np.arange(baseline_duration), baseline_diff, color='green', label='Normalized Differences from Baseline')
            plt.plot(np.arange(baseline_duration,len(fluorescence_trace)), normalized_differences, color='red', label='Normalized Differences')
            plt.xlabel('Time (ms)')
            plt.ylabel('Normalised differences in fluorescence from baseline(%)')
            plt.title('Fluorescent trace and normalised differences for ROI {}'.format(cell_index))
            plt.legend()
            plt.grid(True)
            
           
            # save plot as png
            plot_file = os.path.join(output_dir, 'roi_plot_{}.png'.format(cell_index))
            plt.savefig(plot_file)
            plt.close()  # closeing--> no display
           
            # save output txt file
            file.write("ROI: {}\n".format(cell_index))
            file.write("Baseline avg.(100%): {:.2f}\n".format(baseline_value))
            #baseline diff
            for i, difference in enumerate(baseline_diff):
                file.write("Time: {} ms, Normalised differences(within baseline duration): {:.2f}%\n".format(i, difference))
            file.write('\n')
            #diff
            for i, difference in enumerate(normalized_differences):
                file.write("Time: {} ms, Normalized differences: {:.2f}%\n".format((i + 1 + baseline_duration), difference))
            file.write('\n')
print(cellcount)
print("Output saved to '{}'".format(output_dir))

