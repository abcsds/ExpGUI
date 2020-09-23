# ---------------------------------------------------------------------
# -------------------------- LSL - Functions --------------------------
# ---------------------------------------------------------------------

import pylsl
from pylsl import StreamInfo, StreamOutlet

def lsl_init():
    
    print('Creating a new marker stream info...')
    info = StreamInfo('paradigm', 'trigger', 1, 0, pylsl.cf_int32, 'mysourceID')
   
    if  'chunksize' not in locals():
          chunksize = 0

    if 'maxbuffered' not in locals():
        maxbuffered = 360
        
    print('Opening an outlet...')
    hOutlet = StreamOutlet(info, chunksize, maxbuffered)
    
    return hOutlet

def lsl_close(lsl_hOutlet):
    
    # close LSL stream
    #lsl_hOutlet.close()
    # lsl_hOutlet.push_sample(["End_of_Trial"])
    return
