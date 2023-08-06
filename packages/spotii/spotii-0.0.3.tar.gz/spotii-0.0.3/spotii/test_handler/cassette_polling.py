import sys
import subprocess
import threading
import time
from .i2c_lib import i2c_device
from .take_photo import takePhoto, TakePhotoProcedure
from datetime import datetime,timezone
from spotii.define import *

# from smbus import SMBus
# import sys
# sys.path.append('/home/pi/gxf/python/spotii')
# sys.path.append('/home/pi/gxf/python/spotii/test_chip_handler')
# import subprocess
# from mythread import MyThread
# import time
# import queue
# import threading
# from i2c_lib import i2c_device
# from take_photo import takePhoto
# from datetime import datetime,timezone
# from define import *

class CassettePolling(threading.Thread):
    def __init__(self, slotIndex, i2c, camera, qResult, qCom, deviceQue):
        threading.Thread.__init__(self)
        self.slotIndex = slotIndex
        self.i2c = i2c
        self.camera = camera
        self.qResult = qResult
        self.qCom = qCom
        self.deviceQue=deviceQue
        self.stopTakingPhoto = threading.Event()
        
        
        self.deviceStatus = DEVICE_STATE_ORIGINAL
        
        self.takePhotoProcedure = None
        
    def stopTakePhotoProcedure(self):
#        print(self.takePhotoProcedure)
        if self.takePhotoProcedure != None and self.takePhotoProcedure.is_alive():
            #print("stop take photo procedure")
            self.stopTakingPhoto.set()
            self.takePhotoProcedure.join()
            self.stopTakingPhoto.clear()
        
    def run(self):
        self.periodPoll()
        while True:
            cmd=self.deviceQue.get()
            if cmd == PHOTO_TAKING_STOP:
                #print("stop command")
                self.stopTakePhotoProcedure()
            self.deviceQue.task_done()
            
#        self.cameraTest(self.index, self.i2c, self.camera)

    def notify(self, item):
        if self.deviceStatus != item[1]:
            self.deviceStatus = item[1]
            if item[1] != DEVICE_STATE_CASSETTE_POLLED:
                self.qResult.put(item)

    def getQr(self):
        try:
            for i in range(5):                
                i2cInstant=i2c_device(self.i2c,I2C_PORT)
                status=i2cInstant.read_data(I2C_MEM_STATUS)|0x80 #There should be bug on daughter board I2c function. sometimes missed bit 7.
                
                if self.slotIndex == 0 and status!=DEVICE_STATE_CASSETTE_POLLED:
                    print(hex(status), time.strftime('%Y%m%d%H%M%S'))
                qrCode=None
                if(status == DEVICE_STATE_CASSETTE_VALID):
                    qr=i2cInstant.read_block_data(I2C_MEM_ID, 9)
                    qrCode=(''.join(chr(x) for x in qr))
                    if not qrCode.isalnum():
                        print(time.strftime('%Y%m%d%H%M%S'), "qrCode crashed", self.slotIndex,qrCode)
                        time.sleep(2)
                        continue
                    break;
                elif status & CASSETTE_STATUS_FLAG == 0:
                    print(time.strftime('%Y%m%d%H%M%S'), "Wrong flag, re-read.", self.slotIndex, hex(status))
                    time.sleep(2)
                    continue
                else:
                    #print("Cassette status:", self.index, hex(status))
                    break;
                    
            #if status != DEVICE_STATE_CASSETTE_POLLED and status in CASSETTE_STATUS:
            if status == DEVICE_STATE_CASSETTE_VALID:
                i2cInstant.write_cmd_arg(I2C_MEM_ACK, status)
                print("Write back ACK")
                
            return status,qrCode
        except Exception as err:
            print("CassettePollingException: ", err)
            return DEVICE_STATE_SUBSYS_EXCEPTION, None        

#     def getPicture_new(self, qr_code):
#         print("slot",self.slotIndex,qr_code)
#         self.notify([self.slotIndex, DEVICE_STATE_TAKING_PHOTO, '', 'Taking photo'])
#         photoFile=takePhoto(self.camera, qr_code+'_'+str(self.slotIndex))
#         if(photoFile !=None ):
#             self.qCom.put(photoFile)


    def deviceDeal(self):  # return [device_slotIndex, state, QRcode, message]
        if self.camera == INVALID_DEVICE_INDEX:
            self.notify([self.slotIndex, DEVICE_STATE_CAMERA_ERROR, '', 'Camera error'])
            return 
        if self.i2c == INVALID_DEVICE_INDEX:
            self.notify([self.slotIndex, DEVICE_STATE_I2C_ERROR, '', 'i2c error'])
            return
        status,qr_code =self.getQr();
        if(status == DEVICE_STATE_CASSETTE_POLLED):
            self.notify( [self.slotIndex, DEVICE_STATE_CASSETTE_POLLED, '', 'no change'])
            return
        elif(status == DEVICE_STATE_CASSETTE_VALID):
            self.notify([self.slotIndex, DEVICE_STATE_TAKING_PHOTO, '', 'Taking photo'])
            self.stopTakePhotoProcedure()
            self.takePhotoProcedure = TakePhotoProcedure(self.slotIndex, qr_code, self.camera, self.qCom, self.stopTakingPhoto)
            self.takePhotoProcedure.start()
        else:
            self.stopTakePhotoProcedure()
            self.notify([self.slotIndex, status, '','Cassette error'])
            
    def periodPoll(self):
        #if self.slotIndex == 0:
        #    print("Period poll", time.strftime('%Y%m%d%H%M%S'))
        self.deviceDeal()
        threading.Timer(DEVICE_POLLING_TIME, self.periodPoll).start()

            
        
    def cameraTest(self):
        photoFile=takePhoto(self.camera, "cameraTest"+'_'+str(self.slotIndex))


if __name__ == "__main__":

    qForGui=queue.Queue()
    qForCom=queue.Queue()

    polling_0= CassettePolling(0, 80, 0, qForGui, qForCom)
    polling_2= CassettePolling(1, 81, 2, qForGui, qForCom)
    polling_4= CassettePolling(2, 82, 4, qForGui, qForCom)
    polling_6= CassettePolling(3, 83, 6, qForGui, qForCom)
    polling_8= CassettePolling(4, 84, 8, qForGui, qForCom)
    polling_0.start()
    polling_2.start()
    polling_4.start()
    polling_6.start()
    polling_8.start()
    
        
