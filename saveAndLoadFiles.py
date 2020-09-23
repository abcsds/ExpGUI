#------------------------------------------------------------------------------
#                 Save and Reload File with Trial-Variables
#------------------------------------------------------------------------------

import pickle

def saveVariables(timing_tStart,timing_trialTimings, \
                  timing_trialSequence, timing_taskOnset, timing_nTrials, \
                  timing_nStates, subject_like_dislike, RUN_TYPE, RUN_NR, \
                  nTrialMax, measCount,loop_not_stop, loop_newTrial, loop_newState, \
                  loop_measure_speed, loop_lastTrial, loop_id, loop_fileName, \
                  loop_feedback, loop_cTrial, loop_cState,loop_cRun, loop_cLoop, \
                  loop_cLinState, kb_read_last,  kb_read_interval, kb_key_value, \
                  kb_key_new, feedback_update, exitScreen):
    
    f = open(loop_fileName + str('_variables.pckl'), 'wb')
    pickle.dump(timing_tStart, f)
    pickle.dump([timing_trialTimings], f)
    pickle.dump(timing_trialSequence, f)
    pickle.dump(timing_taskOnset, f)
    pickle.dump(timing_nTrials, f)  
    pickle.dump(timing_nStates, f)  
    pickle.dump(subject_like_dislike, f)     
    pickle.dump(RUN_TYPE, f)  
    pickle.dump(RUN_NR, f)  
    pickle.dump(nTrialMax, f)  
    pickle.dump(measCount, f) 
    pickle.dump(loop_not_stop, f) 
    pickle.dump(loop_newTrial, f) 
    pickle.dump(loop_newState, f) 
    pickle.dump(loop_measure_speed, f) 
    pickle.dump(loop_lastTrial, f) 
    pickle.dump(loop_id, f) 
    pickle.dump(loop_fileName, f) 
    pickle.dump(loop_feedback, f) 
    pickle.dump(loop_cTrial, f) 
    pickle.dump(loop_cState, f) 
    pickle.dump(loop_cRun, f) 
    pickle.dump(loop_cLoop, f) 
    pickle.dump(loop_cLinState, f)  
    pickle.dump(kb_read_last, f) 
    pickle.dump(kb_read_interval, f) 
    pickle.dump(kb_key_value, f) 
    pickle.dump(kb_key_new, f) 
    pickle.dump(feedback_update, f) 
    pickle.dump(exitScreen, f) 
    f.close()


def loadVariables(loop_fileName):

    with open(loop_fileName + str('_variables.pckl'), 'rb') as f:
        timing_tStart = pickle.load(f)
        timing_trialTimings = pickle.load(f)
        timing_trialSequence = pickle.load(f)
        timing_taskOnset = pickle.load(f)
        timing_nTrials = pickle.load(f)
        timing_nStates = pickle.load(f)
        subject_like_dislike = pickle.load(f)
        RUN_TYPE = pickle.load(f)
        RUN_NR = pickle.load(f)
        nTrialMax = pickle.load(f)
        measCount = pickle.load(f)
        loop_not_stop = pickle.load(f)
        loop_newTrial = pickle.load(f)
        loop_newState = pickle.load(f)
        loop_measure_speed = pickle.load(f)
        loop_lastTrial = pickle.load(f)
        loop_id = pickle.load(f)
        loop_fileName = pickle.load(f)
        loop_feedback = pickle.load(f)
        loop_cTrial = pickle.load(f)
        loop_cState = pickle.load(f)
        loop_cRun = pickle.load(f)
        loop_cLoop = pickle.load(f)
        loop_cLinState = pickle.load(f)
        kb_read_last = pickle.load(f)
        kb_read_interval = pickle.load(f)
        kb_key_value = pickle.load(f)
        kb_key_new = pickle.load(f)
        feedback_update = pickle.load(f)
        exitScreen = pickle.load(f)
        
        return timing_tStart,timing_trialTimings,timing_trialSequence,  \
                  timing_taskOnset, timing_nTrials, timing_nStates, \
                  subject_like_dislike, RUN_TYPE, RUN_NR, nTrialMax, \
                  measCount,loop_not_stop, loop_newTrial, loop_newState, \
                  loop_measure_speed, loop_lastTrial, loop_id, loop_fileName, \
                  loop_feedback, loop_cTrial, loop_cState,loop_cRun, loop_cLoop, \
                  loop_cLinState, kb_read_last,  kb_read_interval, kb_key_value, \
                  kb_key_new, feedback_update, exitScreen
