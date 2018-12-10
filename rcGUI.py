import sys
import cv2
import PyQt5
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
#from win32api import GetSystemMetrics
import os
import queue
import subprocess
import ip

import testLog

#GLOBAL VARIABLES FOR MAP COORDINATES
#right_clicks = list()
startingX, startingY = -1,-1
endingX, endingY = -1,-1
PortIP = ip.PORTIP

#Car Gui opens when executed
class loadCarGui(QDialog):
    def __init__(self):
        super(loadCarGui,self).__init__()
        loadUi('rcGUI_design.ui',self)
        self.setWindowTitle('Neural Network R/C Car')


        self.scrollArea.setWidget(self.CarLogLabel)
        self.scrollArea.setVerticalScrollBar(self.sensorLog_verticalScrollBar)
        self.sensorLog_verticalScrollBar.setValue(self.sensorLog_verticalScrollBar.maximum());
        self.scrollArea.setWidget(self.CarLogLabel)

        self.err_scrollArea.setWidget(self.exception_line)
        self.err_scrollArea.setVerticalScrollBar(self.err_verticalScrollBar)
        self.err_verticalScrollBar.setValue(self.err_verticalScrollBar.maximum());
        self.err_scrollArea.setWidget(self.exception_line)

        self.sendCMD.clicked.connect(self.socketTextTest)
        self.MapUploadButton.clicked.connect(self.mapUpload)
        self.ConnectButton.clicked.connect(self.connectionButtonClicked)
        self.testLogButton.clicked.connect(self.testLogFeed)
        self.stopLogButton.clicked.connect(self.stopLogFeed)
        self.TestCamButton.clicked.connect(self.Start_WebCam)
        self.TurnOffCamButton.clicked.connect(self.Stop_WebCam)

        #start button: VideoCascade and LaneDetectWrapper
            #videocascade -> LaneDetectWrapper
        self.RunButton.clicked.connect(self.connectCascadeAndLaneDetect)
        self.StopButton.clicked.connect(self.connectCascadeAndLaneDetectStopped)

        self.pickX.clicked.connect(self.pickXcoordinate)
        self.pickY.clicked.connect(self.pickYcoordinate)
        self.sendToMapProcessingButton.clicked.connect(self.sendToMapProcessingCode)

        self.i = 0
        self.qTimer = QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(self.testLogFeed)
        self.temp = ""
        self.err = ""


        #self.qTimer.start()
    @pyqtSlot()
#------------------------------------------------------------------------------#

    def connectCascadeAndLaneDetect(self):
        #self.p = subprocess.Popen(['python', 'VideoCascade.py'])
        self.p = subprocess.Popen(['python3', 'VideoCascade.py'])
        #self.p = subprocess.Popen(['py','-3', 'VideoCascade.py'])

        #self.l = subprocess.Popen(['python', 'LaneDetectWrapper.py'])
        self.p = subprocess.Popen(['python3', 'LaneDetectWrapper.py'])
        #self.p = subprocess.Popen(['py','-3', 'VideoCascade.py'])



    def connectCascadeAndLaneDetectStopped(self):
        self.p.kill()
        self.l.kill()


#------------------------------------------------------------------------------#
    def errorCatch(self, s):
        self.err += s + "\n"
        self.exception_line.setText(self.err)
        self.err_verticalScrollBar.setValue(self.err_verticalScrollBar.maximum());



#------------------------------------------------------------------------------#
#This function will connected to the socket-man.py listener socket
    def socketTextTest(self):
        try:
            line = self.cmd_line.toPlainText()
            socket_man_test.pullfromCLient(line)
        except:
            self.errorCatch("Error in method socketTextTest")


#------------------------------------------------------------------------------#
#This function will take map file and send it to processing. Then show processed image
#   on MapProccesedImage
    def mapUpload(self):
        try:
            #import find_corners

            # Create widget
            #label = QLabel(self.MapProccesedImage)
            pixmap = QPixmap('roomwithoutmarkers.png')
            resized_pixmap = pixmap.scaled(574.67, 431)
            self.MapProccesedImage.setPixmap(resized_pixmap)
            #self.resize(pixmap.width(),pixmap.height())
            #self.MapProccesedImage.displayImage("finalWithNodes.png", 1)
        except:
            self.errorCatch("Error in method mapUpload")

    def pickXcoordinate(self):
        try:
            print("Picking Starting Coordinate...")
            #set mouse callback function for window
            #this function will be called whenever the mouse is right-clicked
            def mouse_callback(event, x, y, flags, params):
                try:
                    global startingX, startingY
                    #right-click event value is 2
                    if event == 2:

                        #store the coordinates of the right-click event in list
                        #right_clicks.append([x, y])

                        #this just verifies that the mouse data is being collected
                        #you probably want to remove this later
                        #print(right_clicks)
                        startingX,startingY = x,y
                        print(startingX,startingY)
                        self.Startcoord_textEdit.setText("X: " + str(startingX) + " Y: " + str(startingY))
                except:
                    self.errorCatch("Error in method mouse_callback for X")

            img = cv2.imread("roomwithoutmarkers.png",0)
            height = img.shape[0]
            width = img.shape[1]
            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('image', width, height)
            cv2.imshow('image', img)
            cv2.setMouseCallback('image', mouse_callback)
        except:
            self.errorCatch("Error in method pickXcoordinate")

    def pickYcoordinate(self):
        try:
            print("Picking Ending Coordinate...")
            #set mouse callback function for window
            #this function will be called whenever the mouse is right-clicked
            def mouse_callback(event, x, y, flags, params):
                try:
                    global endingX, endingY
                    #right-click event value is 2
                    if event == 2:

                        #store the coordinates of the right-click event in list
                        #right_clicks.append([x, y])

                        #this just verifies that the mouse data is being collected
                        #you probably want to remove this later
                        #print(right_clicks)
                        endingX,endingY = x,y
                        print(endingX,endingY)
                        self.Endcoord_textEdit.setText("X: " + str(endingX) + " Y: " + str(endingY))
                except:
                    errorCatch("Error in method mouse_caalback for Y")
            img = cv2.imread("roomwithoutmarkers.png",0)
            height = img.shape[0]
            width = img.shape[1]
            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('image', width, height)
            cv2.imshow('image', img)
            cv2.setMouseCallback('image', mouse_callback)
        except:
            self.errorCatch("Error in method pickYcoordinate")


    def sendToMapProcessingCode(self):
        try:
            os.system("python3" + " find_corners.py " + str(startingX) + " " + str(startingY) + " " + str(endingX) + " " + str(endingY))

            #q = queue.Queue()
            pixmap = QPixmap('finalWithNodes.png')
            resized_pixmap = pixmap.scaled(574.67, 431)
            self.MapProccesedImage.setPixmap(resized_pixmap)
        except:
            self.errorCatch("Error in method sendToMapProcessingCode")




#------------------------------------------------------------------------------#
#This function will take IP Address and connect to the PI
    def connectionButtonClicked(self):
        try:
            #WILL CONNECT TO SERVER
            import socket_man_test
            self.CarIPLabel.setText("10.42.0.230:8081")
            ipVAl = self.IPlineEdit.text()
            if ipVAl == "":
                self.noIPwarning.setText("NO IP:PORT VALUE")
        except:
            self.errorCatch("Error in method connectionButtonClicked")


#------------------------------------------------------------------------------#
#This function will test output sensor log from testLog.pyr
    def testLogFeed(self):
        try:

            #self.CarLogLabel.setText(testLog.testPrint())
            self.qTimer.start()

            self.i += 1
            #self.temp += testLog.testPrint() + " " + str(self.i) + "\n"
            self.temp += sys.stdout
            self.CarLogLabel.setText(self.temp)
            self.sensorLog_verticalScrollBar.setValue(self.sensorLog_verticalScrollBar.maximum());

            #Find a way to keep calling the scrollbar.maximum()

            #self.sensorLog_verticalScrollBar.setValue(scrollBar.maxValue())
            #while self.qTimer.stop() != 'true':
            #    self.sensorLog_verticalScrollBar.maximum();
        except:
            self.errorCatch("Error in method testLogFeed")


    def stopLogFeed(self):
        self.qTimer.stop()


#------------------------------------------------------------------------------#
# test port: http://192.168.137.141:8081/
# Code to Test WebCam Functionality.
# This is to just figure out how live video will work on this client
    def Start_WebCam(self):
        try:
            #port on webcam
            #self.capture=cv2.VideoCapture(0)

            #Port on the Aaron's pi
            #self.capture=cv2.VideoCapture('http://192.168.137.141:8081/')

            #Function will return if IP:Port Value is empty
            if self.IPlineEdit.text() == "":
                self.noIPwarning.setText("NO IP:PORT VALUE")
                return

            #IP:Port from input
            #self.capture=cv2.VideoCapture('http://' + self.IPlineEdit.text() + '/')
            self.capture=cv2.VideoCapture('http://' + PortIP + '/')

            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

            self.timer=PyQt5.QtCore.QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(5)
        except:
            self.errorCatch("Error in method Start_WebCam")

    def update_frame(self):
        ret,self.image=self.capture.read()
        #self.image=cv2.flip(self.image,1)
        self.displayImage(self.image,1)

    def Stop_WebCam(self):
        try:
            self.timer.stop()
            self.LiveCamView.clear()
            self.capture.release()
            cv2.destroyAllWindows()
        except:
            self.errorCatch("Error in method Stop_WebCam")

    def displayImage(self,img,window=1):
        try:
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
        except:
            self.errorCatch("Error in method displayImage")
#-----------------------Live Video Feed Code Ends Here-------------------------#

    def exitGUI(self):
        sys.exit()



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
