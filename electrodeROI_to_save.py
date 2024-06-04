import os
import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt

electrodeROIs = [29, 45, 47, 49, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#save output as .npy file

electrodeROI = np.array(electrodeROIs[0])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_08_16_11-14_ampl/electrodeROI.npy', electrodeROI)
print(electrodeROI)

electrodeROI = np.array(electrodeROIs[1])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_08_16_19_20_6_22_dur/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[2])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_08_16_23_6_24_freq/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[3])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_08_16_26-29_pulseNo/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[4])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_08_16_4-7_pos_ampl/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[5])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_21-24_ampl/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[6])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_27-30_ampl/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[7])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_33-36_ampl/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[8])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_3-6_pos_amp/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[9])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_37-39_41_dur/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[10])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_42-44_freq/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[11])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_46-49_pulseNo/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[12])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_24_02_09_10-12_freq/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[13])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_24_02_09_1-4_ampl/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[14])
np.save('c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_24_02_09_6-9_dur/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[15])
np.save('c:/Hyperstim/Deliverable/GCaMP6s/merged_GCaMP6s_23_09_11_15-18_ampl/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[16])
np.save('c:/Hyperstim/Deliverable/GCaMP6s/merged_GCaMP6s_23_09_11_36-38_40_dur/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[17])
np.save('c:/Hyperstim/Deliverable/GCaMP6s/merged_GCaMP6s_23_09_11_45-48_pulseNo/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[18])
np.save('c:/Hyperstim/Deliverable/GCaMP6s/merged_GCaMP6s_23_09_11_41-43_freq/electrodeROI.npy', electrodeROI)

electrodeROI = np.array(electrodeROIs[19])
np.save('c:/Hyperstim/Deliverable/GCaMP6s/merged_GCaMP6s_23_09_11_8-11_pos_ampl/electrodeROI.npy', electrodeROI)
