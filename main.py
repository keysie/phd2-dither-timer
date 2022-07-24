"""
Sample PHD2 python client demo
"""

from imp import new_module
from guider import Guider
import sys
import time
import math
from datetime import datetime, timedelta

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

    # dither settings
    ditherPixels = 10.0
    settlePixels = 2.0
    settleTime = 10.0
    settleTimeout = 20

    # timer settings (seconds)
    startDelay = 3
    exposure = 10  #15 * 60.0
    breakTime = 30.0

    PADDING = 2.0

    # START

    # initial delay
    nextEvent = datetime.now() + timedelta(seconds=startDelay)
    waitUntil(nextEvent, "Starting in")

    # exposure/dither loop
    while 1==1:
        print("START EXPOSURE")
        nextEvent = datetime.now() + timedelta(seconds=exposure)
        waitUntil(nextEvent, "Exposure ends in")
        nextEvent = datetime.now() + timedelta(seconds=PADDING)
        waitUntil(nextEvent, "Making sure exp. is done for")
        nextEvent = datetime.now() + timedelta(seconds=breakTime - PADDING)
        guider.Dither(ditherPixels, settlePixels, settleTime, settleTimeout)
        print("DITHER")
        waitUntil(nextEvent, "Waiting for guider to settle")
