import os
import numpy as np
import matplotlib.pyplot as plt
import math

expDir = 'c:/Hyperstim/Deliverable/GCaMP6s'

for dir in os.listdir(expDir):
    print(expDir + '/' + dir)
    F_path = expDir + '/' + dir + '/suite2p/plane0/F0.npy'
    stim_start_times_path = expDir + '/' + dir + '/stim_start_times.npy'
    stim_duration_path = expDir + '/' + dir + '/stimDurations.npy'
    block_frames_path =expDir + '/' + dir + '/frameNos.npy'
    roi_number_path = expDir + '/' + dir + '/suite2p/plane0/ROI_numbers.npy'

    F = np.load(F_path, allow_pickle = True)
    stim_start = np.load(stim_start_times_path,allow_pickle=True)
    block_frames = np.load(block_frames_path,allow_pickle=True)
    stim_duration = np.load(stim_duration_path, allow_pickle = True)
    roi_num = np.load(roi_number_path, allow_pickle = True)

    frame_rate = 31
    num_trials = 5
    start_timepoints = []
    for i in stim_start:
        start_timepoints.append(i)

    time_block = []
    for b in block_frames:
        time_block.append(b)
    stimulation_duration = []
    for s in stim_duration:
        stimulation_duration.append(s)

    num_blocks = len(time_block)

    resting_period = 2
    rest_dur_f = resting_period * frame_rate
    stim_dur_f = []
    end_f =[]

    for s in stimulation_duration:
        frameNo = math.floor(s*frame_rate)
        stim_dur_f.append(frameNo)
        end_f.append(frameNo + rest_dur_f)

    blocks_start = []
    for i in range(len(time_block)):
        prev_blocks_duration = sum(time_block[0:i])
        start_time = prev_blocks_duration
        end_time = start_time + time_block[i]-1
        blocks_start.append(start_time)

    start_stim_times = []
    trial_start_t = []
    trial_end_t = []
    trial_stim_end_t = []
    threshold_block = []
    rest_traces = []
    stim_traces = []
    avgs_stim = []
    avgs_rest = []
    exceed_thr = []
    stimResults = np.empty([len(F), num_blocks, num_trials],'int')
    restResults = np.empty([len(F), num_blocks, num_trials],'int')
    stimAvgs = np.empty([len(F), num_blocks, num_trials])
    restAvgs = np.empty([len(F), num_blocks, num_trials])
    baselineAvgs = np.empty([len(F), num_blocks])

    for iTrace in range(len(F)):
        stim_result_list =[]
        rest_result_list = []
        for iBlock  in range(num_blocks):
            baseline_dur = F[iTrace, blocks_start[iBlock]: blocks_start[iBlock] + (start_timepoints[iBlock]-1)]
            baseline_avg = np.mean(baseline_dur)
            baselineAvgs[iTrace,iBlock] = baseline_avg
            baseline_std = np.std(baseline_dur)
            threshold = baseline_std * 3 + baseline_avg

            avgs_stim_trial = []
            avgs_rest_trial = []
            for iTrial in range(num_trials):

                trial_start = blocks_start[iBlock] + (start_timepoints[iBlock] + iTrial * end_f[iBlock])
                trial_end = trial_start + stim_dur_f[iBlock]
                stim_trace = F[iTrace, trial_start:trial_end]
                avg_stim = np.mean(stim_trace)
                stimAvgs[iTrace][iBlock][iTrial] = avg_stim

                if avg_stim > threshold:
                    stim_above_thr = True
                else:
                    stim_above_thr = False

                stimResults[iTrace][iBlock][iTrial] = stim_above_thr

                rest_trace_start = blocks_start[iBlock] + (start_timepoints[iBlock] + ((iTrial+1) * (stim_dur_f[iBlock]) + (iTrial*rest_dur_f)))
                rest_trace_end = rest_trace_start + rest_dur_f
                rest_trace = F[iTrace, rest_trace_start:rest_trace_end]
                avg_rest = np.mean(rest_trace)
                restAvgs[iTrace][iBlock][iTrial] = avg_rest

                if avg_rest > threshold:
                    rest_above_thr = True

                else:
                    rest_above_thr = False
                restResults[iTrace, iBlock, iTrial] = rest_above_thr

    numRows = math.ceil(math.sqrt(len(F)))
    fig, axs = plt.subplots(numRows, numRows)

    full_trial_traces = np.zeros((len(F), num_blocks, num_trials,124), dtype=object)
    for iTrace in range(len(F)):
        for iBlock in range(num_blocks):
            for iTrial in range(num_trials):
                full_trial = np.concatenate((stim_trace, rest_trace))
                full_trial_traces[iTrace, iBlock, iTrial,0:len(full_trial)] = full_trial

    for i in range(numRows):
        for j in range(numRows):
            if i*numRows+j < len(F):
                axs[i][j].imshow(stimResults[i*numRows+j,:,:])
                axs[i][j].set_title('ROI' + str(roi_num[i*numRows+j]))
            else:
                print()
    #plt.show()

    #np.savez(expDir + '/' + dir + '/results.npz', stimResults=stimResults, restResults=restResults, stimAvgs=stimAvgs, restAvgs=restAvgs, baselineAvgs=baselineAvgs, full_trial_traces=full_trial_traces)

