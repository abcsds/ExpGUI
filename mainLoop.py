# --------------------- Import Libraries ----------------------------

import os
import time
import numpy as np

# --------------------- Import Functions ----------------------------
from diary import diary, closeHandlersDiary
from kb_Functions import kb_init, kb_read, kb_close
from lsl_Functions import lsl_init, lsl_close
from timing_Functions import timing_init, timing_check
from fig_init import fig_init, fig_close
from fig_update import fig_update
from saveAndLoadFiles import saveVariables  # , loadVariables


# Function for mainLoop and Trial-Execution
def loop(
    path,
    extension,
    paradigm,
    trialNr,
    blkSc,
    taskLen,
    cueLen,
    fixC,
    runType,
    runNr,
    condNr,
    imagePres,
    nMaxConsecTrials,
    t_mean_rand_break,
    t_zero_trial,
):
    # starterTime = time.time()
    print("*** Loop started. ***")

    # Type 1: Run Nr. 1,10
    #         Stimulus presentation = 1500 ms, each stimulus 3 times
    # Type 2: Run Nr. 2,3,4,5,6,7
    #         Stimulus presentation = 80 ms, each stimulus 10 times
    # Type 3: Run Nr. 8,9
    #         Timing as in Type 2, no fixation point before stimulus presentation

    # RUN_TYPE = 1 # Standard

    # Set RUN_TYPE variable and run number
    # "Custom" runType:  set variables for customized trial execution
    if runType == "Custom":
        RUN_TYPE = 0
        cueLen = float(cueLen)
        trialNr = int(trialNr)
        taskLen = float(taskLen)
        blkSc = float(blkSc)
        fixC = float(fixC)
        condNr = int(condNr)
        runNr = int(runNr)
        imagePres = float(imagePres)
        nMaxConsecTrials = int(nMaxConsecTrials)
        t_mean_rand_break = float(t_mean_rand_break)
        t_zero_trial = float(t_zero_trial)
    else:
        RUN_TYPE = int(runType)

    # RUN_NR will always start with 1 - if it is not set, it will be auto-set.
    if runNr == 0:
        RUN_NR = 1
    else:
        RUN_NR = runNr

    # participant's data
    loop_id = "SUPER_"
    loop_cRun = str(RUN_NR)
    loop_fileName = loop_id + str(RUN_TYPE) + "_run_" + loop_cRun

    # Check if file name already exists, if so, stop trial (avoid overwriting)
    if os.path.isfile(loop_fileName):
        print("!!! Error filename already existing. Stopping !!!")
        print("*** finished ***")
        return

    # Diary-Writer
    logger, fileHandler, consoleHandler = diary(loop_fileName)

    loop_measure_speed = False
    loop_feedback = True
    loop_not_stop = True

    # initialize keyboard queue
    logger.info("- Initializing keyboard queue.")
    kb_key_new, kb_key_value, kb_read_last, kb_read_interval = kb_init()

    # initialize lab streaming layer
    logger.info("- Initializing LSL.")
    lsl_hOutlet = lsl_init()

    # initialize figure
    print("First Timer - t_zero_trial mit 1.5s")
    updateFig = time.time()

    logger.info("- Initializing figure.")
    win, dim, stimulus = fig_init(RUN_TYPE, path, extension)

    # initialize trial sequence and timings
    logger.info("- Initializing trial sequence.")
    (
        timing_trialSequence,
        timing_trialTimings,
        timing_nStates,
        timing_nTrials,
    ) = timing_init(
        RUN_TYPE,
        condNr,
        trialNr,
        taskLen,
        cueLen,
        blkSc,
        fixC,
        nMaxConsecTrials,
        t_mean_rand_break,
        t_zero_trial,
    )

    # initialize loop variables
    logger.info("- Initializing main loop variables.")
    loop_cLoop = 0
    loop_cLinState = -2
    loop_newState = False
    loop_newTrial = False
    loop_lastTrial = 0
    feedback_update = False

    # loop_measure_speed = True
    if loop_measure_speed:

        loop_start_time = time.time()
        loop_nLoopMax = int((timing_trialTimings[0][-1] + 600) * 25000)

        loop_speed = np.empty(
            (
                loop_nLoopMax,
                1,
            )
        )
        loop_speed[:] = np.nan

    # Vector for subject feedback
    subject_like_dislike = np.zeros(np.shape(timing_trialSequence))
    # Vector to save task presentation time (Screen Flip time)
    timing_taskOnset = np.zeros((len(timing_trialSequence) + 2, 3))
    # Maximal number of trials
    nTrialMax = len(timing_trialSequence)

    try:
        # main loop
        logger.info("- Running main loop.")
        while loop_not_stop:
            loop_cLoop = loop_cLoop + 1

            if loop_measure_speed:
                loop_speed[loop_cLoop] = time.time() - loop_start_time

            if time.time() - kb_read_last > kb_read_interval:
                [kb_read_last, kb_key_new, kb_key_value] = kb_read()

            # check for start signal via keyboard (Return key)
            if loop_cLinState == -2 and kb_key_new:
                if kb_key_value == "Return":
                    timing_tStart = time.time()
                    loop_cLinState = -1
                    loop_newState = True

            # check timings for new state
            if loop_cLinState >= -1 and loop_cLinState <= timing_nStates:
                loop_cLinState, loop_newState = timing_check(
                    timing_tStart, timing_trialTimings, loop_cLinState, loop_newState
                )

            if loop_cLinState > -1:
                loop_cState, loop_cTrial = np.unravel_index(
                    loop_cLinState, np.shape(timing_trialTimings), order="F"
                )
                loop_cTrial = loop_cTrial + 1
                loop_cState = loop_cState + 1

            else:
                loop_cState = -1
                loop_cTrial = 1

            # check if new state is a trial start
            if loop_newState and loop_cLinState >= 0 and loop_cTrial <= timing_nTrials:
                if loop_lastTrial < loop_cTrial:
                    loop_newTrial = True
                    logger.info("-- Current trial: " + str(loop_cTrial))

                loop_lastTrial = loop_cTrial

            # set measCount back to 1 for every new trial
            if loop_newTrial:
                measCount = 1

            # update figure and lsl trigger
            if loop_newState:
                ende = time.time() - updateFig
                print("Ende Timer für fig_update: " + str(ende))

                fig_update(
                    loop_cLinState,
                    loop_cState,
                    loop_cTrial,
                    timing_trialSequence,
                    timing_nStates,
                    lsl_hOutlet,
                    timing_taskOnset,
                    win,
                    dim,
                    stimulus,
                    extension,
                    imagePres,
                    logger,
                )

                print("Starte neuen Timer mit tic")
                updateFig = time.time()

            # check keyboard conditions
            if kb_key_new and (kb_key_value == "ESCAPE"):
                loop_not_stop = False

            elif kb_key_new and (kb_key_value == "1"):
                subject_like_dislike[loop_cTrial - 1] = 1
                logger.info("Subject: Like - 1")

            elif kb_key_new and (kb_key_value == "2"):
                subject_like_dislike[loop_cTrial - 1] = 2
                logger.info("Subject: Dislike - 2")

            # Stopping criterion
            if loop_measure_speed:
                if loop_cLoop >= loop_nLoopMax:
                    loop_not_stop = False

            elif loop_cTrial == nTrialMax + 1:
                loop_not_stop = False

            # reset messages
            kb_key_new = False
            loop_newState = False
            loop_newTrial = False
            feedback_update = False

    except:
        logger.info("Error")
        closeHandlersDiary(fileHandler, consoleHandler)

    logger.info("*** Main loop finished. Exit screen and save data with ESCAPE ***")

    exitScreen = False
    printMsg = True

    while not exitScreen:

        if kb_key_value == "ESCAPE":

            exitScreen = True

        elif printMsg:
            print("ESCAPE and Exit GUI")
            printMsg = False
        [_, _, kb_key_value] = kb_read()

    # close figure
    logger.info("- Closing figure.")
    fig_close(win)

    # close lsl stream
    logger.info("- Closing LSL stream.")
    lsl_close(lsl_hOutlet)

    # close keyboard queue
    logger.info("- Closing keyboard queue.")
    kb_close()

    # saving data
    logger.info("- Saving data.")
    # save(loop_fileName,'-v7.3')

    #  Save all variables from trial to pkl-File
    saveVariables(
        timing_tStart,
        timing_trialTimings,
        timing_trialSequence,
        timing_taskOnset,
        timing_nTrials,
        timing_nStates,
        subject_like_dislike,
        RUN_TYPE,
        RUN_NR,
        nTrialMax,
        measCount,
        loop_not_stop,
        loop_newTrial,
        loop_newState,
        loop_measure_speed,
        loop_lastTrial,
        loop_id,
        loop_fileName,
        loop_feedback,
        loop_cTrial,
        loop_cState,
        loop_cRun,
        loop_cLoop,
        loop_cLinState,
        kb_read_last,
        kb_read_interval,
        kb_key_value,
        kb_key_new,
        feedback_update,
        exitScreen,
    )

    # End of Output - close ALL handlers
    closeHandlersDiary(fileHandler, consoleHandler)

    logger.info("- Exit GUI")
    # endTime = time.time() - starterTime
    # print("Dauer des Programmes: {}".format(endTime))
    return True


# Load variables from pkl-file
# timing_tStart,timing_trialTimings, \
#         timing_trialSequence, timing_taskOnset, timing_nTrials, \
#         timing_nStates, subject_like_dislike, RUN_TYPE, RUN_NR, \
#         nTrialMax, measCount,loop_not_stop, loop_newTrial, loop_newState, \
#         loop_measure_speed, loop_lastTrial, loop_id, loop_fileName, \
#         loop_feedback, loop_cTrial, loop_cState,loop_cRun, loop_cLoop, \
#         loop_cLinState, kb_read_last,  kb_read_interval, kb_key_value, \
#         kb_key_new, feedback_update, exitScreen = loadVariables(loop_fileName)
