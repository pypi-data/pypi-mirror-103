# -*- coding: utf-8 -*-
"""
Discription: TrackLab of the Molecular Nanophotonics Group
Author(s): M. Fränzl
Data: 19/04/21
"""

import numpy as np

import nptdms
import imageio

def read_tdms_video(file):
    """
    Read TDMS video file.
    
    Arguments:
        file (string): The path to the TDMS file.
    Returns:
        images (3D array): The image series data. \n
        metadata (pandas DataFrame): A pandas DataFrame with the metadata. 
    """
    
    tdms_file = nptdms.TdmsFile(file)
    p = tdms_file.properties 
    
    metadata = {}
    for name, value in tdms_file.properties.items():
 
        if value.isdigit(): # Check if values is an integer.
            metadata[name] = int(value)
        else:
            try:
                metadata[name] = float(value) # Check if value can be converted to float.
            except:
                metadata[name] = value # If not, value is a string.
                
    dimx = metadata['dimx']
    dimy = metadata['dimy']
    
    try:
        frames = metadata['dimz'] # Backward compatibility
    except:
        frames = metadata['frames'] 
    
    images = tdms_file['Image']['Image'].data
    return images.reshape(frames, dimx, dimy), metadata


def read_tiff_stack(file):
    """
    Read TIFF stack file.
    
    Arguments:
        file (string): The path to the TIFF file.
    Returns:
        images (3D array): The image series data. \n
        metadata (pandas DataFrame): A pandas DataFrame with the metadata. 
    """
    images = io.imread(file)
    frames = images.shape[0]
    dimy = images.shape[1]
    dimx = images.shape[2]
    metadata = {
        "dimx": dimx,
        "dimy": dimy,
        "frames": frames,
        }
    return images, metadata       

  
def read_mp4_video(file):
    """
    Read MP4 video file.
    
    Arguments:
        file (string): The path to the MP4 file.
    Returns:
        images (3D array): The image series data. \n
        metadata (pandas DataFrame): A pandas DataFrame with the metadata. 
    """
    
    video = imageio.get_reader(file)
    dimx = video.get_meta_data()['size'][0]
    dimy = video.get_meta_data()['size'][1]
    frames = video.count_frames()
    images = np.stack([video.get_data(i)[:,:,0] for i in range(frames)])
    metadata = {
        "dimx": dimx,
        "dimy": dimy,
        "frames": frames,
        }
    return images, metadata


def read_avi_video(file):
    """
    Read AVI video file.
    
    Arguments:
        file (string): The path to the AVI file.
    Returns:
        images (3D array): The image series data. \n
        metadata (pandas DataFrame): A pandas DataFrame with the metadata. 
    """
    video = imageio.get_reader(file)
    dimx = video.get_meta_data()['size'][0]
    dimy = video.get_meta_data()['size'][1]
    frames = video.count_frames()
    images = np.stack([video.get_data(i)[:,:,0] for i in range(frames)])
    metadata = {
        "dimx": dimx,
        "dimy": dimy,
        "frames": frames,
        }
    return images, metadata


def read_png_image(file):
    """
    Read PNG file.
    
    Arguments:
        file (string): The path to the PNG file.
    Returns:
        images (2D array): The image data. \n
        metadata (pandas DataFrame): A pandas DataFrame with the metadata. 
    """
    images = io.imread(file)
    dimx = images.shape[0]
    dimy = images.shape[1]
    images = images[:,:,0]
    images = images[np.newaxis,:,:]
    frames = 1
    metadata = {
        "dimx": dimx,
        "dimy": dimy,
        "frames": frames,
        }
    return images, metadata


def read_jpg_image(self, file):
    """
    Read JPG file.
    
    Arguments:
        file (string): The path to the JPG file.
    Returns:
        images (2D array): The image data. \n
        metadata (pandas DataFrame): A pandas DataFrame with the metadata. 
    """
    images = io.imread(file)
    dimx = images.shape[0]
    dimy = images.shape[1]
    images = images[:,:,0]
    images = images[np.newaxis,:,:]
    frames = 1
    metadata = {
        "dimx": dimx,
        "dimy": dimy,
        "frames": frames,
        }
    return images, metadata
