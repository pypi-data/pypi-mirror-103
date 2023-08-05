# -*- coding: utf-8 -*-
"""
Discription: Preferences Window
Author(s): M. Fränzl
Data: 19/06/11
"""

import os

import numpy as np

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from pyqtgraph import QtCore, QtGui

class HelpWidget(QDialog):
    
    def __init__(self):
        super().__init__(None,  QtCore.Qt.WindowCloseButtonHint)
        
        loadUi(os.path.splitext(os.path.relpath(__file__))[0] + '.ui', self)
        