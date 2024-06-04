import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ast
import os

expDir = 'c:/Hyperstim/Deliverable/GCaMP6s/'

for dir in os.listdir(expDir):

    iscell_path = expDir + '/' + dir + '/suite2p/plane0/iscell.npy'
    stat_path = expDir + '/' + dir + '/suite2p/plane0/stat.npy'
    electrodeROI_path = expDir + '/' + dir + '/electrodeROI.npy'

    stat = np.load(stat_path, allow_pickle=True)
    iscell = np.load(iscell_path, allow_pickle=True)
    electrodeROI = np.load(electrodeROI_path, allow_pickle=True)

    #extract cell roi info
    first_column = iscell[:, 0]
    tempforcells = []
    for index, value in enumerate(first_column):
        if value ==1:
            roi_info = f"{index}, Value: {value}"
            tempforcells.append([roi_info.split(',')[0]])


    #extract all roi med info
    med_values = [roi['med']for roi in stat]
    tempforallmed = []
    tempforallroi = []
    for roi_number, med_value in enumerate(med_values):
        tempforallroi.append(roi_number)
        tempforallmed.append(med_value)

    #dataframes for cells & all roi
    dfcell_roi = pd.DataFrame(tempforcells, columns = ['roi_num'])
    mergedallmedinfo = list(zip(tempforallroi, tempforallmed))
    dfallmedinfo = pd.DataFrame(mergedallmedinfo, columns=['roi_num', 'med'])

    #matching
    matched_roi_med = []
    for roi_num in tempforcells:
        roi_num = int(roi_num[0])  # extracting roi nums from tempforcells
        if roi_num in tempforallroi:
            med_value = dfallmedinfo.loc[dfallmedinfo['roi_num'] == roi_num, 'med'].values
            if len(med_value) > 0:
                matched_roi_med.append((roi_num, med_value[0]))
    #df for matched info
    dfmatched = pd.DataFrame(matched_roi_med, columns = ['roi_num', 'med_value'])

    # Distance calc w dfmatched-------------------------------------------
    def euclidean_distance(point1, point2):
        return np.linalg.norm(np.array(point1) - np.array(point2))
    # fv minimum distance search
    def minimum_distance_search(med_values, start_roi):
        start_point = None  #spec starting point(ha kell)
        for roi, coords in zip(roi_numbers, med_values):
            if roi == start_roi:
                start_point = coords
                break

        if start_point is None:
            raise ValueError(f"ROI {start_roi} not found in the dataset.")
        distances = [euclidean_distance(start_point, coords) for coords in med_values]
        return distances

    roi_numbers = dfmatched['roi_num']
    med_values =dfmatched['med_value']
    distances = minimum_distance_search(med_values, electrodeROI)
    # extracting electrode info
    electrode_i = dfmatched[dfmatched['roi_num'] == electrodeROI].index
    electrode_med= dfmatched.loc[electrode_i, 'med_value'].iloc[0]
    x_value,y_value = electrode_med
    #print(distances)

    # Distance calc w dfmatched-------------------------------------------

    #df for electrode med info
    electrode_df = pd.DataFrame({'electrode med x': [x_value], 'electrode med y': [y_value]})

    #Results
    result_df = pd.DataFrame({
        'ROI_Number': roi_numbers,
        'Med_Values': med_values,
        'distance': distances

    })

    print(result_df)

    # save output as .npy file
    np.save(expDir + '/' + dir + '/suite2p/plane0/distances.npy', result_df)
    np.save(expDir + '/' + dir + '/suite2p/plane0/ROI_numbers.npy', roi_numbers)


