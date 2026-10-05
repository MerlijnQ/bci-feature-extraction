import numpy as np
import pyxdf

# LOAD XDF FILE AND SEPARATE STREAMS
xdf_path = "C:/Users/Gianluca/OneDrive/Documenti/University/2_I_a/Realtime_BCI/CurrentStudy/sub-P001/ses-S001/eeg/deneme.xdf"  # Update with your .xdf file path
streams, header = pyxdf.load_xdf(xdf_path)

eeg_stream = None
marker_stream = None

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

# EPOCH EEG DATA AROUND MARKERS (hint: find the closest EEG timestamps to marker timestamp)
# you can also infer 'y' based on your markers: IMAGERY_LEFT, CUE_RIGHT, etc. 
# process and extract the features 
#Epoch classification window 3.25–4.25 s 

