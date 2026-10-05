import time
import random
from pylsl import StreamInfo, StreamOutlet
# use this instead of winsound because winsound only works on Windows. 
# on Linux:
# sudo apt install sox
# sudo apt install libsox-fmt-all
from beep import Beep

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
        cue_finished = False
        # Randomly select task condition
        condition = random.choice(conditions)
        # You can also include additional markers
        # Adjust the timings. 
        start_time = time.time()

        # 1. FIXATION 
        print("X")
        time.sleep(2.0)

        #2. WARNING BEEP
        Beep(freq=1000, ms= 500)
        time.sleep(1.5)

        # 3. CUE + Marker
        while time.time() - start_time < 3.0:
            time.sleep(0.001)  # Wait until 3 seconds have passed

        print(f"CUE_{condition}")
        outlet.push_sample([f"CUE_{condition}"])
        time.sleep(1.25)
        
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