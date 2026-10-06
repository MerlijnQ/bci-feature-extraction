import numpy as np
import pyxdf
import pickle

# LOAD XDF FILE AND SEPARATE STREAMS
xdf_path = "/mnt/c/Users/Gianluca/Downloads/sub-P001/ses-S001/eeg/sub-P001_ses-S001_task-Default_run-001_eeg.xdf"  # Update with your .xdf file path
streams, header = pyxdf.load_xdf(xdf_path)

eeg_stream = None
marker_stream = None

def get_stream_data(stream):
    # Identify streams by type or name
    for stream in streams:
        s_type = stream['info']['type'][0]
        s_name = stream['info']['name'][0]
        
        if s_type == 'EEG' or 'Unicorn' in s_name:
            eeg_stream = stream
        elif s_type == 'Markers' or s_name == 'MotorImageryMarkers':
            marker_stream = stream

    # Extract data matrices and timestamps
    eeg_data = np.array(eeg_stream['time_series'])       # Shape: (samples, channels)
    eeg_timestamps = np.array(eeg_stream['time_stamps'])  # Shape: (samples,)
    fs = float(eeg_stream['info']['nominal_srate'][0])     # Nominal sampling rate (e.g., 250 Hz)

    marker_series = [m[0] for m in marker_stream['time_series']]
    marker_timestamps = np.array(marker_stream['time_stamps'])

    print(f"Loaded EEG Stream: {eeg_data.shape[1]} channels @ {fs:.1f} Hz ({eeg_data.shape[0]} samples)")
    print(f"Loaded Marker Stream: {len(marker_series)} markers found")

    return eeg_data, eeg_timestamps, marker_series, marker_timestamps, fs

# EPOCH EEG DATA AROUND MARKERS (hint: find the closest EEG timestamps to marker timestamp)
# you can also infer 'y' based on your markers: IMAGERY_LEFT, CUE_RIGHT, etc. 
# process and extract the features 
#Epoch classification window 3.25–4.25 s 

def epoch_eeg_data(eeg_data, eeg_timestamps, marker_timestamps, marker_series, epoch_onset=3.25, duration=1.0):

    epochs = []
    labels = []
    for marker_time, marker_label in zip(marker_timestamps, marker_series):
        # Find the closest EEG timestamp to the marker
        start_idx = np.argmin(np.abs(eeg_timestamps - (marker_time + epoch_onset)))

        end = eeg_timestamps[start_idx] + duration

        end_idx = np.argmin(np.abs(eeg_timestamps - end))
        
        # Extract the epoch data
        epoch_data = eeg_data[start_idx:end_idx]
        epochs.append(epoch_data)
        labels.append(marker_label)

    return (np.array(epochs), np.array(labels))

#save epochs
eeg_data, eeg_timestamps, marker_series, marker_timestamps, fs = get_stream_data(streams)
data = epoch_eeg_data(eeg_data, eeg_timestamps, marker_timestamps, marker_series)
print(f"Extracted {len(data[0])} epochs from EEG data.")

with open("epochs.pkl", "wb") as f:
    pickle.dump(data, f)
