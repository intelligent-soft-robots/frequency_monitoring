#!/usr/bin/env python3

import numpy 
import time
from frequency_monitoring import FrequencyMonitoring


SIZE=500
SEGMENT_ID="frequency_monitoring_demo"

print("\nrunning with segment id:",SEGMENT_ID)
print("start in another terminal: frequency_monitoring -segment_id frequency_monitoring_demo")

fm = FrequencyMonitoring(SEGMENT_ID,SIZE)

print("\npinging at 50Hz, low standard deviation\n")
time_start = time.time()
while time.time()-time_start < 20:
    fm.ping()
    fm.share()
    time.sleep(1./50.)

print("pinging at 100Hz, low standard deviation\n")
time_start = time.time()
while time.time()-time_start < 20:
    fm.ping()
    fm.share()
    time.sleep(1./100.)

print("pinging at 50Hz, with standard deviation of 5\n")
mean=50
sd=5
nb_points=mean*20
frequencies=numpy.random.normal(mean,sd,nb_points)
for f in frequencies:
    fm.ping()
    fm.share()
    time.sleep(1./f)

print("pinging at 100Hz, with standard deviation of 20\n")
mean=100
sd=20
nb_points=mean*20
frequencies=numpy.random.normal(mean,sd,nb_points)
for f in frequencies:
    fm.ping()
    fm.share()
    time.sleep(1./f)

    
    
    

    
