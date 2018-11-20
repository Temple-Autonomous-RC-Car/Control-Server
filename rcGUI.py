import sys
import cv2
import PyQt5
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap

import testLog
import socket_man_test

#Car Gui opens when executed
class loadCarGui(QDialog):
    def __init__(self):
        super(loadCarGui,self).__init__()
        loadUi('rcGUI_design.ui',self)



        self.setWindowTitle('Neural Network R/C Car')
        self.scrollArea.setWidget(self.CarLogLabel)
        self.scrollArea.setVerticalScrollBar(self.sensorLog_verticalScrollBar)

        self.sendCMD.clicked.connect(self.socketTextTest)

        self.ConnectButton.clicked.connect(self.connectionButtonClicked)
        self.testLogButton.clicked.connect(self.testLogFeed)
        self.stopLogButton.clicked.connect(self.stopLogFeed)
        self.TestCamButton.clicked.connect(self.Start_WebCam)
        self.TurnOffCamButton.clicked.connect(self.Stop_WebCam)
        self.i = 0
        self.qTimer = QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(self.testLogFeed)
        self.temp = ""
        #self.qTimer.start()
    @pyqtSlot()


#------------------------------------------------------------------------------#
    def socketTextTest(self):
        line = self.cmd_line.toPlainText()
        socket_man_test.pullfromCLient(line)

#------------------------------------------------------------------------------#
#This function will take IP Address and connect to the PI
    def connectionButtonClicked(self):
        self.CarIPLabel.setText(self.IPlineEdit.text())
        ipVAl = self.IPlineEdit.text()
        if ipVAl == "":
            self.noIPwarning.setText("NO IP:PORT VALUE")


#------------------------------------------------------------------------------#
#This function will test output sensor log from testLog.py
    def testLogFeed(self):


        #self.CarLogLabel.setText(testLog.testPrint())
        self.qTimer.start()
        self.i += 1
        self.temp += testLog.testPrint() + " " + str(self.i) + "\n"
        self.CarLogLabel.setText(self.temp)

        #Find a way to keep calling the scrollbar.maximum()

        self.sensorLog_verticalScrollBar.setValue(scrollBar.maxValue())
        #while self.qTimer.stop() != 'true':
        #    self.sensorLog_verticalScrollBar.maximum();



    def stopLogFeed(self):
        self.qTimer.stop()


#------------------------------------------------------------------------------#
# test port: http://192.168.137.141:8081/
# Code to Test WebCam Functionality.
# This is to just figure out how live video will work on this client
    def Start_WebCam(self):
        #port on webcam
        #self.capture=cv2.VideoCapture(0)

        #Port on the Aaron's pi
        #self.capture=cv2.VideoCapture('http://192.168.137.141:8081/')

        #Function will return if IP:Port Value is empty
        if self.IPlineEdit.text() == "":
            self.noIPwarning.setText("NO IP:PORT VALUE")
            return

        #IP:Port from input
        self.capture=cv2.VideoCapture('http://' + self.IPlineEdit.text() + '/')

        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

        self.timer=PyQt5.QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        ret,self.image=self.capture.read()
        #self.image=cv2.flip(self.image,1)
        self.displayImage(self.image,1)

    def Stop_WebCam(self):
        self.timer.stop()
        self.LiveCamView.clear()
        self.capture.release()
        cv2.destroyAllWindows()

    def displayImage(self,img,window=1):
        qformat=PyQt5.QtGui.QImage.Format_Indexed8
        if len(img.shape)==3 : #[0]=rows , [1]=cols [2]=channels
            if img.shape[2]==4 :
                qformat=PyQt5.QtGui.QImage.Format_RGBA8888
            else:
                qformat=PyQt5.QtGui.QImage.Format_RGB888

        outImage=PyQt5.QtGui.QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        #BGR>>RGB
        outImage=outImage.rgbSwapped()

        if window==1:
            self.LiveCamView.setPixmap(QPixmap.fromImage(outImage))
            self.LiveCamView.setScaledContents(True)

#-----------------------Live Video Feed Code Ends Here-------------------------#


if __name__=='__main__':
    app=QApplication(sys.argv)
    window=loadCarGui()
    window.show()
    sys.exit(app.exec_())

"""
app=QApplication(sys.argv)
widget=loadCarGui()
widget.show()
sys.exit(app.exec_())
"""
