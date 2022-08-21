"""
Sample PHD2 python client demo
"""

from imp import new_module
from guider import Guider
import sys
import time
import math
from datetime import datetime, timedelta
from alpaca.telescope import Telescope

def waitUntil(endTime: datetime, msg: str) -> None:
    while endTime > datetime.now():
        remaining = (endTime - datetime.now()).total_seconds()
        print("%s: %d seconds" %(msg, round(remaining)))
        time.sleep(remaining - math.floor(remaining))

host = "localhost"
if len(sys.argv) > 1:
    host = sys.argv[1]

with Guider(host) as guider:
    guider.Connect()

    T = Telescope('localhost:11111', 0) # Local EQ5 Mount
    T.Connected = True

    # timer settings (seconds)
    # -> same kinds of settings as on the handheld shutter release timer
    # -> set to same values, except for the starting delay
    startDelay = 15         # set to 5 sec more then on the handheld to be able to sync propperly
    exposure = 20 * 60.0    # duration of exposures
    breakTime = 60.0        # time for new position to settle (60 is a good start)
    numFrames = math.ceil(5.5 * ((60*60)/exposure))   # number of exposures to take

    # dither settings
    # -> don't change unless you know why
    # -> settling is not checked, so timeouts don't matter
    ditherPixels = 10.0
    settlePixels = 2.0
    settleTime = 10.0
    settleTimeout = 20

    # number of seconds we assume the handheld timer could be out of sync
    # with this script's timer
    PADDING = 2.0

    # START

    # initial delay
    nextEvent = datetime.now() + timedelta(seconds=startDelay)
    waitUntil(nextEvent, "Starting in")

    # exposure/dither loop
    for i in range(numFrames):
        print("START EXPOSURE")
        nextEvent = datetime.now() + timedelta(seconds=exposure)
        waitUntil(nextEvent, "Exposure ends in")
        nextEvent = datetime.now() + timedelta(seconds=PADDING)
        waitUntil(nextEvent, "Making sure exp. is done for")
        nextEvent = datetime.now() + timedelta(seconds=breakTime - PADDING)
        guider.Dither(ditherPixels, settlePixels, settleTime, settleTimeout)
        print("DITHER")
        waitUntil(nextEvent, "Waiting for guider to settle")

    # cleaning up
    print("DONE")
    T.Tracking = False
    T.Connected = False
    guider.Disconnect()

