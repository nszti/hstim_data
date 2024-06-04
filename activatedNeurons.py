
#roi_thresholds list, roi_results--> thr values for each tuple, exceedence check results
#each roi: roi_thresholds list, roi_results list--> stores the threshold values for each tuple, stores the results of the exceedance check for each tuple.
#lists: appended to threshold_list and results_list--> which store the threshold values and results for all rois
#threshold_list and results_list--> converted & saved to npy

import os
import numpy as np
import pandas as pd

# Load the fluorescence traces and iscell array
F0 = np.load('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_3-6_pos_amp/suite2p/plane0/F0.npy', allow_pickle=True)
iscell = np.load('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_3-6_pos_amp/suite2p/plane0/iscell.npy', allow_pickle=True)
ROI_numbers = np.load('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_3-6_pos_amp/suite2p/plane0/ROI_numbers.npy', allow_pickle=True)

stim_start_times = np.load('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_3-6_pos_amp/stim_start_times.npy', allow_pickle=True)


output_dir = 'c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_3-6_pos_amp/'

# Define time block duration in frames
time_block = 1085

# Calculate TIFF trigger start and end tuples
num_tif_triggers = int(len(F0[0]) / time_block)
tif_triggers = []

for i in range(num_tif_triggers):
    start_time = i * time_block
    end_time = start_time + time_block
    tif_triggers.append((start_time, end_time))

# Define baseline duration
baseline_duration = stim_start_times[0] # Duration in milliseconds
baseline_durs=[]
# Create an empty list to store threshold values for each ROI and tuple
threshold_list = []
# Create an empty list to store results for each ROI and tuple
results_list = []
# Iterate through all ROIs
for i in range(len(F0)):
    roi_thresholds = []
    roi_results = []
    # Iterate through all TIFF triggers
    for tif_trigger in tif_triggers:
        # Extract start and end time stamps for the current tuple
        start_time, end_time = tif_trigger
        # Create lists to store threshold and results for the current ROI
        baseline_dur = F0[i,start_time:start_time + baseline_duration] #??is it right
        #print(baseline_dur)
        # Calculate average for baseline
        baseline_avg = np.mean(baseline_dur)
        #print(baseline_avg)
        # Calculate standard deviation for the baseline trace
        baseline_std = np.std(baseline_dur)
        # Calculate threshold for the current tuple
        threshold = baseline_std * 1 + baseline_avg
        # Append threshold to the list for the current ROI
        roi_thresholds.append(threshold)
        # Check if fluorescence exceeds threshold for the current tuple
        stim_avg = np.mean(F0[i,(start_time + baseline_duration):(start_time + baseline_duration + 465)])
        if stim_avg > threshold:
            exceed_threshold = 1
        else:
            exceed_threshold = 0
        # Append result (1 or 0) to the list for the current ROI
        roi_results.append(int(exceed_threshold))
    # Append threshold values and results for the current ROI to the overall lists
    threshold_list.append(roi_thresholds)
    results_list.append(roi_results)
    #print(threshold_list)
    #print(roi_results)

# Convert the lists of threshold values and results to NumPy arrays
threshold_array = np.array(threshold_list)
results_array = np.array(results_list)

result_df = pd.DataFrame({
    'ROI_number': ROI_numbers,
    #'thresholds': threshold_list,
    'activated_neurons': results_list
})
pd.set_option('display.max_rows', None)

catSum = []
for j in range(4):
    cat = []
    for i in range(len(results_list)):
        cat.append(results_list[i][j])
    catSum.append(sum(cat))


print(catSum)

#np.save(expDir + '/' + dir + '/suite2p/plane0/distances.npy', result_df)
