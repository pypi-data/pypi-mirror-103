from PyQt5.QtWidgets import QFileDialog, QLabel
import numpy as np
import os
from .models import ImgData


class MainController():
    def __init__(self, widget):
        self.widget = widget
        self._create_connections()
        self.data = ImgData()

    
    def _create_connections(self):
        #buttons
        self.widget.pushButton.clicked.connect(self.loadData)

        #connect slider in windows to update
        self.widget.graphicsView.timeLine.sigPositionChanged.connect(self.updateTextWithSliders)
        self.widget.graphicsView_2.timeLine.sigPositionChanged.connect(self.updateTextWithSliders)
        self.widget.graphicsView_3.timeLine.sigPositionChanged.connect(self.updateTextWithSliders)
        self.widget.actionLoad_Test_Data.triggered.connect(self.loadFakeData)
        self.widget.spinBox.valueChanged.connect(self.paramValueChanged)


    #slots
    def loadData(self):
        filename = QFileDialog.getOpenFileName()
        self.data.loadData(filename[0])
        #rename the choose file dialog
        self.widget.lineEdit_4.setText(filename[0])
        self.plotData()
        self.widget.spinBox.setMaximum(self.data.number_of_params)

        #update what is slider value
        self.updateTextWithSliders()


    def loadFakeData(self):
        self.data.loadFakeData()
        self.plotData()
        self.updateTextWithSliders()

    def paramValueChanged(self):
        param_num = self.widget.spinBox.value()
        self.data.change_param_number(param_num-1)
        
        z_ind = self.widget.graphicsView.currentIndex
        y_ind = self.widget.graphicsView_2.currentIndex
        x_ind = self.widget.graphicsView_3.currentIndex

        self.plotData()

        self.widget.graphicsView.setCurrentIndex(z_ind)
        self.widget.graphicsView_2.setCurrentIndex(y_ind)
        self.widget.graphicsView_3.setCurrentIndex(x_ind)


        self.updateTextWithSliders()


    def plotData(self):
        posSlice, scaleSlice, imgSlice = self.data.get_slice_parallel()
        self.widget.graphicsView.setImage(imgSlice, pos=posSlice, scale=scaleSlice, autoRange=True, autoHistogramRange=True)

        posPerp, scalePerp, imgPerp = self.data.get_slice_perp()
        self.widget.graphicsView_2.setImage(imgPerp, pos=posPerp, scale=scalePerp, autoRange=True, autoHistogramRange=True)

        posPerp2, scalePerp2, imgPerp2 = self.data.get_slice_perp2()
        self.widget.graphicsView_3.setImage(imgPerp2, pos=posPerp2, scale=scalePerp2, autoRange=True, autoHistogramRange=True)

    def updateTextWithSliders(self):
        z_ind = self.widget.graphicsView.currentIndex
        y_ind = self.widget.graphicsView_2.currentIndex
        x_ind = self.widget.graphicsView_3.currentIndex

        self.widget.lineEdit.setText(f"z={self.data.z[z_ind]}")
        self.widget.lineEdit_3.setText(f"y={self.data.y[y_ind]}")
        self.widget.lineEdit_2.setText(f"x={self.data.x[x_ind]}")


class MainController2():
    def __init__(self, widget):
        self.widget = widget
        self._create_connections()
        self.data = ImgData()

    
    def _create_connections(self):
        #buttons
        self.widget.pushButton.clicked.connect(self.loadData)

        #connect slider in windows to update
        self.widget.graphicsView.sigTimeChanged.connect(self.updateTextWithSliders)
        self.widget.graphicsView_2.sigTimeChanged.connect(self.updateTextWithSliders)
        self.widget.graphicsView_3.sigTimeChanged.connect(self.updateTextWithSliders)
        self.widget.graphicsView_4.sigTimeChanged.connect(self.updateTextWithSliders)


    #slots
    def loadData(self):
        filename = QFileDialog.getOpenFileName()
        self.data.loadData(filename[0])
        #rename the choose file dialog
        self.widget.lineEdit_4.setText(filename[0])
        self.plotData()

        #update what is slider value
        self.updateTextWithSliders(0)


    def plotData(self):
        self.data.change_param_number(0)
        posSlice, scaleSlice, imgSlice = self.data.get_slice_parallel()
        self.widget.graphicsView.setImage(imgSlice, pos=posSlice, scale=scaleSlice, autoRange=True, autoHistogramRange=True)

        self.data.change_param_number(1)
        posSlice, scaleSlice, imgSlice = self.data.get_slice_parallel()
        self.widget.graphicsView_2.setImage(imgSlice, pos=posSlice, scale=scaleSlice, autoRange=True, autoHistogramRange=True)

        self.data.change_param_number(2)
        posSlice, scaleSlice, imgSlice = self.data.get_slice_parallel()
        self.widget.graphicsView_3.setImage(imgSlice, pos=posSlice, scale=scaleSlice, autoRange=True, autoHistogramRange=True)

        self.data.change_param_number(3)
        posSlice, scaleSlice, imgSlice = self.data.get_slice_parallel()
        self.widget.graphicsView_4.setImage(imgSlice, pos=posSlice, scale=scaleSlice, autoRange=True, autoHistogramRange=True)



    def updateTextWithSliders(self, ind):
        self.widget.graphicsView.setCurrentIndex(ind)
        self.widget.graphicsView_2.setCurrentIndex(ind)
        self.widget.graphicsView_3.setCurrentIndex(ind)
        self.widget.graphicsView_4.setCurrentIndex(ind)

        self.widget.lineEdit.setText(f"z={self.data.z[ind]}")
        self.widget.lineEdit_3.setText(f"z={self.data.z[ind]}")
        self.widget.lineEdit_2.setText(f"z={self.data.z[ind]}")
        self.widget.lineEdit_5.setText(f"z={self.data.z[ind]}")