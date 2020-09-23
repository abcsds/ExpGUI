#
# ------------------------- Timing Functions ---------------------------
#

import time
import numpy as np

def RUN_TYPE_0(condNr, trialNr,breakLen, cueLen, blkSc, fixC, nMaxConsecTrials, t_mean_rand_break, t_zero_trial):
#
    nDiffCond= condNr
    nTrialsPerCond= trialNr
    nMaxConsecTrials= nMaxConsecTrials
    t_cross_mi= cueLen  
    t_break_min= breakLen 
    t_mean_rand_break =  t_mean_rand_break
    t_zero_trial= t_zero_trial
    t_cross_ref= fixC 
    t_instr_mi=blkSc
    
    return nDiffCond, nTrialsPerCond, nMaxConsecTrials, t_cross_mi,t_break_min, t_mean_rand_break, t_zero_trial, t_cross_ref, t_instr_mi

def RUN_TYPE_1():

    nDiffCond= 6
    nTrialsPerCond= 1
    nMaxConsecTrials= 1
    t_cross_mi= 15 # image presentation
    t_break_min= 2.5 # break after task
    t_mean_rand_break= 0.5
    t_zero_trial= 1.5
    t_cross_ref= 2 # reference cross/dot presentation
    t_instr_mi= 0

    return nDiffCond, nTrialsPerCond, nMaxConsecTrials, t_cross_mi,t_break_min, t_mean_rand_break, t_zero_trial, t_cross_ref, t_instr_mi

def RUN_TYPE_2():

    nDiffCond= 6
    nTrialsPerCond= 30
    nMaxConsecTrials= 2
    t_cross_mi= 0.080 # image presentation
    t_break_min= 1.5 # break after task
    t_mean_rand_break= 0
    t_zero_trial= 1.5
    t_cross_ref= 0.5 # reference cross/dot presentation
    t_instr_mi= 0

    return nDiffCond, nTrialsPerCond, nMaxConsecTrials, t_cross_mi,t_break_min, t_mean_rand_break, t_zero_trial, t_cross_ref, t_instr_mi

def RUN_TYPE_3():

    nDiffCond = 10
    nTrialsPerCond= 10
    nMaxConsecTrials= 2
    t_cross_mi= 0.080 # image presentation
    t_break_min= 1.5 # break after task
    t_mean_rand_break= 0
    t_zero_trial= 1.5
    t_cross_ref= 0.5 # reference cross/dot presentation
    t_instr_mi= 0

    return nDiffCond, nTrialsPerCond, nMaxConsecTrials, t_cross_mi,t_break_min, t_mean_rand_break, t_zero_trial, t_cross_ref, t_instr_mi

def indices(a,b):
        ind = []
        for i in range(0,(len(a))):
            if a[i] != b[i]:
                ind.append(i)
    
        return ind  
            
    
def rle(sequence):
    print('Please check the rle-Function in file timing_Functions ')
    
    # if x: #decoding #if iscell(x) % decoding
    #     i = np. cumsum([1, x[1]]) #i = cumsum([ 1 x{2} ]);
    #     j = np.zeros([1, i[-1]-1])
    #     j[0][i[:-1]-1] = 1 # matlab beginnt bei index 1, python bei 0
    #                 # um den gleichen Inhalt im array zu erhalten,
    #                 # muss 1 abgezogen werden von position i
    #                 # ansonsten kommt statt [1 0 ] bei python [0 1]
        
    #     data = [x[0]* np.cumsum(j)] #data = x{1}(cumsum(j));
    
    if 'sequence' in locals(): #encoding
        sequence = np.array(sequence)
        sequence = sequence.reshape(np.shape(sequence)[0], 1)
        if np.shape(sequence)[0] > np.shape(sequence)[1]:
            sequence = np.transpose(sequence)
        x1 = sequence[0][0:len(sequence[0])-1]    
        x2 = sequence[0][1:len(sequence[0])] 
        i = indices(x1,x2)
        i.append(np.shape(sequence)[1]-1)
        data = np.stack((sequence[0][i], np.diff(np.hstack((1, i)))))   
    
    return data
    

def timing_init(RUN_TYPE, condNr, trialNr,taskLen, cueLen, blkSc, fixC, nMaxConsecTrials, t_mean_rand_break, t_zero_trial):

    # Define timing for different run types
    if RUN_TYPE == 3:
        nDiffCond, nTrialsPerCond, nMaxConsecTrials, t_cross_mi,t_break_min, t_mean_rand_break, t_zero_trial, t_cross_ref, t_instr_mi = RUN_TYPE_3()
    if RUN_TYPE == 2:
        nDiffCond, nTrialsPerCond, nMaxConsecTrials, t_cross_mi,t_break_min, t_mean_rand_break, t_zero_trial, t_cross_ref, t_instr_mi = RUN_TYPE_2()
    if RUN_TYPE == 1:
        nDiffCond, nTrialsPerCond, nMaxConsecTrials, t_cross_mi,t_break_min, t_mean_rand_break, t_zero_trial, t_cross_ref, t_instr_mi = RUN_TYPE_1()
    if RUN_TYPE == 0:
        nDiffCond, nTrialsPerCond, nMaxConsecTrials, t_cross_mi,t_break_min, t_mean_rand_break, t_zero_trial, t_cross_ref, t_instr_mi= RUN_TYPE_0(condNr, trialNr,taskLen, cueLen, blkSc, fixC, nMaxConsecTrials, t_mean_rand_break, t_zero_trial)
    
    # construct the pseudo random trial sequence
    nTrials = nDiffCond * nTrialsPerCond
    np.random.seed()
    
    trialSequence = []
    
    for var in range(0,nTrialsPerCond): 
        tempRand = np.random.permutation(nDiffCond)
        trialSequence.extend(tempRand)
    
    rleData = rle(trialSequence)

    nLoop = 0

    while True:

        nLoop = nLoop+1
        
        if sum(rleData[1] > nMaxConsecTrials) > 0:
            np.random.seed()
            trialSequence = np.random.permutation(nTrials)
            rleData = rle(trialSequence)
        else:
            break
        
        if nLoop > 1000:
            print('!!! Error: Was not able to create a suitable trial sequence within 1000 attempts !!!')
            break
    
    # construct the timings matrix
    trialTimings = np.zeros((nTrials,4))
    cTrialStart = t_zero_trial
    
    for cur in range(0,nTrials):
        trialTimings[cur][0] = cTrialStart
        trialTimings[cur][1]  = cTrialStart + t_cross_ref
        trialTimings[cur][2] = cTrialStart + t_cross_ref + t_instr_mi
        trialTimings[cur][3] = cTrialStart + t_cross_ref + t_instr_mi + t_cross_mi
        
        cTrialStart = cTrialStart+t_break_min+t_mean_rand_break*2*np.random.rand(1)+t_cross_mi+t_instr_mi+t_cross_ref
        
    var = trialTimings[-1][-1] + t_break_min+t_mean_rand_break*2*np.random.rand(1)
    trialTimings = np.vstack((trialTimings, [var[0], 0,0,0]))
    trialTimings = np.transpose(trialTimings)
    
    nStates = nTrials*4
    
    return trialSequence, trialTimings, nStates, nTrials


def timing_check(tStart,trialTimings,cLinState,newState):

    trialTimings = trialTimings.flatten('F')
    
    if (time.time() - tStart) > trialTimings[cLinState+1]:
        cLinState = cLinState+1
        newState = True
    
    return cLinState, newState
