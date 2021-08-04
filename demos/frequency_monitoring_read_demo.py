#!/usr/bin/env python3

import numpy 
import time
from frequency_monitoring import read


SEGMENT_ID="frequency_monitoring_demo"

fp = read(SEGMENT_ID)

print(str("\nmean: {}\n"
          "sd: {}\n"
          "min: {}\n"
          "max: {}\n".format(fp.mean,
                             fp.sd,
                             fp.min,
                             fp.max)))

