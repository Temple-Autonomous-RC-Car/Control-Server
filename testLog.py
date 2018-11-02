import threading

def testPrint():
    threading.Timer(1.0, testPrint).start()
    self.CarLogLabel.setText(self.text("Hello, World!"))

testPrint()
