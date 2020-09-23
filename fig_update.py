#
# -------------------------- Figure Update ----------------------------------
#
from psychopy import visual, core

# ------------------------------------------
#     Black Screen Setting
# ------------------------------------------


def setScreenBlack(win, blackScreenTime):
    win.color = "black"
    win.flip(clearBuffer=True)
    # core.wait(blackScreenTime)
    return win


# ------------------------------------------
#     Fixation cross / fixation dot
# ------------------------------------------
def drawCross(win, dim, crossDuration):
    xLine = visual.Line(
        win, lineWidth=15, start=(-300 / dim[0], 0), end=(300 / dim[0], 0)
    )
    xLine.draw()
    yLine = visual.Line(
        win, lineWidth=15, start=(0, 300 / dim[1]), end=(0, -300 / dim[1])
    )
    yLine.draw()
    win.flip()
    # core.wait(crossDuration)
    return win


def fig_update(
    cLinState,
    cState,
    cTrial,
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
):

    if cLinState > timing_nStates - 1:
        cState = 5

    if cState == -1:
        # white/black screen
        lsl_hOutlet.push_sample([10])  # lsl_outlet Function
        # print('- Sending start trigger. (10)')
        logger.info("- Sending start trigger. (10)")

        # Now fill the screen white
        # Actual command made screen black
        # Flip to screen
        win = setScreenBlack(win, [])

    if cState == 1:
        # Fixation cross/dot
        lsl_hOutlet.push_sample([11])
        # print('- Sending fixation cross trigger. (11)')
        logger.info("- Sending fixation cross trigger. (11)")

        # Draw Cross and flip to screen
        win = drawCross(win, dim, [])

    if cState == 2:
        # Now fill the screen white - original code: screen = black
        win = setScreenBlack(win, 0)

    if cState == 3:
        cCond = timing_trialSequence[cTrial - 1]
        trig = 20 + cCond

        lsl_hOutlet.push_sample([trig])
        logger.info("- Sending condition video trigger.({}) ".format(str(trig)))

        if extension == ".mp4":
            # video presentation
            while stimulus[cCond].status != visual.FINISHED:

                stimulus[cCond].draw()
                win.flip()
        else:
            stimulus[cCond].draw()
            win.flip()
            if imagePres == 0 or imagePres == "0":
                imagePres = 1
            core.wait(imagePres)

        trig = 30 + cCond

        lsl_hOutlet.push_sample([trig])
        logger.info("- Sending condition MI trigger. ({})".format(str(trig)))

        # Draw text
        message = visual.TextStim(win, text="Imagine", color="white")
        message.draw()  # Draw the stimulus to the window.
        win.flip()  # Flip backside of the window.

    if cState == 4:
        # send break trigger
        lsl_hOutlet.push_sample([12])
        logger.info("- Sending break trigger. (12)")

        # Fill screen black
        win = setScreenBlack(win, [])

    if cState == 5:
        # Send lsl trigger
        lsl_hOutlet.push_sample([11])
        logger.info("- Sending end trigger. (10)")

        # Draw text
        message = visual.TextStim(win, text="Done!", color="white")
        message.draw()
        win.flip()

    return timing_taskOnset, win
