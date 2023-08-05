# -*- coding: utf-8 -*-

"""
Discription: TrackLab of the Molecular Nanophotonics.
Author(s): M. Fränzl
Data: 18/09/18
"""

import sys, os
from PyQt5.QtWidgets import QApplication

sys.path.append('..')
from trackerlab import app

if __name__ == '__main__':
    a = QApplication(sys.argv)
    window = app.MainWindow()
    window.show()
    sys.exit(a.exec_())
    