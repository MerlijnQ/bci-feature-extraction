"""
Real-time feature extraction pipeline
"""

from pylsl import StreamInlet, resolve_streams
from src.window import SlidingWindow
from src.bandpower import BandPower
from src.log import FeatureLogger
import numpy as np

FS = 250
N_CHANNELS = 8
WINDOW_SECONDS = 0.5
WINDOW_SIZE = int(FS * WINDOW_SECONDS)
# CHANGE THIS
CHANNEL_IDX = [0, 1]

#Resulting overlaps for different windows
#0.5 seconds = (1-25/125) = 0.8
#1 seconds = (1-25/250) = 0.9
#2.5 seconds = (1-25/625) = 0.96

# 0.5 seconds too little might have to do with ERDS. 
# Note that 0.5 suffers from poor frequency resolution and high noise sensitivity. 
# Might have to do with nyquist. 
# I.e. some frequencies might not be visible meaning we cannot pick up those at the end of the bet spectrum


streams = resolve_streams(1)
inlet = StreamInlet(streams[0])

# CHANGE THIS
# give 2 channels for testing
window = SlidingWindow(size=WINDOW_SIZE, step=FS // 10, channels= 8)
feature = BandPower(fs=FS, band=(8, 12))
logger = FeatureLogger(f"features_size_{WINDOW_SECONDS}.csv")

window.start_clock()

while True:
    sample, _ = inlet.pull_sample()
    # CHANGE THIS
    # pick just one channel for testing
    # sample = sample[:2]
    win = window.update(sample)

    if win is not None:
        #win = (time, channels). We want to extract channels at CHANNEL_IDX
        win = win[:, CHANNEL_IDX]
        feats = feature.compute(win)
        log_psd = np.log10(feats)
        logger.log(feats) #logging a tuple?
        print("Features:", feats)
