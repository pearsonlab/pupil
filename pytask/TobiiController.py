#!/usr/bin/python
#
# Tobii Glasses controller for PsychoPy
# author: Shariq Iqbal
#

import sys
import time
import threading
import urllib2
import json
import socket
from psychopy import core

GLASSES_IP = "192.168.71.50"  # IPv4 address
PORT = 49152
base_url = 'http://' + GLASSES_IP
timeout = 1

# Keep-alive message content used to request live data and live video streams
KA_DATA_MSG = "{\"type\": \"live.data.unicast\", \"key\": \"some_GUID\", \"op\": \"start\"}"
KA_VIDEO_MSG = "{\"type\": \"live.video.unicast\", \"key\": \"some_other_GUID\", \"op\": \"start\"}"


class TobiiController:

    def __init__(self):
        peer = (GLASSES_IP, PORT)
        data_socket = self.mksock(peer)
        td = threading.Thread(
            target=self.send_keepalive_msg, args=[data_socket, KA_DATA_MSG, peer])
        td.daemon = True
        td.start()

        # Create socket which will send a keep alive message for the live video
        # stream
        video_socket = self.mksock(peer)
        tv = threading.Thread(
            target=self.send_keepalive_msg, args=[video_socket, KA_VIDEO_MSG, peer])
        tv.daemon = True
        tv.start()

        try:
            self.create_project()
            self.create_participant()
        except:
            print "Could not connect to Tobii Glasses"
            sys.exit()

        self.events = []
        self.eventData = {}
        self.datafile = None

    # Create UDP socket
    def mksock(self, peer):
        iptype = socket.AF_INET
        if ':' in peer[0]:
            iptype = socket.AF_INET6
        return socket.socket(iptype, socket.SOCK_DGRAM)

    # Callback function
    def send_keepalive_msg(self, socket, msg, peer):
        while True:
            socket.sendto(msg, peer)
            time.sleep(timeout)

    def post_request(self, api_action, data=None):
        url = base_url + api_action
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        data = json.dumps(data)
        response = urllib2.urlopen(req, data)
        data = response.read()
        json_data = json.loads(data)
        return json_data

    def get_request(self, api_action):
        url = base_url + api_action
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req)
        data = response.read()
        json_data = json.loads(data)
        return json_data

    def wait_for_status(self, api_action, key, values):
        url = base_url + api_action
        running = True
        while running:
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, None)
            data = response.read()
            json_data = json.loads(data)
            if json_data[key] in values:
                running = False
            time.sleep(1)

        return json_data[key]

    def create_project(self):
        json_data = self.post_request('/api/projects')
        self.project_id = json_data['pr_id']

    def create_participant(self):
        data = {'pa_project': self.project_id}
        json_data = self.post_request('/api/participants', data)
        self.participant_id = json_data['pa_id']

    def create_calibration(self):
        data = {'ca_project': self.project_id, 'ca_type': 'default',
                'ca_participant': self.participant_id}
        json_data = self.post_request('/api/calibrations', data)
        self.calibration_id = json_data['ca_id']

    def start_calibration(self):
        self.post_request(
            '/api/calibrations/' + self.calibration_id + '/start')

    def create_recording(self):
        data = {'rec_participant': self.participant_id}
        json_data = self.post_request('/api/recordings', data)
        self.recording_id = json_data['rec_id']

    def start_recording(self):
        self.post_request('/api/recordings/' + self.recording_id + '/start')

    def stop_recording(self):
        self.post_request('/api/recordings/' + self.recording_id + '/stop')

    def waitForFindEyeTracker(self):
        while len(self.eyetrackers.keys()) == 0:
            time.sleep(0.01)

    ##########################################################################
    # tracking methods
    ##########################################################################
    def startTracking(self):
        self.eventData = {}
        self.events = []
        self.sync_pulses = []
        self.start_sync()
        self.start_recording()

    def stopTracking(self):
        self.stop_recording()
        self.stop_sync()
        self.flushData()
        self.eventData = {}
        self.events = []
        self.sync_pulses = []

    # starts thread to listen to sync port of Tobii Glasses and record pulses
    def start_sync(self):
        self.stop_event = threading.Event()
        sync_thread = threading.Thread(target=self.get_pulses)
        sync_thread.start()

    def stop_sync(self):
        self.stop_event.set()

    def get_pulses(self):
        while not self.stop_event.is_set():
            # self.sync_pulses.append(core.getTime())
            core.wait(1.0)

    # altered to take open file instead of filename. got rid of header which
    # makes the file incompatible with matlab
    def setDataFile(self, openfile):
        self.datafile = openfile

    # altered to simply flush data, but not close file
    def closeDataFile(self):
        if self.datafile is not None:
            self.flushData()

        self.datafile = None

    def recordEvent(self, event):  # records timestamp for an event
        self.eventData[event].append(core.getTime())

    def addParam(self, param, value):  # appends value to param list
        self.eventData[param].append(value)

    def setParam(self, param, value):  # sets value for param
        self.eventData[param] = value

    def setVector(self, param, vector):  # sets a vector in an event parameter
        self.eventData[param] = list(vector)

    # creates columns for events and params
    def setEventsAndParams(self, events):
        self.events = events
        for event in events:
            self.eventData[event] = []

    # altered to create data file that is easily imported into matlab
    def flushData(self):
        if self.datafile is None:
            print 'Data file is not set.'
            return

        if len(self.eventData) == 0:
            return

        self.eventData['sync_pulses'] = self.sync_pulses
        self.datafile.write(json.dumps(self.eventData))

        self.datafile.flush()
