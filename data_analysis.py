import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import math


#load files and data
file_path = 'c:/Hyperstim/Deliverable/GCaMP6f/merged_GCaMP6f_23_09_25_3-6_pos_amp/'
container = np.load(file_path + 'results.npz')
distances = np.load(file_path +  '/suite2p/plane0/distances.npy', allow_pickle=True)
ROI_IDs = np.load(file_path + '/suite2p/plane0/ROI_numbers.npy', allow_pickle=True)
electrode_ROI = np.load(file_path + '/electrodeROI.npy', allow_pickle=True)
distanceFromElectrode = distances[:,2]
stimResults = container["stimResults"]
restResults = container["restResults"]
stimAvgs = container["stimAvgs"]
restAvgs = container["restAvgs"]
baselineAvgs = container["baselineAvgs"]

#remove electrode ROI from data
electrode_ROI_index = np.where(ROI_IDs == electrode_ROI)[0]
distanceFromElectrode=np.delete(distanceFromElectrode, electrode_ROI_index, axis=0)
stimResults= np.delete(stimResults, electrode_ROI_index, axis=0)
restResults = np.delete(restResults, electrode_ROI_index, axis=0)
stimAvgs = np.delete(stimAvgs, electrode_ROI_index, axis=0)
restAvgs = np.delete(restAvgs, electrode_ROI_index, axis=0)
baselineAvgs = np.delete(baselineAvgs, electrode_ROI_index, axis=0)

#collect ROI, block and trial numbers
ROI_No = stimResults.shape[0]
block_No = stimResults.shape[1]
trial_No = stimResults.shape[2]
legend = ['10','20','30','40']

#collect neurons activated during a block
activatedNeurons = np.empty([ROI_No, block_No],'int')
for iROI in range(ROI_No):
    for iBlock in range(block_No):
        sumTrials = sum(stimResults[iROI, iBlock, :])
        if sumTrials > 0:
            activatedNeurons[iROI][iBlock] = 1
        else:
            activatedNeurons[iROI][iBlock] = 0


#compute the number and fraction of neurons activated (or silent) during a block
activeNeuronsPerBlock = np.empty(block_No,'int')
silentNeuronsPerBlock = np.empty(block_No,'int')
activeNeuronsPerBlockFraction = np.empty(block_No)
silentNeuronsPerBlockFraction = np.empty(block_No)

for iBlock in range(block_No):
    activeNeuronsPerBlock[iBlock] = sum(activatedNeurons[:,iBlock])
    activeNeuronsPerBlockFraction[iBlock] = activeNeuronsPerBlock[iBlock]/ ROI_No
    silentNeuronsPerBlock[iBlock] = stimResults.shape[0] - activeNeuronsPerBlock[iBlock]
    silentNeuronsPerBlockFraction[iBlock] = silentNeuronsPerBlock[iBlock] / ROI_No

#plot the number and fraction of neurons activated (or silent) during a block
barWidth = 5
#blockLabels2 = [x + barWidth for x in blockLabels]
f1 = plt.figure('Figure 1')
blockLabels = ['10', '20', '30', '40']
#plt.bar(blockLabels, activeNeuronsInBlock, width=barWidth)
plt.plot(blockLabels, activeNeuronsPerBlock, marker="o")
#plt.bar(blockLabels2, silentNeuronsInBlock, width=barWidth)
plt.title('Number of active neurons for different stimulation currents')
plt.xlabel('Stimulation current(uA)')
plt.ylabel('Number of active neurons ')
plt.savefig(file_path + '/active_per_block.svg')
plt.show()

blockLabels = ['10', '20', '30', '40']
f2 = plt.figure('Figure 2')
plt.plot(blockLabels, activeNeuronsPerBlockFraction, marker="o")
plt.xlabel('Stimulation current(uA)')
plt.ylabel('Fraction of active neurons')
#plt.savefig(file_path + '.svg')
plt.show()

#compute the number and fraction of neurons activated during trials of a block
activeNeuronsPerBlockPerTrial = np.empty([trial_No, block_No],'int')
activeNeuronsPerBlockPerTrialFraction = np.empty([trial_No, block_No])

for iBlock in range(block_No):
    for iTrial in range(trial_No):
        activeNeuronsPerBlockPerTrial[iTrial][iBlock] = sum(stimResults[:, iBlock, iTrial])
        activeNeuronsPerBlockPerTrialFraction[iTrial][iBlock] = sum(stimResults[:, iBlock, iTrial]) / ROI_No


#plot the number and fraction of neurons activated during trials of a block
f3 = plt.figure('Figure 3')
plt.plot(['1','2','3','4','5'], activeNeuronsPerBlockPerTrial, marker="o")
plt.legend([10, 20, 30, 40])
plt.show()

f4 = plt.figure('Figure 4')
plt.plot(['1','2','3','4','5'], activeNeuronsPerBlockPerTrialFraction, marker="o")
plt.legend([10, 20, 30, 40])
plt.show()


#calculate and plot the mean ampitudes during stimulation trials of a block
f5 = plt.figure('Figure 5')
x_axis = ['1', '2', '3', '4', '5']
avgCAduringTrials = np.empty([block_No, trial_No])
for iBlock in range(block_No):
    for iTrial in range(trial_No):
        avgCAduringTrials[iBlock][iTrial] = np.mean(stimAvgs[:, iBlock, iTrial])

    plt.plot(x_axis, avgCAduringTrials[iBlock,:], label=legend[iBlock],marker="o") #,linestyle = 'dashed'

plt.legend()
plt.show()


#fig, ax = plt.subplots()
#ax.imshow(avgCAduringTrials)
#plt.show()

f6 = plt.figure('Figure 6')
avgCAduringRest = np.empty([block_No, trial_No])
for iBlock in range(block_No):
    for iTrial in range(trial_No):
        avgCAduringRest[iBlock][iTrial] = np.mean(restAvgs[:, iBlock, iTrial])

    plt.plot(x_axis, avgCAduringRest[iBlock,:], label=legend[iBlock],marker="o")
plt.legend()
plt.show()


#distance calculation and plot
binSize = 50
maxDistance = 600
bin_numbers = int(maxDistance/binSize)
CAduringStim = [[[] for _ in range(bin_numbers)] for _ in range(stimResults.shape[1])]


#CAduringStim = np.empty([bins])
for iROI in range(stimResults.shape[0]):
    for iBlock in range(stimResults.shape[1]):
        binNo = math.floor((distanceFromElectrode[iROI]/maxDistance)/(1/bin_numbers))
        #if activatedNeurons[iROI][iBlock] == 1:
        CAduringStim[iBlock][binNo].append(np.mean(stimAvgs[iROI, iBlock, :]))
            #CAduringStim[iBlock][binNo].append(stimAvgs[iROI, iBlock, 0])


#for iBin in range(bin_numbers):
#    print(len(CAduringStim[3][iBin]))
distanceMeans = np.empty([stimResults.shape[1], bin_numbers])
f7 = plt.figure('Figure 7')


x_axis = ['0-50','50-100','100-150','150-200','200-250','250-300','300-350','350-400','400-450','450-500','500-550','550-600']
for iBlock in range(stimResults.shape[1]):
    for iBin in range(bin_numbers):
            distanceMeans[iBlock][iBin] = np.mean(CAduringStim[iBlock][iBin])

    plt.plot(x_axis,distanceMeans[iBlock, :], label=legend[iBlock],marker="o")
plt.legend()
plt.show()
