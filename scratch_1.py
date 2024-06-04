import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# CHANGE THESE
distances = np.load('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_3-6_pos_amp/suite2p/plane0/distances.npy', allow_pickle=True)
F0 = np.load('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_3-6_pos_amp/suite2p/plane0/F0.npy', allow_pickle=True)
iscell = np.load('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_3-6_pos_amp/suite2p/plane0/iscell.npy', allow_pickle=True)

distanceValues = distances[:,2]
plt.hist(distanceValues, bins=30, color='skyblue', edgecolor='black')
#plt.plot(F0[48,:])
plt.show()