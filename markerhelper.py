import time
import random
from pylsl import StreamInfo, StreamOutlet
import winsound

def create_marker_outlet():
    info = StreamInfo(
        name='MotorImageryMarkers',
        type='Markers',
        channel_count=1,
        nominal_srate=0,  # Irregular sampling rate for event-based triggers
        channel_format='string',
    )
    return StreamOutlet(info)

def run_motor_imagery_paradigm(outlet, total_trials=1):

    conditions = ['LEFT', 'RIGHT']
    
    for trial_num in range(1, total_trials + 1):
        # Randomly select task condition
        # You can also include additional markers
        # Adjust the timings. 

        # 1. FIXATION 

        #2. WARNING BEEP
        winsound.Beep(frequency=1000, duration=500) #in ms

        # 3. CUE + Marker
        outlet.push_sample([f"CUE_{condition}"])

        # 4. IMAGERY + Marker
        outlet.push_sample([f"IMAGERY_{condition}"])

        # 5. INTER-TRIAL INTERVAL (ITI) 


if __name__ == '__main__':
    # Initialize the marker stream first
    marker_outlet = create_marker_outlet()
    
    print("LSL Marker Outlet initialized: 'MotorImageryMarkers'")
    
    # Linking to LabRecorder
    print("0. Start Unicorn Recorder and run the paradigm code.")
    print("\n1. Open LSL LabRecorder.")
    print("2. Click 'Update' and ensure both 'Unicorn' and 'MotorImageryMarkers' are visible.")
    print("3. Select both streams and click 'Start' to begin recording.")
    
    input("\n--> Press ENTER in this terminal once LabRecorder is recording to start the task...")

    # Start Experiment
    run_motor_imagery_paradigm(marker_outlet, total_trials=1)