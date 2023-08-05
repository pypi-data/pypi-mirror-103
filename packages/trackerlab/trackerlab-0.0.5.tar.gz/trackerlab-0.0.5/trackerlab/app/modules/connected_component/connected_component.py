# -*- coding: utf-8 -*-
"""
Discription: Module for Connected-Component Labeling similar to the 
            "Particle Analysis.vi" in the LabVIEW Vision Development Module.
Author(s):   M. Fränzl
Data:        20/01/20
"""

import numpy as np

import skimage
import pandas as pd

import os
path = os.path.dirname(os.path.realpath(__file__)) + "/"

from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal


import pyqtgraph as pg

from ..utils import pgutils, helpwidget
from ..utils.settings import saveSettings, restoreSettings

from trackerlab.detectors import connected_components

class Module(QtWidgets.QWidget):

    updated = pyqtSignal()
        
    def __init__(self):
        super().__init__(None)
        
        loadUi(path + os.path.splitext(os.path.basename(__file__))[0] + '.ui', self)
        self.settingsFile = path + os.path.splitext(os.path.basename(__file__))[0] + '.ini'
        
        self.helpWidget = helpwidget.HelpWidget()
        self.helpButton.clicked.connect(self.helpWidget.show)
        self.helpWidget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)     
        self.helpWidget.textEdit.setText('\n'.join([line.strip() for line in connected_components.__doc__.split('\n')]))
        
        self.thresholdSpinBox.valueChanged.connect(self.updated.emit)  
        self.minAreaSpinBox.valueChanged.connect(self.updated.emit)  
        self.maxAreaSpinBox.valueChanged.connect(self.updated.emit)
        self.invertCheckBox.stateChanged.connect(self.updated.emit)
        self.maxFeaturesSpinBox.valueChanged.connect(self.updated.emit)
        self.showOverlayCheckBox.stateChanged.connect(self.updated.emit)

           
    def attach(self, plot):
        self.p = plot
        self.items = []
        restoreSettings(self.settingsFile, self.widget)
        
        
    def detach(self):
        for item in self.items:
            self.p.removeItem(item)
            del item
        saveSettings(self.settingsFile, self.widget)
        

    def findFeatures(self, frame, imageItem):
            
        threshold = self.thresholdSpinBox.value()
        min_area = self.minAreaSpinBox.value()
        max_area = self.maxAreaSpinBox.value()
        max_features = self.maxFeaturesSpinBox.value()
        invert = self.invertCheckBox.checkState()

        features, image_out = \
           connected_components(imageItem.image, 
                                threshold, 
                                min_area,
                                max_area, 
                                max_features, 
                                invert)
           
        features["frame"] = frame
        
        imageItem.setImage(image_out)
        
        # Overlay
        for item in self.items:
            self.p.removeItem(item)
            del item
        self.items = []
        if self.showOverlayCheckBox.checkState():
            for i, f in features.iterrows():
                x0 = f.x + 0.5
                y0 = f.y + 0.5
                self.items.append(pgutils.EllipseItem([x0, y0], f.minor_axis_length, f.major_axis_length, -np.degrees(f.orientation), color='r', width=2))
                self.p.addItem(self.items[-1])
                self.items.append(pgutils.LineItem([x0, y0], [x0 + 0.5*f.minor_axis_length*np.cos(f.orientation), y0 - 0.5*f.minor_axis_length*np.sin(f.orientation)], color='b', width=2))
                self.p.addItem(self.items[-1])
                self.items.append(pgutils.LineItem([x0, y0], [x0 + 0.5*f.major_axis_length*np.sin(f.orientation), y0 + 0.5*f.major_axis_length*np.cos(f.orientation)], color='b', width=2))
                self.p.addItem(self.items[-1])
            
        if features.size > 0:
            self.numberOfFeatures.setText(str(features.shape[0]))
        else:
            self.numberOfFeatures.setText('0')
        
        return features
