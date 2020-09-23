
from psychtoolbox import PsychHID
import time
import numpy as np


def kb_init():
    
    #create the keyboard queue
    PsychHID('KbQueueCreate') # Psychtoolbox 
    
    # start logging keyboard button presses
    PsychHID('KbQueueStart')

    # initializations
    key_new = False
    key_value = []
    read_last = time.time()
    read_interval = 1/3.1 # every 1/3.1 sec
    
    return key_new, key_value, read_last, read_interval

def kb_read(): 
   
    [key_new, firstPress, _, _, _] = PsychHID('KbQueueCheck')
    # time when keyboard was last checked
    read_last = time.time()
    # if there was a key press find the key name
    if key_new:
         ind1, ind2 = np.unravel_index(firstPress.argmax(), firstPress.shape)

         if (ind2) == 26:
             key_value = 'ESCAPE'
         elif (ind2) == 12:
             key_value = 'Return'
         else: 
             key_value = chr(ind2+1)
    else:
         key_value = []
    
    return read_last, key_new, key_value

def kb_close():
    PsychHID('KbQueueRelease')
    return