# -*- coding: utf-8 -*-
"""
Discription: TrackLab of the Molecular Nanophotonics Group
Author(s): M. Fränzl
Data: 19/04/21
"""

import os, sys
import numpy as np
import glob, fnmatch

path = os.path.dirname(os.path.realpath(__file__)) + "/"

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog
from PyQt5.uic import loadUi

import pyqtgraph as pg
#import pyqtgraph.exporters

################################################################################
#sys.path.append('..')
from trackerlab import readers
################################################################################

import importlib

moduleNames = []
for m in os.listdir(path + "modules"):
    if os.path.isdir(os.path.join(path + "modules", m)) and m != "utils" and m != "template" and m != "__pycache__":
       moduleNames.append(m)

moduleList = []
for moduleName in moduleNames:
    moduleList.append(importlib.import_module("trackerlab.app.modules." + moduleName + '.' + moduleName))
    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #path = os.path.dirname(os.path.realpath(__file__))

        self.ui = loadUi(path + "app.ui", self) 
        
        self.displayedIcon = QtGui.QIcon(QtGui.QPixmap(path + "resources/circle.png")) 

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 0.75)
        pg.setConfigOption('imageAxisOrder', 'row-major')
        
        graphicsLayout = pg.GraphicsLayoutWidget()
        self.layout.addWidget(graphicsLayout)
        
        self.p1 = graphicsLayout.addPlot(row=1, col=1)
        self.p1.showAxis('top')
        self.p1.showAxis('right')
        self.p1.getAxis('top').setStyle(showValues=False)
        self.p1.getAxis('right').setStyle(showValues=False)
        self.p1.getAxis('top').setHeight(10)
        self.p1.getAxis('right').setWidth(15)
        self.p1.setAspectLocked(True) 
        self.im1 = pg.ImageItem()
        self.p1.addItem(self.im1)
        self.p1.getViewBox().invertY(True)

        self.p2 = graphicsLayout.addPlot(row=1, col=2)
        self.p2.showAxis('top')
        self.p2.showAxis('right')
        self.p2.getAxis('top').setStyle(showValues=False)
        self.p2.getAxis('right').setStyle(showValues=False)
        self.p2.getAxis('top').setHeight(10)
        self.p2.getAxis('right').setWidth(15)
        self.p2.setAspectLocked(True)
        self.im2 = pg.ImageItem()
        
        self.p2.addItem(self.im2)
        self.p2.getViewBox().invertY(True)     

        
        ################################################################################
        # Menu Bar
        ################################################################################
        self.actionAbout.triggered.connect(self.aboutClicked)

        self.dir = '../test_data'
        self.selectedFilter = 0
        
        self.filterList = ['TDMS Video Files (*_video.tdms *_movie.tdms)', # *_movie.tdms is kept for backward compatibility 
                           'TIFF Files (*.tif)',
                           'MP4 Video (*.mp4)', 
                           'PNG Image (*.png)', 
                           'JPG Image (*.jpg *.jpeg)',
                           'AVI Video (*.avi)']
        
        ################################################################################
        # File Selection
        ################################################################################
        
        self.selectFilesButton.clicked.connect(self.selectFiles)
        #self.addFilesButton.clicked.connect(self.appendFiles)
        #self.removeFilesButton.clicked.connect(self.removeFiles)
        self.fileList = []
        #self.fileListWidget.itemDoubleClicked.connect(self.fileDoubleClicked)
 
        self.frameSlider.valueChanged.connect(self.frameSliderChanged)   
        self.frameSpinBox.valueChanged.connect(self.frameSpinBoxChanged)  
      

        ################################################################################
        # Colormaps
        ################################################################################
        self.colormaps = []
        self.colormapComboBox.clear()
        for file in glob.glob(path + 'colormaps/*.csv'):
            self.colormapComboBox.addItem(os.path.splitext(os.path.basename(file))[0])
            self.colormaps.append(np.loadtxt(file, delimiter=','))
               
        if not self.colormaps:
            self.colormapComboBox.addItem('Gray') # default
        else:
            self.colormapComboBox.setCurrentIndex(self.colormapComboBox.findText('Gray'))
            
        self.colormapComboBox.currentIndexChanged.connect(self.colormapComboBoxChanged) 
        
        ################################################################################
        # Scaling/Levels
        ################################################################################
        
        self.scalingComboBox.currentIndexChanged.connect(self.scalingComboBoxChanged) 
        self.levelMinSlider.valueChanged.connect(self.levelMinSliderChanged)   
        self.levelMinSpinBox.valueChanged.connect(self.levelMinSpinBoxChanged)  
        self.levelMaxSlider.valueChanged.connect(self.levelMaxSliderChanged)   
        self.levelMaxSpinBox.valueChanged.connect(self.levelMaxSpinBoxChanged)  
        
        ################################################################################
        # Setup the "Modules" panel
        ################################################################################
        self.modules = []
        for module in moduleList:
            self.modules.append(module.Module())
        
        for module, moduleName in zip(self.modules, moduleNames):
            displayedName = moduleName.replace("_", " ").title() # Replace "_" with " " + title case 
            self.modulesComboBox.addItem(displayedName)
            self.moduleLayout.addWidget(module.widget)
            module.widget.hide()
            
        self.moduleIndex = 0
        self.modules[self.moduleIndex].widget.show()
        self.modulesComboBox.currentIndexChanged.connect(self.moduleIndexChanged) 

        self.modules[self.moduleIndex].attach(self.p2)
        self.modules[self.moduleIndex].updated.connect(self.update)
    
    
    def update(self):
        
        self.image1 = self.images[self.frameSlider.value()]
        
        if self.scalingComboBox.currentIndex() == 0:
            self.im1.setImage(self.image1)
        else:
            self.im1.setImage(self.image1, levels=[self.levelMinSpinBox.value(), self.levelMaxSpinBox.value()])             
        
        # Filters, ROI, ... 
        self.image2 = self.image1
        
        #features = pd.DataFrame()
        if self.featureDetectionCheckBox.checkState():
            self.im2.setImage(self.image2)
            features = self.modules[self.moduleIndex].findFeatures(self.frameSlider.value(), self.im2)
        else:
            if self.scalingComboBox.currentIndex() == 0:
                self.im2.setImage(self.image2)
            else:
                self.im2.setImage(self.image2, levels=[self.cminSlider.value(), self.cmaxSlider.value()])
        
        #if self.batch:
        #    self.features = self.features.append(features)
            

    def frameSliderChanged(self, value):
        self.frameSpinBox.setValue(value)
        self.update()
        
    def frameSpinBoxChanged(self, value):
        self.frameSlider.setValue(value)
        

    def colormapComboBoxChanged(self, value):
        if self.colormaps:
            self.im1.setLookupTable(self.colormaps[value])
            if not self.featureDetectionCheckBox.checkState():
                self.im2.setLookupTable(self.colormaps[value])    
        
    def scalingComboBoxChanged(self, value):
        if self.scalingComboBox.isEnabled():
            if self.scalingComboBox.currentIndex() == 0:
                self.cminSlider.setValue(0)
                self.cmaxSlider.setValue(np.max(self.images))
                self.enableLevels(False)
            else:
                self.enableLevels(True)
            self.update()
            
            
    def levelMinSliderChanged(self, value):
        self.levelMinSpinBox.setValue(value)
        
    def levelMinSpinBoxChanged(self, value):
        self.levelMinSlider.setValue(value)
        self.im1.setLevels([self.levelMinSpinBox.value(), self.levelMaxSpinBox.value()])
        if not self.featureDetectionCheckBox.checkState():
            self.im2.setLevels([self.levelMinSpinBox.value(), self.levelMaxSpinBox.value()])
        
    def levelMaxSliderChanged(self, value):
        self.levelMaxSpinBox.setValue(value)
        
        
    def levelMaxSpinBoxChanged(self, value):
        self.levelMaxSlider.setValue(value)
        self.im1.setLevels([self.levelMinSpinBox.value(), self.levelMaxSpinBox.value()])
        if not self.featureDetectionCheckBox.checkState():
            self.im2.setLevels([self.levelMinSpinBox.value(), self.levelMaxSpinBox.value()])
            
            
    def selectFilesDialog(self):
        options = QtWidgets.QFileDialog.DontUseNativeDialog 
        self.files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Files...', self.dir, ';;'.join(self.filterList), self.filterList[self.selectedFilter], options=options) # 'All Files (*)'
        if self.files:
            extension = os.path.splitext(self.files[0])[1]
            #self.selectedFilter = self.filterList.index(extension)
            if extension == '.tdms':
                self.selectedFilter = 0
            if extension == '.tif':
                self.selectedFilter = 1
            if extension == '.mp4':
                self.selectedFilter = 2
            if extension == '.png':
                self.selectedFilter = 3
            if extension == '.jpg':
                self.selectedFilter = 4
            if extension == '.avi':
                self.selectedFilter = 5
                
    def selectFiles(self):
        
        self.selectFilesDialog()
        
        if self.files:  
            #if not self.fileList:
                #self.modules[self.moduleIndex].attach(self.p2)
                #self.p1.scene().sigMouseMoved.connect(self.mouseMoved)   
                #self.p2.getViewBox().scene().sigMouseMoved.connect(self.mouseMoved)
                
            self.fileList = []
            self.fileListWidget.clear()
            for file in self.files:
                if fnmatch.fnmatch(file,'*_movie.tdms') or fnmatch.fnmatch(file,'*_video.tdms') or fnmatch.fnmatch(file,'*.tif') or fnmatch.fnmatch(file,'*.mp4')  or fnmatch.fnmatch(file,'*.png') or fnmatch.fnmatch(file,'*.jpg') or fnmatch.fnmatch(file,'*.avi'):
                    self.fileList.append(file)
                    item = QtGui.QListWidgetItem(os.path.basename(file))
                    item.setToolTip(file)
                    self.fileListWidget.addItem(item) # self.fileListWidget.addItem(os.path.basename(file))  
                
            self.displayedItem = self.fileListWidget.item(0)
            self.displayedItem.setIcon(self.displayedIcon)
            self.displayedItemChanged(0)
            #self.frameSlider.setValue(0) # Here, self.update() is called
            #self.frameSlider.setMaximum(self.frames-1)
            
            self.setEnabled(True)

            #if self.colormaps:
            #    self.colormapComboBox.setEnabled(True)
            #self.scalingComboBox.setEnabled(True)
            
            self.enableLevels(False) 
                

 
    
    def displayedItemChanged(self, value):
            
        file = self.fileList[value]
        extension = os.path.splitext(file)[1]
        #self.statusBar.showMessage('Loading: ' + os.path.basename(file))
        if extension == '.tdms':
            self.images, self.metadata = readers.read_tdms_video(file)
        if extension == '.tif':
            self.images, self.metadata = readers.read_tiff_stack(file)
        if extension == '.mp4':
            self.images, self.metadata = readers.read_mp4_video(file)  
        if extension == '.png':
            self.images, self.metadata = readers.read_png_image(file)
        if extension == '.jpg':
            self.images, self.metadata = readers.read_jpg_image(file)
        if extension == '.avi':
            self.images, self.metadata = readers.read_avi_video(file)
        
        self.dimx = self.metadata['dimx']
        self.dimy = self.metadata['dimy']
        
        try:
            self.frames = self.metadata['dimz'] # Backward compatibility
        except:
            self.frames = self.metadata['frames'] 
        
        self.infoLabel.setText('Dimensions: ' + str(self.dimx) + ' x ' + str(self.dimy) + ' x ' + str(self.frames))
        
    
        levelMax = np.max(self.images) 
        self.levelMinSlider.setMaximum(levelMax)
        self.levelMinSpinBox.setMaximum(levelMax)
        self.levelMaxSlider.setMaximum(levelMax)
        self.levelMaxSpinBox.setMaximum(levelMax)
        
        if self.scalingComboBox.currentIndex() == 0: # "Full Dynamic"
            self.levelMinSlider.setValue(0)
            self.levelMaxSlider.setValue(levelMax)
        
        if self.frameSlider.value() == 0:
            self.update() 
        else:
            self.frameSlider.setValue(0) # Here, self.update() is called
        self.frameSlider.setMaximum(self.frames-1)
        self.frameSpinBox.setMaximum(self.frames-1)
        
        self.startFrameSpinBox.setMaximum(self.frames-1)
        self.startFrameSpinBox.setValue(0)
        self.endFrameSpinBox.setMaximum(self.frames-1)
        self.endFrameSpinBox.setValue(self.frames-1)
        
        self.p1.setRange(xRange=[0, self.dimx], yRange=[0, self.dimy]) 
        #self.scaleBar1.sizeChanged(self.dimx, self.dimy)
        
                     
        self.statusBar.showMessage('Ready')


    def moduleIndexChanged(self):
        self.modules[self.moduleIndex].detach()
        self.modules[self.moduleIndex].widget.hide()
        self.moduleIndex = self.modulesComboBox.currentIndex()
        self.modules[self.moduleIndex].widget.show()
        self.modules[self.moduleIndex].updated.connect(self.update)
        self.modules[self.moduleIndex].attach(self.p2)
        self.update()
        
    def setEnabled(self, state):
        self.fileListWidget.setEnabled(state)
        self.frameSlider.setEnabled(state)
        self.frameSpinBox.setEnabled(state)
        self.colormapComboBox.setEnabled(state)
        self.scalingComboBox.setEnabled(state)
        self.maskTypeComboBox.setEnabled(state)
        self.subtractMeanCheckBox.setEnabled(state)
        self.invertImageCheckBox.setEnabled(state)
        self.enableLevels(state) 
        self.batchButton.setEnabled(state)
        self.preprocessingFrame.setEnabled(state)
        self.exportImageButton.setEnabled(state)
        #if self.ffmpeg:
        #    self.exportFrame.setEnabled(state)
        #    self.exportVideoButton.setEnabled(state)
        if self.exportTypeComboBox.currentIndex() == 1:
            self.startFrameSpinBox.setEnabled(False)
            self.endFrameSpinBox.setEnabled(False)
        self.featureDetectionCheckBox.setEnabled(state)
        self.modulesComboBox.setEnabled(state)
        if self.featureDetectionCheckBox.checkState():
            self.moduleFrame.setEnabled(True)
        self.removeFilesButton.setEnabled(state)
        self.lineProfileButton.setEnabled(state)
        self.scaleBar1CheckBox.setEnabled(state)
        self.scaleBar1Button.setEnabled(state)
        self.scaleBar2CheckBox.setEnabled(state)
        self.scaleBar2Button.setEnabled(state)


    def enableLevels(self, state): 
       self.levelMinSlider.setEnabled(state)  
       self.levelMinSpinBox.setEnabled(state) 
       self.levelMaxSlider.setEnabled(state)  
       self.levelMaxSpinBox.setEnabled(state) 
       
       
    def aboutClicked(self):
       about = QtWidgets.QMessageBox()
       about.setWindowTitle("TrackerLab App")
       about.setTextFormat(QtCore.Qt.RichText)   
       about.setText("This is the Molecular Nanophotonics TrackerLab App. " +
                     "It is based on PyQt and the PyQtGraph libary." + 2*"<br>" +
                     "<a href='http://github.com/Molecular-Nanophotonics/TrackerLab'>http://github.com/molecular-nanophotonics/trackerlab</a>" + 2*"<br>" +
                     "M. Fränzl")
       about.exec()