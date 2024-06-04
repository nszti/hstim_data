import os
import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt
# Load the fluorescence traces and iscell array
expDir = 'c:/Hyperstim/Deliverable/GCaMP6f/'

for dir in os.listdir(expDir):

    F_path = expDir + '/' + dir + '/suite2p/plane0/F.npy'
    iscell_path = expDir + '/' + dir + '/suite2p/plane0/iscell.npy'
    stim_start_times_path = expDir + '/' + dir + '/stim_start_times.npy'
    print(F_path)
    F = np.load(F_path, allow_pickle=True)
    iscell = np.load(iscell_path, allow_pickle=True)
    stim_start_times = np.load(stim_start_times_path, allow_pickle=True)

    # Define baseline duration
    baseline_duration = stim_start_times[0]-1  # Duration in milliseconds

    # create empty list to store normalized baseline_diffs
    all_norm_traces = []

    cellcount = 0

    # Iterate through all rois
    for cell_index, (fluorescence_trace, (iscell_value, _)) in enumerate(zip(F, iscell)):
        # Check iscell==1
        if iscell_value == 1:
            cellcount += 1
            baseline_value = np.mean(fluorescence_trace[:baseline_duration])
            normalized_trace = (fluorescence_trace - baseline_value) / baseline_value
            #plt.plot(normalized_differences)
            #plt.show()
            all_norm_traces.append(normalized_trace)

    # convert the list of baseline_diffs to a npy array
    all_norm_traces = np.array(all_norm_traces)

    #save output as .npy file
    np.save(expDir + '/' + dir + '/suite2p/plane0/F0.npy', all_norm_traces)
    print(all_norm_traces.shape)