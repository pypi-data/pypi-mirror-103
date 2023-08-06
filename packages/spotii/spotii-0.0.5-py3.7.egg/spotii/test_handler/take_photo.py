import time
import cv2
import random
from shutil import copyfile
import threading
import sys
import threading
import ntpath
import os


#sys.path.append('/home/pi/gxf/python/spotii')
from spotii.define import *
#sys.path.append('/home/pi/gxf/python/spotii/test_handler')

from .calibration import crop_rotate


def camInstCreate(cameraIndex):
    try:
        device="/dev/video"+str(cameraIndex)
#        print(device)
        camInst=cv2.VideoCapture(device)
        camInst.set(cv2.CAP_PROP_FRAME_WIDTH,  MAX_CAMERA_RESOLUTION_WIDTH)
        camInst.set(cv2.CAP_PROP_FRAME_HEIGHT, MAX_CAMERA_RESOLUTION_HEIGHT)
        return camInst
    except Exception as camErr:
        print("Camera create exception:",camErr)
        return None;
    

camera_sem = threading.Semaphore()
def takePhoto(cameraIndex,qrCode,event):
    rtn = None
    for i in range(5):
        camera_sem.acquire()    
        try:
            cam=camInstCreate(cameraIndex)
            s, img=cam.read()
            if s:
                photo=qrCode+'_'+str(int(time.time())) + '_'+time.strftime('%Y%m%d%H%M%S')+'.jpg'
                
                #path = Path("/here/your/path/file.txt")
                #print ((os.getcwd()).parent.absolute())
                
                #print(os.getcwd())
                imageFile=os.getcwd()+'/'+IMG_PATH+photo
                if crop_rotate(img,imageFile):
                    cam.release()
                    camera_sem.release()
                    rtn=photo
                    break;
            else:
                print("Photo taking failed!",qrCode, time.strftime('%Y%m%d%H%M%S'))
        except cv2.error as cv2Error:
            print("takePhoto cv2 Error: ", cv2Error)
        except Exception as e:
            print("takePhoto Exception: ", e)
    
        if cam !=None:
            cam.release()
        camera_sem.release()            
        event.wait(2)
        if event.isSet():
            break;
    return rtn

class TakePhotoProcedure(threading.Thread):
    def __init__(self, slotIndex, qrCode, camera, qCom, stopTakingPhoto):
        threading.Thread.__init__(self)
        self.slotIndex=slotIndex
        self.qrCode=qrCode
        self.camera = camera
        self.qCom = qCom
       
        self.timerParaIndex = 0
        self.taskStop=False
        self.event=stopTakingPhoto

    def run(self):
        while True:
            begin=time.time()
            self.procedure(self.timerParaIndex)
            end=time.time()
                        
            if self.timerParaIndex < len(PHOTO_TAKING_GAPS):
                delay=PHOTO_TAKING_GAPS[self.timerParaIndex] - (end-begin)
                self.timerParaIndex += 1
                if delay > 0:
                    self.event.wait(delay)                
            else:
                self.timerParaIndex = 0
                break;
            
            if self.event.isSet():
                #print(time.strftime('%Y%m%d%H%M%S'), "got stop command")
                break;
            
    def procedure(self,photoIndex):        
        photoFile=takePhoto(self.camera, self.qrCode+'_'+str(self.slotIndex)+'_'+str(photoIndex), self.event)
        if(photoFile !=None ):
            print(photoFile)
            self.qCom.put(photoFile)
        
   
def takePhoto_test():
    cameraIndex = 6
    qrCode ='8888'
    stopTakingPhoto = threading.Event()
    stopTakingPhoto.set()
    print (takePhoto(cameraIndex,qrCode,stopTakingPhoto) )
    
def takePhotoProcedure_test():
    None
    
    
if __name__ == "__main__":
    takePhoto_test()
          
