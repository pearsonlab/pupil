#!/usr/bin/python
#
# Tobii controller for PsychoPy
# author: Hiroyuki Sogo
#         Modified by Soyogu Matsushita
#         Modified further by Shariq Iqbal (2015)
# - Tobii SDK 3.0 is required
# - no guarantee
#
import os, sys

PSYCHOPYPATH = os.path.dirname(sys.executable)
if PSYCHOPYPATH[-5:] != 'MacOS': # If Windows (Linux not tested!)
    TOBIIPATH = os.path.join(PSYCHOPYPATH, 'tobii', 'Modules')
else: # If Mac (since install configuration is slightly different)
    PSYCHOPYPATH = os.path.dirname(PSYCHOPYPATH)
    TOBIIPATH = os.path.join(PSYCHOPYPATH, 'tobii', 'modules')
sys.path.append(TOBIIPATH)

#MODIFIED: tobii.sdk -> tobii.eye_tracking_io
from tobii.eye_tracking_io.basic import EyetrackerException


import datetime
import time

#MODIFIED: tobii.sdk -> tobii.eye_tracking_io
import tobii.eye_tracking_io.mainloop
import tobii.eye_tracking_io.browsing
import tobii.eye_tracking_io.eyetracker
import tobii.eye_tracking_io.time.clock
import tobii.eye_tracking_io.time.sync

from tobii.eye_tracking_io.types import Point2D, Blob

import psychopy.visual
import psychopy.event

import Image
import ImageDraw

class TobiiController:
    def __init__(self, testWin, experWin):
        self.eyetracker = None
        self.eyetrackers = {}
        self.testWin = testWin
        self.experWin = experWin
        self.gazeData = []
        self.eventData = []
        self.datafile = None
        
        tobii.eye_tracking_io.init()
        self.clock = tobii.eye_tracking_io.time.clock.Clock()
        self.mainloop_thread = tobii.eye_tracking_io.mainloop.MainloopThread()
        self.mainloop_thread.start()
        self.browser = tobii.eye_tracking_io.browsing.EyetrackerBrowser(self.mainloop_thread, self.on_eyetracker_browser_event)
        
    def waitForFindEyeTracker(self):
        while len(self.eyetrackers.keys())==0:
            time.sleep(0.01)
        
    def on_eyetracker_browser_event(self, event_type, event_name, eyetracker_info):
        # When a new eyetracker is found we add it to the treeview and to the 
        # internal list of eyetracker_info objects
        if event_type == tobii.eye_tracking_io.browsing.EyetrackerBrowser.FOUND:
            self.eyetrackers[eyetracker_info.product_id] = eyetracker_info
            return False
        
        # Otherwise we remove the tracker from the treeview and the eyetracker_info list...
        del self.eyetrackers[eyetracker_info.product_id]
        
        # ...and add it again if it is an update message
        if event_type == tobii.eye_tracking_io.browsing.EyetrackerBrowser.UPDATED:
            self.eyetrackers[eyetracker_info.product_id] = eyetracker_info
        return False
        
    def destroy(self):
        self.eyetracker = None
        self.browser.stop()
        self.browser = None
        self.mainloop_thread.stop()
        
    ############################################################################
    # activation methods
    ############################################################################
    def activate(self,eyetracker):
        eyetracker_info = self.eyetrackers[eyetracker]
        print "Connecting to:", eyetracker_info
        tobii.eye_tracking_io.eyetracker.Eyetracker.create_async(self.mainloop_thread,
                                                     eyetracker_info,
                                                     lambda error, eyetracker: self.on_eyetracker_created(error, eyetracker, eyetracker_info))
        
        while self.eyetracker==None:
            time.sleep(0.01)
        self.syncmanager = tobii.eye_tracking_io.time.sync.SyncManager(self.clock,eyetracker_info,self.mainloop_thread)
        
    def on_eyetracker_created(self, error, eyetracker, eyetracker_info):
        if error:
            print "  Connection to %s failed because of an exception: %s" % (eyetracker_info, error)
            if error == 0x20000402:
                print "The selected unit is too old, a unit which supports protocol version 1.0 is required.\n\n<b>Details:</b> <i>%s</i>" % error
            else:
                print "Could not connect to %s" % (eyetracker_info)
            return False
        
        self.eyetracker = eyetracker
        
    ############################################################################
    # calibration methods
    ############################################################################
    
    def doCalibration(self,calibrationPoints):
        if self.eyetracker is None:
            return
        
        self.points = calibrationPoints
        self.point_index = -1
        
        img = Image.new('RGB',self.experWin.size)
        draw = ImageDraw.Draw(img)
        
        self.calin = psychopy.visual.Circle(self.testWin,radius=2,fillColor=(0.0,0.0,0.0))
        self.calout = psychopy.visual.Circle(self.testWin,radius=64,lineColor=(0.0,1.0,0.0))
        self.calresult = psychopy.visual.SimpleImageStim(self.experWin,img)
        self.calresultmsg = psychopy.visual.TextStim(self.experWin,pos=(0,-self.experWin.size[1]/4))
        self.promptone = psychopy.visual.TextStim(self.experWin,pos=(0,-self.experWin.size[1]/4))
        self.promptone.setText('Press space bar when ready to calibrate.')
        self.prompttwo = psychopy.visual.TextStim(self.testWin,pos=(0,-self.testWin.size[1]/4))
        self.prompttwo.setText('Focus your eyes on the center of the circles that appear.')
        
        self.initcalibration_completed = False
        print "StartCalibration"
        self.eyetracker.StartCalibration(self.on_calib_start)
        while not self.initcalibration_completed:
            time.sleep(0.01)
        waitkey = True
        while waitkey:
            for key in psychopy.event.getKeys():
                if key=='space':
                   waitkey = False
            
            self.calout.draw()
            self.calin.draw()
            self.promptone.draw()
            self.prompttwo.draw()
            self.testWin.flip()
            self.experWin.flip()
        
        clock = psychopy.core.Clock()
        for self.point_index in range(len(self.points)):
            p = Point2D()
            p.x, p.y = self.points[self.point_index]
            self.calin.setPos(((p.x-0.5)*self.testWin.size[0],(0.5-p.y)*self.testWin.size[1]))
            self.calout.setPos(((p.x-0.5)*self.testWin.size[0],(0.5-p.y)*self.testWin.size[1]))
            
            clock.reset()
            currentTime = clock.getTime()
            while currentTime < 1.5:
                self.calout.setRadius(40*(1.5-(currentTime))+4)
                psychopy.event.getKeys()
                self.calout.draw()
                self.calin.draw()
                self.testWin.flip()
                currentTime = clock.getTime()
            self.add_point_completed = False
            self.eyetracker.AddCalibrationPoint(p, self.on_add_completed)
            while not self.add_point_completed:
                psychopy.event.getKeys()
                self.calout.draw()
                self.calin.draw()
                self.testWin.flip()
         
        self.computeCalibration_completed = False
        self.computeCalibration_succeeded = False
        self.eyetracker.ComputeCalibration(self.on_calib_compute)
        while not self.computeCalibration_completed:
            time.sleep(0.01)
        self.eyetracker.StopCalibration(None)
        
        self.testWin.flip()
        self.experWin.flip()
        
        self.getcalibration_completed = False
        self.calib = self.eyetracker.GetCalibration(self.on_calib_response)
        while not self.getcalibration_completed:
            time.sleep(0.01)
        
        draw.rectangle(((0,0),tuple(self.experWin.size)),fill=(128,128,128))
        if not self.computeCalibration_succeeded:
            #computeCalibration failed.
            self.calresultmsg.setText('Not enough data was collected (Retry:r/Abort:ESC)')
            
        elif self.calib == None:
            #no calibration data
            self.calresultmsg.setText('No calibration data (Retry:r/Abort:ESC)')
        else:
            points = {}
            for data in self.calib.plot_data:
                points[data.true_point] = {'left':data.left, 'right':data.right}
            
            if len(points) == 0:
                self.calresultmsg.setText('No true calibration data (Retry:r/Abort:ESC)')
            
            else:
                for p,d in points.iteritems():
                    # MODIFIED: validity -> status
                    if d['left'].status == 1:
                        draw.line(((p.x*self.experWin.size[0],p.y*self.experWin.size[1]),
                                   (d['left'].map_point.x*self.experWin.size[0],
                                    d['left'].map_point.y*self.experWin.size[1])),fill=(255,0,0))
                    # MODIFIED: validity -> status
                    if d['right'].status == 1:
                        draw.line(((p.x*self.experWin.size[0],p.y*self.experWin.size[1]),
                                   (d['right'].map_point.x*self.experWin.size[0],
                                    d['right'].map_point.y*self.experWin.size[1])),fill=(0,255,0))
                    draw.ellipse(((p.x*self.experWin.size[0]-10,p.y*self.experWin.size[1]-10),
                                  (p.x*self.experWin.size[0]+10,p.y*self.experWin.size[1]+10)),
                                 outline=(0,0,0))
                self.calresultmsg.setText('Accept calibration results (Accept:a/Retry:r/Abort:ESC)')
                
        self.calresult.setImage(img)
        
        waitkey = True
        while waitkey:
            for key in psychopy.event.getKeys():
                if key == 'a':
                    retval = 'accept'
                    waitkey = False
                elif key == 'r':
                    retval = 'retry'
                    waitkey = False
                elif key == 'escape':
                    retval = 'abort'
                    waitkey = False
            self.calresult.draw()
            self.calresultmsg.draw()
            self.experWin.flip()
        
        return retval
    
    def on_calib_start(self, error, r):
        if error:
            print "Could not start calibration because of error. (0x%0x)" % error
            return False
        self.initcalibration_completed = True
    
    def on_add_completed(self, error, r):
        if error:
            print "Add Calibration Point failed because of error. (0x%0x)" % error
            return False
        
        self.add_point_completed = True
        return False
    
    def on_calib_compute(self, error, r):
        if error == 0x20000502:
            print "CalibCompute failed because not enough data was collected:", error
            print "Not enough data was collected during calibration procedure."
            self.computeCalibration_succeeded = False
        elif error != 0:
            print "CalibCompute failed because of a server error:", error
            print "Could not compute calibration because of a server error.\n\n<b>Details:</b>\n<i>%s</i>" % (error)
            self.computeCalibration_succeeded = False
        else:
            print ""
            self.computeCalibration_succeeded = True
        
        self.computeCalibration_completed = True
        return False
    
    def on_calib_response(self, error, calib):
        if error:
            print "On_calib_response: Error =", error
            self.calib = None
            self.getcalibration_completed = True
            return False
        
        print "On_calib_response: Success"
        self.calib = calib
        self.getcalibration_completed = True
        return False    
    
    def on_calib_done(self, status, msg):
        # When the calibration procedure is done we update the calibration plot
        if not status:
            print msg
            
        self.calibration = None
        return False
    
    ############################################################################
    # tracking methods
    ############################################################################
    def startTracking(self):
        self.gazeData = []
        self.eventData = []
        self.eyetracker.events.OnGazeDataReceived += self.on_gazedata
        self.eyetracker.StartTracking()
    
    def stopTracking(self):
        self.eyetracker.StopTracking()
        self.eyetracker.events.OnGazeDataReceived -= self.on_gazedata
        self.flushData()
        self.gazeData = []
        self.eventData = []
    
    def on_gazedata(self,error,gaze):
        self.gazeData.append(gaze)
    
    def getGazePosition(self,gaze): # modified to return relative coordinates rather than pixel coordinates
        return ((gaze.LeftGazePoint2D.x-0.5),
                (0.5-gaze.LeftGazePoint2D.y),
                (gaze.RightGazePoint2D.x-0.5),
                (0.5-gaze.RightGazePoint2D.y))
    
    def getCurrentGazePosition(self):
        if len(self.gazeData)==0:
            return (None,None,None,None)
        else:
            return self.getGazePosition(self.gazeData[-1])

    def getCurrentPupilsandValidity(self): # added
        if len(self.gazeData)==0:
            return(None,None,None,None)
        else:
            return self.getPupilsandValidity(self.gazeData[-1])

    def getPupilsandValidity(self, gaze): # added
        return (gaze.LeftPupil, gaze.LeftValidity, gaze.RightPupil, gaze.RightValidity)
    
    def setDataFile(self, openfile): # altered to take open file instead of filename
        self.datafile = openfile
        self.datafile.write('Recording date:\t'+datetime.datetime.now().strftime('%Y/%m/%d')+'\n')
        self.datafile.write('Recording time:\t'+datetime.datetime.now().strftime('%H:%M:%S')+'\n')
        self.datafile.write('Recording resolution\t%d x %d\n\n' % tuple(self.testWin.size))
        
    def closeDataFile(self): # altered to simply flush data, but not close file
        if self.datafile != None:
            self.flushData()
        
        self.datafile = None
    
    def recordEvent(self,event):
        t = self.syncmanager.convert_from_local_to_remote(self.clock.get_time())
        self.eventData.append((t,event))
    
    def flushData(self):
        if self.datafile == None:
            print 'data file is not set.'
            return
        
        if len(self.gazeData)==0:
            return
        
        self.datafile.write('\t'.join(['TimeStamp',
                                       'GazePointXLeft',
                                       'GazePointYLeft',
                                       'PupilLeft', # added
                                       'ValidityLeft',
                                       'GazePointXRight',
                                       'GazePointYRight',
                                       'PupilRight', # added
                                       'ValidityRight',
                                       'GazePointX',
                                       'GazePointY',
                                       'Event'])+'\n')
        timeStampStart = self.gazeData[0].Timestamp
        for g in self.gazeData:
            self.datafile.write('%.1f\t%.4f\t%.4f\t%.2f\t%d\t%.4f\t%.4f\t%.2f\t%d'%(
                                (g.Timestamp-timeStampStart)/1000.0,
                                g.LeftGazePoint2D.x if g.LeftValidity!=4 else -1.0, # modified to save relative coordinates rather than pixel coordinates
                                g.LeftGazePoint2D.y if g.LeftValidity!=4 else -1.0,
                                g.LeftPupil if g.LeftValidity!=4 else -1.0, # added
                                g.LeftValidity,
                                g.RightGazePoint2D.x if g.RightValidity!=4 else -1.0,
                                g.RightGazePoint2D.y if g.RightValidity!=4 else -1.0,
                                g.RightPupil if g.RightValidity!=4 else -1.0, # added
                                g.RightValidity))
            if g.LeftValidity == 4 and g.RightValidity == 4: #not detected
                ave = (-1.0,-1.0)
            elif g.LeftValidity == 4:
                ave = (g.RightGazePoint2D.x,g.RightGazePoint2D.y)
            elif g.RightValidity == 4:
                ave = (g.LeftGazePoint2D.x,g.LeftGazePoint2D.y)
            else:
                ave = (g.LeftGazePoint2D.x+g.RightGazePoint2D.x,
                       g.LeftGazePoint2D.y+g.RightGazePoint2D.y)
                
            self.datafile.write('\t%.4f\t%.4f\t'%ave)
            self.datafile.write('\n')
        
        formatstr = '%.1f'+'\t'*11+'%s\n'
        for e in self.eventData:
            self.datafile.write(formatstr % ((e[0]-timeStampStart)/1000.0,e[1]))
        
        self.datafile.flush()

############################################################################
# run following codes if this file is executed directly 
############################################################################
#
#if __name__ == "__main__":
#    import sys
#    
#    win = psychopy.visual.Window(size=(1280,1024),fullscr=True,units='pix')
#    controller = TobiiController(win)
#    controller.setDataFile('testdata.tsv')
#    
#    controller.waitForFindEyeTracker()
#    controller.activate(controller.eyetrackers.keys()[0])
#    
#    while True:
#        ret = controller.doCalibration([(0.1,0.1), (0.9,0.1) , (0.5,0.5), (0.1,0.9), (0.9,0.9)])
#        if ret == 'accept':
#            break
#        elif ret == 'abort':
#            controller.destroy()
#            sys.exit()
#    
#    marker = psychopy.visual.Rect(win,width=5,height=5)
#    
#    controller.startTracking()
#    
#    waitkey = True
#    while waitkey:
#        currentGazePosition = controller.getCurrentGazePosition()
#        if not None in currentGazePosition:
#            marker.setPos(currentGazePosition[0:2])
#        for key in psychopy.event.getKeys():
#            if key=='space':
#                waitkey = False
#            elif key=='w':
#                controller.recordEvent('w key')
#        
#        marker.draw()
#        win.flip()
#    
#    controller.stopTracking()
#    win.close()
#    controller.closeDataFile()
#    controller.destroy()
