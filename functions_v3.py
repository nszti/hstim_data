import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import os
from pathlib import Path
import re
import ast


#stim_dur
def stim_dur_val(tiff_dir, list_of_file_nums):
    '''

    Parameters
    ----------
    tiff_dir: path to 'merged_tiffs' directory

    Returns:
    -------
    stimDurations.npy calculated from frequencies
    '''

    base_dir = Path(tiff_dir)
    filenames = [file.name for file in base_dir.iterdir() if file.name.startswith('merged')]
    #print(filenames)
    for numbers_to_merge in list_of_file_nums:
        suffix = '_'.join(map(str, numbers_to_merge))
        num_to_search = []
        for dir in filenames:
            num_to_search_split = dir.split('MUnit_')
            #print(num_to_search_split)
            if len(num_to_search_split) > 1:
                file_suffix = num_to_search_split[1].rsplit('.', 1)[0]
                if file_suffix == suffix:
                    matched_file = dir
                    print(matched_file)
                    break
        else:
            continue

        if matched_file:
            dir_path = base_dir / matched_file
            frequency_path = dir_path / 'selected_freqs.npy'
            frequency = np.load(frequency_path, allow_pickle=True)
            print(frequency)
            if not os.path.exists(frequency_path):
                print(f"Frequency file not found")
                exit(1)
            else:
                print(f"Stimulation frequencies: {frequency}")
                stim_duration = []
                for freq in frequency:
                    ref_freq = 100
                    ref_dur = 1
                    stim_dur = ref_freq / (ref_dur * freq)  # float
                    stim_duration.append(stim_dur)
                print(stim_duration)
                print(f"Stimulation durations for {matched_file}: {stim_duration}")
                np.save(dir_path /'stimDurations.npy', stim_duration)

#electrodeROI
def electROI_val(tiff_dir,list_of_file_nums):
    '''
    Parameters
    ----------
    Returns:
    -------
    saves electrodeROI.npy (spec. elec roi num) from 'selected_elec_ROI.npy'
    '''
    base_dir = Path(tiff_dir)
    filenames = [file.name for file in base_dir.iterdir() if file.name.startswith('merged')]

    for numbers_to_merge in list_of_file_nums:
        suffix = '_'.join(map(str, numbers_to_merge))
        num_to_search = []
        for dir in filenames:
            num_to_search_split = dir.split('MUnit_')
            # print(num_to_search_split)
            if len(num_to_search_split) > 1:
                file_suffix = num_to_search_split[1].rsplit('.', 1)[0]
                if file_suffix == suffix:
                    matched_file = dir
                    print(matched_file)
                    break
        else:
            continue

        if matched_file:
            dir_path = base_dir / matched_file
            print(dir_path)
            elec_roi_path = dir_path / 'selected_elec_ROI.npy'
            print(elec_roi_path)
            selected_elec_ROI = np.load(elec_roi_path, allow_pickle=True)
            if not os.path.exists(elec_roi_path):
                print(f" File not found")
                exit(1)
            else:
                print(f"ROIs of used electrodes: {selected_elec_ROI}")
                electrodeROI = []
                for roi in selected_elec_ROI:
                    electrodeROI.append(roi)
                print(f"Used electrode ROI for {dir}: {electrodeROI}")
                np.save(dir_path / 'electrodeROI.npy', electrodeROI)

#distance
def dist_vals (tiff_dir, list_of_file_nums):
    '''

    Parameters
    ----------
    tiff_dir
    list_of_file_nums

    Returns
    -------
    'roi_num' contains the roi number of detected cells--> gets saved into 'ROI_numbers.npy'
    euclidean distance from electrode roi--> 'distances.npy'

    '''
    #new_elec_med_value = (None, None)
    base_dir = Path(tiff_dir)

    filenames = [file.name for file in base_dir.iterdir() if file.name.startswith('merged')]

    for numbers_to_merge in list_of_file_nums:
        suffix = '_'.join(map(str, numbers_to_merge))
        num_to_search = []
        for dir in filenames:
            num_to_search_split = dir.split('MUnit_')
            # print(num_to_search_split)
            if len(num_to_search_split) > 1:
                file_suffix = num_to_search_split[1].rsplit('.', 1)[0]
                if file_suffix == suffix:
                    matched_file = dir
                    print(matched_file)
                    break
        else:
            continue

        if matched_file:
            iscell_path = tiff_dir  + matched_file + '/suite2p/plane0/iscell.npy'
            stat_path = tiff_dir  + matched_file + '/suite2p/plane0/stat.npy'
            electrodeROI_path = tiff_dir + matched_file + '/selected_elec_ROI.npy'
            csv_file_path = tiff_dir + matched_file + '/elec_roi_info.csv'
            print(csv_file_path)
            stat = np.load(stat_path, allow_pickle=True)
            iscell = np.load(iscell_path, allow_pickle=True)
            electrodeROI = np.load(electrodeROI_path, allow_pickle=True)
            print(electrodeROI)
            distances = []
            # extract cell roi info
            first_column = iscell[:, 0]
            tempforcells = []
            for index, value in enumerate(first_column):
                if value == 1:
                    roi_info = f"{index}, Value: {value}"
                    tempforcells.append([roi_info.split(',')[0]])

            # extract all roi med info
            med_values = [roi['med'] for roi in stat]
            tempforallmed = []
            tempforallroi = []
            for roi_number, med_value in enumerate(med_values):
                tempforallroi.append(roi_number)
                tempforallmed.append(med_value)

            # dataframes for cells & all roi
            dfcell_roi = pd.DataFrame(tempforcells, columns=['roi_num'])
            mergedallmedinfo = list(zip(tempforallroi, tempforallmed))
            dfallmedinfo = pd.DataFrame(mergedallmedinfo, columns=['roi_num', 'med'])

            # matching
            matched_roi_med = []
            for roi_num in tempforcells:
                roi_num = int(roi_num[0])  # extracting roi nums from tempforcells
                if roi_num in tempforallroi:
                    med_value = dfallmedinfo.loc[dfallmedinfo['roi_num'] == roi_num, 'med'].values
                    if len(med_value) > 0:
                        matched_roi_med.append((roi_num, med_value[0]))
            # df for matched info
            dfmatched = pd.DataFrame(matched_roi_med, columns=['roi_num', 'med_value'])



            # Distance calc w dfmatched-------------------------------------------
            def euclidean_distance(point1, point2):
                return np.linalg.norm(np.array(point1) - np.array(point2))

            # fv minimum distance search
            def minimum_distance_search(med_values, start_roi):
                start_point = None  # spec starting point(ha kell)
                for roi, coords in zip(roi_numbers, med_values):
                    print(med_values)
                    if roi == electrodeROI.any():
                        start_point = coords
                        break

                if start_point is None:
                    raise ValueError(f"ROI {start_roi} not found in the dataset.")
                distances = [euclidean_distance(start_point, coords) for coords in med_values]
                return distances


            roi_numbers = dfmatched['roi_num'] #df 0tol szamol!!
            med_values = dfmatched['med_value']
            distances = minimum_distance_search(med_values, electrodeROI)
            # print(distances)
            # extracting electrode info
            #electrode_med = []
            if isinstance(electrodeROI, list) or isinstance(electrodeROI, np.ndarray):
                for roi in electrodeROI:
                    electrode_i = dfmatched[dfmatched['roi_num'] == roi].index

            else:
                electrode_i = dfmatched[dfmatched['roi_num'] == electrodeROI].index
            electrode_med = dfmatched.loc[electrode_i, 'med_value'].iloc[0]
            x_value, y_value = electrode_med
            '''
            if new_elec_med_value is not None:
                [x_value, y_value] = new_elec_med_value
                distances = minimum_distance_search(med_values, new_elec_med_value)
            
            def modify_elec_med(new_elec_med_value):
                x_value, y_value = new_elec_med_value
                if new_elec_med_value is None:
                    x_value,y_value = electrode_med
                    return x_value, y_value

            mod_elec_med = modify_elec_med(new_elec_med_value)
            '''
            # Distance calc w dfmatched-------------------------------------------

            # df for electrode med info
            electrode_df = pd.DataFrame({'electrode med x': [x_value], 'electrode med y': [y_value]})

            # Results
            result_df = pd.DataFrame({
                'ROI_Number': roi_numbers,
                'Med_Values': med_values,
                'distance': distances
            })

            # concatenate elec info & roi info
            finaldf = pd.concat([electrode_df, result_df], ignore_index=True)
            finaldf.to_csv(csv_file_path, index=False)

            print(f"Results saved to {csv_file_path}")
            # print(result_df)
            # print(result_df.shape)
            dir_path = os.path.join(base_dir, dir)
            np.save(dir_path + '/suite2p/plane0/distances.npy', result_df)
            np.save(dir_path + '/suite2p/plane0/ROI_numbers.npy', roi_numbers)
            print(
                f"distances.npy saved to {dir_path + '/suite2p/plane0/distances.npy'}, ROI_numbers.npy saved to {dir_path + '/suite2p/plane0/ROI_numbers.npy'}")
            # save output as .npy file
            # np.save(expDir + '/' + dir + '/suite2p/plane0/distances.npy', result_df)
            # np.save(expDir + '/' + dir + '/suite2p/plane0/distances.npy', distances)
            # np.save(expDir + '/' + dir + '/suite2p/plane0/ROI_numbers.npy', roi_numbers)

def baseline_val(root_directory,tiff_dir, list_of_file_nums ):
    '''
    :return: saves all_norm_traces, prints shape of all_norm_traces, output: F0.npy (baseline corrected fluorescence trace)
    '''
    base_dir = Path(tiff_dir)
    filenames = [file.name for file in base_dir.iterdir() if file.name.startswith('merged')]
    matching_tiff = []
    file_nums_to_search = list_of_file_nums[0]

    for file in os.listdir(root_directory):
        #print(file)
        if file.endswith('.tif') and 'MUnit_' in file:
            start_index = file.find('MUnit_') + len('MUnit_')
            end_index = file.rfind('.tif')

            if start_index != -1 and end_index != -1 and start_index < end_index:
                number_str = file[start_index:end_index]

                if number_str.isdigit():
                    file_number = int(number_str)
                    if file_number in file_nums_to_search:
                        matching_tiff.append(file)

    for numbers_to_merge in list_of_file_nums:
        suffix = '_'.join(map(str, numbers_to_merge))
        matched_dir = None
        num_to_search = []
        for dir in filenames:
            num_to_search_split = dir.split('MUnit_')
            # print(num_to_search_split)
            if len(num_to_search_split) > 1:
                file_suffix = num_to_search_split[1].rsplit('.', 1)[0]
                if file_suffix == suffix:
                    matched_dir = dir
                    #print(matched_dir)
                    break
        else:
            continue

        file_dir = Path(base_dir/matched_dir)
        baseline_durations = []
        for num_id in file_nums_to_search:
            stim_times_path = os.path.join(file_dir, f'stimTime_{num_id}.npy')
            if os.path.exists(stim_times_path):
                stim_times = np.load(stim_times_path, allow_pickle=True)
                if stim_times.size > 0:
                    baseline_duration = int(stim_times[0]) - 1
                    baseline_durations.append(baseline_duration)


        if matched_dir:

            F_path = tiff_dir + matched_dir + '/suite2p/plane0/F.npy'
            iscell_path = tiff_dir + matched_dir + '/suite2p/plane0/iscell.npy'
            stim_start_times_path = tiff_dir + matched_dir + '/stimTimes.npy'

            F = np.load(F_path, allow_pickle=True)
            iscell = np.load(iscell_path, allow_pickle=True)
            stim_start_times = np.load(stim_start_times_path, allow_pickle=True)
            #print(f"stim type: {type(stim_start_times)}")


            all_norm_traces = []
            cellcount = 0
            # Iterate through all rois
            for cell_index, (fluorescence_trace, (iscell_value, _)) in enumerate(zip(F, iscell)):
                # Check iscell==1
                if iscell_value == 1:
                    cellcount += 1
                    baseline_duration = baseline_durations[cell_index % len(baseline_durations)]
                    baseline_duration = int(stim_start_times[0]) - 1
                    if baseline_duration is not None:
                        baseline_value = np.mean(fluorescence_trace[:baseline_duration])
                        normalized_trace = (fluorescence_trace - baseline_value) / baseline_value
                        all_norm_traces.append(normalized_trace)
                        #plt.figure()
                        #plt.plot(normalized_trace)
                        #plt.show()
            # convert the list of baseline_diffs to a npy array
            all_norm_traces = np.array(all_norm_traces)
            #print(len(all_norm_traces))
            #save output as .npy file
            dir_path = os.path.join(base_dir, dir)
            np.save(dir_path + '/suite2p/plane0/F0.npy', all_norm_traces)
            print(f"F0.npy saved to {dir_path + '/suite2p/plane0/F0.npy'}")
            #print(all_norm_traces.shape)
            #print(all_norm_traces)

#activated_neurons
def activated_neurons_val(root_directory, tiff_dir, list_of_file_nums, threshold_value = 1):
    '''
    :param input_file_path: 'D:/2P/E/test/merged_GCaMP6f_23_09_25_3-6_pos_amp/'
    :param time_block: type: number, time block duration in frames, example: 1085
    :return: saves distance results as 'result_df', can print sum of roi_num-med_val distances, output: activated_neurons.npy
    '''
    base_dir = Path(tiff_dir)
    filenames = [file.name for file in base_dir.iterdir() if file.name.startswith('merged')]
    file_nums_to_search = list_of_file_nums[0]
    matching_tiff = []
    for file in os.listdir(root_directory):
    # print(file)
        if file.endswith('.tif') and 'MUnit_' in file:
            start_index = file.find('MUnit_') + len('MUnit_')
            end_index = file.rfind('.tif')
            if start_index != -1 and end_index != -1 and start_index < end_index:
                number_str = file[start_index:end_index]
                if number_str.isdigit():
                    file_number = int(number_str)
                    if file_number in file_nums_to_search:
                        matching_tiff.append(file)

    for numbers_to_merge in list_of_file_nums:
        suffix = '_'.join(map(str, numbers_to_merge))
        for dir in filenames:
            num_to_search_split = dir.split('MUnit_')
            # print(num_to_search_split)
            if len(num_to_search_split) > 1:
                file_suffix = num_to_search_split[1].rsplit('.', 1)[0]
                if file_suffix == suffix:
                    matched_dir = dir
                    print(matched_dir)
                    break
        else:
            continue

        file_dir = Path(base_dir / matched_dir)
        baseline_durations = []
        for num_id in file_nums_to_search:
            stim_times_path = os.path.join(file_dir, f'stimTime_{num_id}.npy')
            if os.path.exists(stim_times_path):
                stim_times = np.load(stim_times_path, allow_pickle=True)
                if stim_times.size > 0:
                    baseline_duration = int(stim_times[0]) - 1
                    baseline_durations.append(baseline_duration)
        if matched_dir:
            # Load the fluorescence traces and iscell array
            F0_path = tiff_dir + matched_dir + '/suite2p/plane0/F0.npy'
            iscell_path = tiff_dir + matched_dir + '/suite2p/plane0/iscell.npy'
            ROI_numbers_path = tiff_dir + matched_dir + '/suite2p/plane0/ROI_numbers.npy'
            stim_start_times_path = tiff_dir + matched_dir + '/stimTimes.npy'
            frame_numbers_path = tiff_dir + matched_dir + '/frameNum.npy'

            F0 = np.load(F0_path, allow_pickle=True)
            iscell = np.load(iscell_path, allow_pickle=True)
            ROI_numbers = np.load(ROI_numbers_path, allow_pickle=True)
            #print(ROI_numbers)
            stim_start_times = np.load(stim_start_times_path, allow_pickle=True)
            #print(stim_start_times)
            frame_numbers = np.load(frame_numbers_path, allow_pickle=True)
            #print(frame_numbers)


            time_block = 1
            if len(frame_numbers) > 0:
                time_block = int(frame_numbers[0]) #1085
                #print(time_block)
            # Calculate TIFF trigger start and end tuples
            num_tif_triggers = int(np.round(len(F0[0]) / time_block))
            #print(len(F0[0]) / time_block)
            #print(num_tif_triggers)

            tif_triggers = []
            for i in range(num_tif_triggers):
                start_time = i * time_block
                #print(start_time)
                end_time = start_time + time_block
                #print(end_time)
                tif_triggers.append((start_time, end_time))
                #print(tif_triggers)
            ROI_numbers=[]
            #store threshold values for each ROI and tuple
            threshold_list = []
            #store results for each ROI and tuple
            results_list = []
            # Iterate through all ROIs
            #print(len(F0))
            for i in range(len(F0)):
                print(i)
                roi_thresholds = []
                roi_results = []
                #for tif_trigger in tif_triggers:
                    #for b in range(len(baseline_durations)):
                for baseline_duration, (start_time, end_time) in zip(baseline_durations, tif_triggers):
                    #for baseline_duration in baseline_durations:
                    #print(baseline_duration)
                    #print(start_time, end_time)
                    baseline_dur = F0[i, start_time:start_time + baseline_duration]
                    baseline_avg = np.mean(baseline_dur)
                    baseline_std = np.std(baseline_dur)
                    threshold = baseline_std * threshold_value + baseline_avg
                    #print(threshold)
                    roi_thresholds.append(threshold)
                    #print(roi_thresholds)
                    # Check if fluorescence exceeds threshold for the current tuple
                    stim_avg = np.mean(F0[i, (start_time + baseline_duration):(start_time + baseline_duration + 465)])
                    #print((start_time + baseline_duration), (start_time + baseline_duration + 465))
                    #print(stim_avg, threshold)
                    if stim_avg > threshold:
                        exceed_threshold = 1
                    else:
                        exceed_threshold = 0
                        # Append result (1 or 0) to the list for the current ROI
                    roi_results.append(int(exceed_threshold))
                #print(roi_results)
                # Append threshold values and results for the current ROI to the overall lists
                threshold_list.append(roi_thresholds)
                results_list.append(roi_results)
                ROI_numbers.append(i)
            print(results_list)
            # Convert the lists of threshold values and results to NumPy arrays---???not used
            threshold_array = np.array(threshold_list)
            results_array = np.array(results_list)
            # print(len(ROI_numbers), len(results_list))
            result_df = pd.DataFrame({
                'ROI_number': ROI_numbers,
                'thresholds': threshold_list,
                'activated_neurons': results_list
            })
            pd.set_option('display.max_rows', None)


        '''
                catSum = []
                for j in range(3):
                    cat = []
                    for i in range(len(results_list)):
                        cat.append(results_list[i][j])
    
            print(f"Summary of activation results: {catSum}")
        '''
        dir_path = os.path.join(base_dir, dir)
        np.save(dir_path + '/suite2p/plane0/activated_neurons.npy', result_df)
        print(f"activated_neurons.npy saved to {dir_path + '/suite2p/plane0/activated_neurons.npy'}")
        #np.save(expDir + '/' + dir + '/suite2p/plane0/activated_neurons.npy', result_df)

#timecourse
def timecourse_vals(tiff_dir, list_of_file_nums, num_trials):
    '''
    :param expDir:
    :param frame_rate: 31Hz
    :param num_trials: 5
    :return: saves 'results.npz'
    '''
    base_dir = Path(tiff_dir)
    filenames = [file.name for file in base_dir.iterdir() if file.name.startswith('merged')]
    frame_rate = 31

    for numbers_to_merge in list_of_file_nums:
        suffix = '_'.join(map(str, numbers_to_merge))
        num_to_search = []
        for dir in filenames:
            num_to_search_split = dir.split('MUnit_')
            # print(num_to_search_split)
            if len(num_to_search_split) > 1:
                file_suffix = num_to_search_split[1].rsplit('.', 1)[0]
                if file_suffix == suffix:
                    matched_file = dir
                    #print(matched_file)
                    break
        else:
            continue

        if matched_file:

            F_path = tiff_dir + matched_file + '/suite2p/plane0/F0.npy'
            stim_start_times_path = tiff_dir + matched_file + '/stimTimes.npy'
            stim_duration_path = tiff_dir + matched_file + '/stimDurations.npy'
            block_frames_path = tiff_dir + matched_file + '/frameNum.npy'
            roi_number_path = tiff_dir + matched_file + '/suite2p/plane0/ROI_numbers.npy'
            # num_trials_path = tiff_dir + matched_file + '/num_trials.npy'

            F = np.load(F_path, allow_pickle=True)
            stim_start = np.load(stim_start_times_path, allow_pickle=True)
            block_frames = np.load(block_frames_path, allow_pickle=True)
            stim_duration = np.load(stim_duration_path, allow_pickle=True)
            roi_num = np.load(roi_number_path, allow_pickle=True)
            #num_trials = np.load(num_trials_path, allow_pickle=True)
            #stim_duration= [2.0, 1.0, 0.5, 1.0]
            stim_duration = [1.0, 1.0, 1.0, 1.0]
            #print(stim_duration)
            start_timepoints = []
            for i in stim_start:
                start_timepoints.append(i)
            #print(stim_duration)

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
            end_f = []

            for s in stimulation_duration:
                frameNo = math.floor(s * frame_rate)
                stim_dur_f.append(frameNo)
                end_f.append(frameNo + rest_dur_f)

            blocks_start = []
            for i in range(len(time_block)):
                #print(i)
                prev_blocks_duration = sum(time_block[0:i])
                start_time = prev_blocks_duration
                end_time = start_time + time_block[i] - 1
                blocks_start.append(start_time)
            #print(num_trials)
            stimResults = np.empty([len(F), num_blocks, num_trials], 'int')
            restResults = np.empty([len(F), num_blocks, num_trials], 'int')
            stimAvgs = np.empty([len(F), num_blocks, num_trials])
            restAvgs = np.empty([len(F), num_blocks, num_trials])
            baselineAvgs = np.empty([len(F), num_blocks])
            full_trial_traces = np.zeros((len(F), num_blocks, num_trials, 124), dtype=object)

            for iTrace in range(len(F)):
                stim_result_list = []
                rest_result_list = []
                for iBlock in range(num_blocks):
                    baseline_dur = F[iTrace, int(blocks_start[iBlock]): int(blocks_start[iBlock]) + (
                                int(start_timepoints[iBlock]) - 1)]
                    baseline_avg = np.mean(baseline_dur)
                    baselineAvgs[iTrace, iBlock] = baseline_avg
                    baseline_std = np.std(baseline_dur)
                    threshold = baseline_std * 3 + baseline_avg

                    avgs_stim_trial = []
                    avgs_rest_trial = []
                    for iTrial in range(num_trials):
                        trial_start = blocks_start[iBlock] + (
                                    int(start_timepoints[iBlock]) + iTrial * int(end_f[iBlock]))
                        trial_end = int(trial_start) + stim_dur_f[iBlock]
                        # print(f"trial start: {trial_start}, stimdur: {stim_dur_f[iBlock]}")
                        # print(f"itrace: {iTrace}, trial start: {trial_start}, trial_end: {trial_end}")
                        stim_trace_plot = F[iTrace, int(trial_start)-31:int(trial_end)]
                        stim_trace = F[iTrace, int(trial_start):int(trial_end)]
                        avg_stim = np.mean(stim_trace)
                        stimAvgs[iTrace][iBlock][iTrial] = avg_stim

                        if avg_stim > threshold:
                            stim_above_thr = True
                        else:
                            stim_above_thr = False

                        stimResults[iTrace][iBlock][iTrial] = stim_above_thr
                        #print(stim_above_thr)

                        rest_trace_start = blocks_start[iBlock] + (int(start_timepoints[iBlock]) + (
                                    (iTrial + 1) * (int(stim_dur_f[iBlock])) + (int(iTrial * rest_dur_f))))
                        rest_trace_end = int(rest_trace_start) + int(rest_dur_f)
                        rest_trace = F[iTrace, int(rest_trace_start):int(rest_trace_end)]
                        avg_rest = np.mean(rest_trace)
                        restAvgs[iTrace][iBlock][iTrial] = avg_rest

                        if avg_rest > threshold:
                            rest_above_thr = True

                        else:
                            rest_above_thr = False
                        restResults[iTrace, iBlock, iTrial] = rest_above_thr

                        full_trial = np.concatenate((stim_trace_plot, rest_trace))
                        full_trial_traces[iTrace, iBlock, iTrial, 0:len(full_trial)] = full_trial


            numRows = math.ceil(math.sqrt(len(F)))
            fig, axs = plt.subplots(numRows, numRows, squeeze=False)


            '''
            full_trial_traces = np.zeros((len(F), num_blocks, num_trials, 124), dtype=object)

            for iTrace in range(len(F)):
                for iBlock in range(num_blocks):
                    for iTrial in range(num_trials):
                        full_trial = np.concatenate((stim_trace, rest_trace))
                        full_trial_traces[iTrace, iBlock, iTrial, 0:len(full_trial)] = full_trial
            '''
            for i in range(numRows):
                #print(range(numRows))
                #print(i)
                for j in range(numRows):
                    #print(j)
                    if i * numRows + j < len(F):
                        axs[i][j].imshow(stimResults[i * numRows + j, :, :])
                        axs[i][j].set_title('ROI' + str(roi_num[i * numRows + j]))
                    else:
                        print()
            #plt.show()

            np.savez(tiff_dir + dir + '/results.npz', stimResults=stimResults, restResults=restResults,
                     stimAvgs=stimAvgs, restAvgs=restAvgs, baselineAvgs=baselineAvgs,full_trial_traces=full_trial_traces)
            print(f"results.npz saved to {tiff_dir + dir + '/' + 'results.npz'}")


#data_analysis
def data_analysis_values (stim_type, tiff_dir, list_of_file_nums):
    '''
    :param stim_type: 4 type: 'amp','freq','pulse_no','dur'
    :return:
    '''
    base_dir = Path(tiff_dir)
    filenames = [file.name for file in base_dir.iterdir() if file.name.startswith('merged')]

    for numbers_to_merge in list_of_file_nums:
        suffix = '_'.join(map(str, numbers_to_merge))
        num_to_search = []
        for dir in filenames:
            num_to_search_split = dir.split('MUnit_')
            # print(num_to_search_split)
            if len(num_to_search_split) > 1:
                file_suffix = num_to_search_split[1].rsplit('.', 1)[0]
                if file_suffix == suffix:
                    matched_file = dir
                    #print(matched_file)
                    break
        else:
            continue

        if matched_file:
            output_dir = tiff_dir + matched_file
            container = np.load(tiff_dir + matched_file + '/results.npz', allow_pickle=True)
            # print(container)
            distances = np.load(tiff_dir +  matched_file + '/suite2p/plane0/distances.npy', allow_pickle=True)
            # print(distances)
            ROI_IDs = np.load(tiff_dir + matched_file + '/suite2p/plane0/ROI_numbers.npy', allow_pickle=True)
            # print(ROI_IDs)
            electrode_ROI = np.load(tiff_dir +  matched_file + '/electrodeROI.npy', allow_pickle=True)

            distanceFromElectrode = distances[:, 2]
            # print(distanceFromElectrode)
            stimResults = container["stimResults"]
            restResults = container["restResults"]
            stimAvgs = container["stimAvgs"]
            restAvgs = container["restAvgs"]
            baselineAvgs = container["baselineAvgs"]
            baselineAvgs = container["baselineAvgs"]
            full_trial_traces = container["full_trial_traces"]
            #print(full_trial_traces.shape)

            # remove electrode ROI from data
            #print(ROI_IDs, electrode_ROI)
            #electrode_ROI_index = np.where(ROI_IDs == electrode_ROI)[0]
            for i in ROI_IDs:
                if i == electrode_ROI[0]:
                    electrode_ROI_index = i
            distanceFromElectrode = np.delete(distanceFromElectrode, electrode_ROI_index, axis=0)
            stimResults = np.delete(stimResults, electrode_ROI_index, axis=0)
            restResults = np.delete(restResults, electrode_ROI_index, axis=0)
            stimAvgs = np.delete(stimAvgs, electrode_ROI_index, axis=0)
            restAvgs = np.delete(restAvgs, electrode_ROI_index, axis=0)
            baselineAvgs = np.delete(baselineAvgs, electrode_ROI_index, axis=0)
            full_trial_traces = np.delete(full_trial_traces, electrode_ROI_index, axis=0)

            # collect ROI, block and trial numbers
            ROI_No = stimResults.shape[0]
            block_No = stimResults.shape[1]
            trial_No = stimResults.shape[2]

            if stim_type == 'amp':
                legend = ['10', '20', '30', '40']
            elif stim_type == 'freq':
                legend = ['50', '100', '200']
            elif stim_type == 'pulse_dur':
                legend = ['50', '100', '200', '400']
            else:
                legend = ['20', '50', '100', '200']
            trialLabels = ['1', '2', '3', '4', '5']

            # collect neurons activated during a block
            activatedNeurons = np.empty([ROI_No, block_No], 'int')
            for iROI in range(ROI_No):
                for iBlock in range(block_No):
                    sumTrials = sum(stimResults[iROI, iBlock, :])
                    if sumTrials > 0:
                        activatedNeurons[iROI][iBlock] = 1
                    else:
                        activatedNeurons[iROI][iBlock] = 0

            # compute the number and fraction of neurons activated (or silent) during a block
            activeNeuronsPerBlock = np.empty(block_No, 'int')
            silentNeuronsPerBlock = np.empty(block_No, 'int')
            activeNeuronsPerBlockFraction = np.empty(block_No)
            #print(activeNeuronsPerBlockFraction)
            silentNeuronsPerBlockFraction = np.empty(block_No)
            #print(silentNeuronsPerBlockFraction)

            for iBlock in range(block_No):
                activeNeuronsPerBlock[iBlock] = sum(activatedNeurons[:, iBlock])
                activeNeuronsPerBlockFraction[iBlock] = activeNeuronsPerBlock[iBlock] / ROI_No
                silentNeuronsPerBlock[iBlock] = stimResults.shape[0] - activeNeuronsPerBlock[iBlock]
                silentNeuronsPerBlockFraction[iBlock] = silentNeuronsPerBlock[iBlock] / ROI_No

            # plot the number and fraction of neurons activated (or silent) during a block
            fig, axs = plt.subplots(2, 2, figsize = (12,8))
            axs[0, 0].plot(legend, activeNeuronsPerBlock, marker="o")
            axs[0, 0].set_xlabel('Stimulation current(uA)')
            axs[0, 0].set_ylabel('Number of active neurons')

            axs[0, 1].plot(legend, activeNeuronsPerBlockFraction, marker="o")
            axs[0, 1].set_xlabel('Stimulation current(uA)')
            axs[0, 1].set_ylabel('Fraction of active neurons')


            # compute the number and fraction of neurons activated during trials of a block
            activeNeuronsPerBlockPerTrial = np.empty([trial_No, block_No], 'int')
            activeNeuronsPerBlockPerTrialFraction = np.empty([trial_No, block_No])

            for iBlock in range(block_No):
                for iTrial in range(trial_No):
                    activeNeuronsPerBlockPerTrial[iTrial][iBlock] = sum(stimResults[:, iBlock, iTrial])
                    activeNeuronsPerBlockPerTrialFraction[iTrial][iBlock] = sum(stimResults[:, iBlock, iTrial]) / ROI_No
            #print(activeNeuronsPerBlockPerTrial.shape)
            #print(activeNeuronsPerBlockPerTrialFraction.shape)

            # plot the number and fraction of neurons activated during trials of a block
            axs[1, 0].plot(trialLabels, activeNeuronsPerBlockPerTrial, marker="o")
            axs[1, 0].legend(legend)
            axs[1, 0].set_xlabel('Trial number')
            axs[1, 0].set_ylabel('Number of active neurons')

            axs[1, 1].plot(trialLabels, activeNeuronsPerBlockPerTrialFraction, marker="o")
            axs[1, 1].legend(legend)
            axs[1, 1].set_xlabel('Trial number')
            axs[1, 1].set_ylabel('Fraction of active neurons')
            # calculate and plot the mean amplitudes during stimulation trials and blocks
            avgCA = np.empty([block_No, trial_No])
            avgCAperTrial = np.empty([trial_No])
            avgCAperBlock = np.empty([block_No])
            for iBlock in range(block_No):
                for iTrial in range(trial_No):
                    avgCA[iBlock][iTrial] = np.mean(stimAvgs[:, iBlock, iTrial])
            avgCAperTrial = np.mean(avgCA, axis=0)
            avgCAperBlock = np.mean(avgCA, axis=1)
            plt.savefig(output_dir + '/09_17_amp_fig1.svg')


            fig2, axs = plt.subplots(2, 2, figsize = (12,8))
            axs[0, 0].plot(legend, avgCAperBlock, marker="o")
            axs[0, 0].set_ylabel('Mean dF/F0')
            axs[0, 0].set_xlabel('Stimulation amplitude (uA)')
            axs[0, 1].plot(trialLabels, avgCAperTrial, marker="o")
            axs[0, 1].set_ylabel('Mean dF/F0')
            axs[0, 1].set_xlabel('Trial number')
            axs[1, 0].set_ylabel('Mean dF/F0')
            axs[1, 0].set_xlabel('Trial number')
            axs[1, 1].set_ylabel('Mean dF/F0')
            axs[1, 1].set_xlabel('Trial number')

            # calculate and plot the mean amplitudes during stimulation trials of a block
            avgCAduringTrials = np.empty([block_No, trial_No])
            for iBlock in range(block_No):
                for iTrial in range(trial_No):
                    avgCAduringTrials[iBlock][iTrial] = np.mean(stimAvgs[:, iBlock, iTrial])

                axs[1, 0].plot(trialLabels, avgCAduringTrials[iBlock, :])
            axs[1, 0].legend(legend)

            # calculate and plot the mean amplitudes during rest periods of a block
            avgCAduringRest = np.empty([block_No, trial_No])
            for iBlock in range(block_No):
                for iTrial in range(trial_No):
                    avgCAduringRest[iBlock][iTrial] = np.mean(restAvgs[:, iBlock, iTrial])

                axs[1, 1].plot(trialLabels, avgCAduringRest[iBlock, :])
            axs[1, 1].legend(legend)
            plt.savefig(output_dir + '/09_17_amp_fig2.svg')

            # plot calcium traces during stimulation
            tracesPerBlock = np.empty([ROI_No, 124])
            avgTracePerBlock = np.empty([block_No, trial_No, 124])
            for iBlock in range(block_No):
                for iTrial in range(trial_No):
                    tracesPerBlock = full_trial_traces[:, iBlock, iTrial, :]
                    avgTracePerBlock[iBlock, iTrial, :] = np.mean(tracesPerBlock, axis=0)  #

            plot_dur = 3 * 31
            ymin = -0.01
            ymax = 0.35
            #plt.savefig(output_dir + '/09_18_amp_fig3.svg')

            fig3, axs = plt.subplots(2, 5, figsize = (12,8))
            for iBlock in range(block_No):
                for iTrial in range(trial_No):
                    axs[0, iBlock].plot(avgTracePerBlock[iBlock, iTrial, 0:plot_dur])
                    axs[0, iBlock].set_title(legend[iBlock])
                    axs[0, iBlock].set_ylim([ymin, ymax])
                    axs[0, iBlock].legend(trialLabels)
                    axs[1, iTrial].plot(avgTracePerBlock[iBlock, iTrial, 0:plot_dur])
                    axs[1, iTrial].set_title(trialLabels[iTrial])
                    axs[1, iTrial].set_ylim([ymin, ymax])
                    axs[1, iTrial].legend(legend)
            axs[0, 0].set_ylabel('Mean dF/F0')
            axs[1, 0].set_ylabel('Mean dF/F0')
            # distance calculation and plot
            binSize = 50
            maxDistance = 600
            bin_numbers = int(maxDistance / binSize)
            CAduringStim = [[[] for _ in range(bin_numbers)] for _ in range(stimResults.shape[1])]
            activatedNeuronsDuringStim = np.zeros([block_No, bin_numbers])

            for iROI in range(stimResults.shape[0]):
                for iBlock in range(stimResults.shape[1]):
                    binNo = math.floor((distanceFromElectrode[iROI] / maxDistance) / (1 / bin_numbers))
                    # if activatedNeurons[iROI][iBlock] == 1:
                    CAduringStim[iBlock][binNo].append(np.mean(stimAvgs[iROI, iBlock, :]))
                    #print(np.mean(stimAvgs[iROI, iBlock, :]))
                    if activatedNeurons[iROI][iBlock] == 1:
                        activatedNeuronsDuringStim[iBlock][binNo] += 1
                        # CAduringStim[iBlock][binNo].append(stimAvgs[iROI, iBlock, 0])


            distanceMeans = np.empty([stimResults.shape[1], bin_numbers])
            plt.savefig(output_dir + '/09_17_amp_fig3.svg')

            # plot distance vs. mean calcium activity and distance vs. activated neurons
            fig4, axs = plt.subplots(2, 2, figsize = (12,8))
            x_axis = ['0-50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350', '350-400', '400-450',
                      '450-500', '500-550', '550-600']
            #print(bin_numbers)
            for iBlock in range(stimResults.shape[1]):
                for iBin in range(bin_numbers):
                    distanceMeans[iBlock][iBin] = np.mean(CAduringStim[iBlock][iBin])
                    print()
                    #print(distanceMeans[iBlock][iBin])

                axs[0, 0].plot(x_axis, distanceMeans[iBlock, :])
                axs[1, 0].plot(x_axis, activatedNeuronsDuringStim[iBlock, :])
            axs[0, 0].legend(legend)
            axs[0, 0].set_ylabel('Mean dF/F0')
            axs[0, 0].set_xlabel('Distance from electrode (um)')
            axs[1, 0].legend(legend)
            axs[1, 0].set_ylabel('Activated neurons')
            axs[1, 0].set_xlabel('Distance from electrode (um)')


            # calculate and plot mean distance of activated neurons vs. blocks
            distancesPerBlock = [[] for _ in range(block_No)]
            for iROI in range(ROI_No):
                for iBlock in range(block_No):
                    if activatedNeurons[iROI][iBlock] == 1:
                        distancesPerBlock[iBlock].append(distanceFromElectrode[iROI])

            meanDistancesPerBlock = np.empty([block_No])
            #print(meanDistancesPerBlock.shape)
            for iBlock in range(block_No):
                meanDistancesPerBlock[iBlock] = np.mean(distancesPerBlock[iBlock], axis=0)
            axs[0, 1].plot(legend, meanDistancesPerBlock)
            axs[0, 1].set_ylabel('Mean distance of activated neurons (um)')
            axs[0, 1].set_xlabel('Stimulation amplitudes')
            plt.savefig(output_dir + '/09_17_amp_fig4.svg')


            #norm
            fig5, axs = plt.subplots(2, 2, figsize=(12, 8))
            x_axis = ['0-50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350', '350-400', '400-450',
                      '450-500', '500-550', '550-600']
            # print(bin_numbers)
            bin_areas = [(math.pi * ((i+1)*binSize)** 2-math.pi * (i*binSize)**2)for i in range(bin_numbers)] #pi(r^2_outer-r^2_inner), outer: (i+1)*binSize, inner: i*binSize

            for iBlock in range(stimResults.shape[1]):
                for iBin in range(bin_numbers):
                    distanceMeans[iBlock][iBin] = np.mean(CAduringStim[iBlock][iBin])/bin_areas[iBin]
                    print()
                    # print(distanceMeans[iBlock][iBin])
                    activatedNeuronsDuringStim[iBlock][iBin] /= bin_areas[iBin]

                axs[0, 0].plot(x_axis, distanceMeans[iBlock, :])
                axs[1, 0].plot(x_axis, activatedNeuronsDuringStim[iBlock, :])
            axs[0, 0].legend(legend)
            axs[0, 0].set_ylabel('Mean dF/F0')
            axs[0, 0].set_xlabel('Normalised distance from electrode (um)')
            axs[1, 0].legend(legend)
            axs[1, 0].set_ylabel('Activated neurons')
            axs[1, 0].set_xlabel('Normalised distance from electrode (um)')

            # calculate and plot mean distance of activated neurons vs. blocks
            distancesPerBlock = [[] for _ in range(block_No)]
            for iROI in range(ROI_No):
                for iBlock in range(block_No):
                    if activatedNeurons[iROI][iBlock] == 1:
                        distancesPerBlock[iBlock].append(distanceFromElectrode[iROI])

            meanDistancesPerBlock = np.empty([block_No])
            # print(meanDistancesPerBlock.shape)
            for iBlock in range(block_No):
                meanDistancesPerBlock[iBlock] = np.mean(distancesPerBlock[iBlock], axis=0)
            axs[0, 1].plot(legend, meanDistancesPerBlock)
            axs[0, 1].set_ylabel('Mean distance of activated neurons (um)')
            axs[0, 1].set_xlabel('Stimulation amplitudes')
            plt.savefig(output_dir + '/09_17_amp_fig5.svg')
            plt.show()
#scratch_1
def scratch_val(tiff_dir):
    '''
    :param expDir:
    :return:
    '''
    base_dir = Path(tiff_dir)
    filenames = [file.name for file in base_dir.iterdir() if file.name.startswith('merged')]
    for dir in os.listdir(filenames):
        distances = np.load(tiff_dir + '/' + dir + '/suite2p/plane0/distances.npy', allow_pickle=True)
        F0 = np.load(tiff_dir + '/' + dir + '/suite2p/plane0/F0.npy', allow_pickle=True)
        #iscell = np.load(expDir + '/' + dir + '/suite2p/plane0/iscell.npy', allow_pickle=True)

        distanceValues = distances[:,2]
        plt.hist(distanceValues, bins=30, color='skyblue', edgecolor='black')
        plt.plot(F0[48,:])
        plt.show()

