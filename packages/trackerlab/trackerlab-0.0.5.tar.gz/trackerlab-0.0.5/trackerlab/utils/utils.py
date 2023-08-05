# -*- coding: utf-8 -*-
"""
Discription: TrackLab of the Molecular Nanophotonics Group
Author(s): M. Fränzl
Data: 19/04/21
"""

import numpy as np

import nptdms
import pandas as pd

def analyse_tdms(file):
    """
    Print properties and channels of a TDMS file.
    
    Arguments:
        file (string): The path to the TDMS file.
    Returns:
        None
    """
    # Print properties and channels of TDMS file
    tdms_file = nptdms.TdmsFile(file)
    print('Properties (Root):')
    for name, value in tdms_file.properties.items():
        print(2*' ' + "{0}: {1}".format(name, value))
    for group in tdms_file.groups():
        print('\'' + group.name + '\'')
        print(2*' ' + 'Properties (' + '\'' + group.name + '\'' ')')
        for name, value in group.properties.items():
            print(2*' ' + "{0}: {1}".format(name, value))
        for channel in group.channels():
            print(2*' ' + channel.name)

  
def read_csv_features(file):
    """
    Read CSV features file (\*_features.csv) generated from TrackerLab.
    
    Arguments:
        file (string): The path to the CSV file.
    Returns:
        features (pandas DataFrame): A pandas DataFrame with the detected features.\n
        metadata (pandas DataFrame): A pandas DataFrame with the metadata.\n
        protocol (string): A string containing the content of the protocol file. 
    """
    protocol = ""
    with open(file) as f:
        row_count = 0
        row = f.readline()
        while row.startswith('#'):
            protocol += row[1:] # Remove leading # and append to comments
            row = f.readline()
            row_count += 1
            
    metadata = pd.read_csv(file, skiprows=row_count, nrows=1, index_col=0).to_dict('records')[0]
    features = pd.read_csv(file, skiprows=row_count+2, index_col=0)
    return features, metadata, protocol

    
def read_hdf5_features(file):
    """
    Read HDF5 features file (\*_features.csv) generated from TrackerLab.
    
    Arguments:
        file (string): The path to the HDF5 file.
    Returns:
        features (pandas DataFrame): A pandas DataFrame with the detected features.\n
        metadata (pandas DataFrame): A pandas DataFrame with the metadata.\n
        protocol (string): A string containing the content of the protocol file. 
    """
    with pd.HDFStore(file) as store:
        features = store["features"]
        metadata = store["metadata"].to_dict("records")[0]
        protocol = ""
        try:
            for line in store["protocol"]:
                protocol += line + "\n"
        except:
            pass
        store.close()

    return features, metadata, protocol
    
    

