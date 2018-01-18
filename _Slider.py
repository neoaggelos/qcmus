# _Slider.py

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class _Slider(QSlider):
    
    def __init__(self, orientation):
        super().__init__(orientation)
        
        self.setTracking(True)
        self.setFocusPolicy(Qt.NoFocus)
    
    def mousePressEvent(self, event):
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width()))
        
    def mouseMoveEvent(self, event):
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width()))
    
