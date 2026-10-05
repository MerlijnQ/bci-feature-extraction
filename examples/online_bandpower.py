"""
Plot band power features in real time
"""

import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_byprop, resolve_streams
from src.utils.window import SlidingWindow
from src.utils.bandpower import BandPower

FS = 250
N_CHANNELS = 8
WINDOW_SECONDS = 0.5
WINDOW_SIZE = int(FS * WINDOW_SECONDS)

streams = resolve_streams(1)
inlet = StreamInlet(streams[0])

window = SlidingWindow(size=WINDOW_SIZE, step=FS // 10, channels= 8)
feature = BandPower(FS, (8, 12))

values = []

plt.ion()
fig, ax = plt.subplots()

window.start_clock()

while True:
    sample, _ = inlet.pull_sample()
    win = window.update(sample)

    if win is not None:
        bp = feature.compute(win)[0]
        values.append(bp)

        if len(values) > 50:
            values.pop(0)

        ax.clear()
        ax.plot(values)
        ax.set_title("Alpha Band Power (Channel 1)")
        plt.pause(0.01)

