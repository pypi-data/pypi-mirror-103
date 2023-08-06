import threading
import time

#qForGui format: [device_index, state, QRcode, message]
class GuiThread (threading.Thread):
    def __init__(self, threadID, name, qForGui):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.qForGui=qForGui
        
    def run (self):
        super().run()
        while True:
            qItem=self.qForGui.get()
            if qItem[2]!='':
                print(qItem, time.strftime('%Y%m%d%H%M%S'))

            self.qForGui.task_done()
                        



