"""
Sliding window for streaming EEG samples; Code adjusted to the implementation of the previous assignment.
"""

# import numpy as np

# class SlidingWindow:
#     def __init__(self, size, step):
#         self.size = size
#         self.step = step
#         self.buffer = []
#         self.counter = 0

#     def update(self, sample):
#         self.buffer.append(sample)
#         self.counter += 1

#         if len(self.buffer) > self.size:
#             self.buffer.pop(0)

#         if len(self.buffer) == self.size and self.counter % self.step == 0:
#             return np.array(self.buffer)

#         return None


import numpy as np
import pylsl as lsl

class SlidingWindow:
    def __init__(self, size, step, channels):
        self.size = size
        self.step = step
        self.channels = channels
        self.buffer = np.empty((0, channels))
        self.counter = 0
        self.is_full = False
        self.start_time = None

    def start_clock(self):
        self.start_time = lsl.local_clock()

    def update(self, sample):
            
        sample = np.array(sample)
        self.buffer = np.vstack((self.buffer, sample))

        if self.is_full:
            self.counter += len(sample)


        if len(self.buffer) > self.size:
            self.buffer = self.buffer[-self.size:]      

        if len(self.buffer) == self.size and self.counter % self.step == 0:

            if not self.is_full:
                self.is_full = True
                end_time = lsl.local_clock()
                time_span = self.start_time - end_time
                print(f"Time taken to full up buffer: {time_span}")
                print(f"Size of window {self.buffer.T.shape}")

            
            if len(self.buffer.shape) > 1:
                return self.buffer.T
            else:
                return self.buffer
            

        return None

