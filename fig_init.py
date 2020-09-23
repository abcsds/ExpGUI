from psychopy import visual, core, monitors
import os

# ------------------------------------------
# ---------- Set-Up Screen ----------------
# ------------------------------------------


def ScreenSetUp():
    # monitors for which calibration files exist
    print("Screen Set-Up")
    allMon = monitors.getAllMonitors()

    # get number of screens available - with external monitor it's 2
    screenCount = len(allMon)

    # display experiment on "last" - (external) second - monitor
    dispScreen = screenCount - 1

    # get dimensions of screen for experiment
    dim = monitors.Monitor("default").getSizePix()

    # Create a window
    win = visual.Window(
        size=dim,
        monitor=allMon[dispScreen],
        color=[-1, -1, -1],
        fullscr=1,
        screen=dispScreen,
        allowGUI=False,
        checkTiming=True,
    )

    return win, dim


# ------------------------------------------
# --------- Build paths to stimuli ---------
# ------------------------------------------
def buildPath_Stim(path, extension):
    images = [img for img in os.listdir(path) if img.endswith(extension)]

    imgPath = []
    # Build the path to each stimulus
    for img in range(0, len(images)):

        imgPath.append(path + "/" + images[img])

    return imgPath


# ------------------------------------------
# ----------- Store all Movies -------------
# ------------------------------------------
def loadMovies(win, stimPaths):

    movieStorage = []

    # Open all Movie-Files
    for i in range(0, len(stimPaths)):
        # Open all Videos
        clip = visual.MovieStim3(
            win, stimPaths[i], flipVert=False, flipHoriz=False, loop=False
        )

        # Store all Videos in variable for quick access later on
        movieStorage.append(clip)

    return movieStorage


# ------------------------------------------
# ------------  Store all Images -----------
# ------------------------------------------
def loadImages(win, stimPaths):

    imageStorage = []

    for i in range(0, len(stimPaths)):

        # Open all Images
        img = visual.ImageStim(win, image=stimPaths[i])

        # Store all Images in variable for quick access later on
        imageStorage.append(img)

    return imageStorage


# --------------------------------------------
# ------------ Initialization ----------------
# --------------------------------------------
def fig_init(RUN_TYPE, path, extension):

    # Get all files with a certain extension within folder
    stimPaths = buildPath_Stim(path, extension)

    # Initialize and open new window
    win, dim = ScreenSetUp()

    # Check extension to load correct stimulus
    if extension == ".mp4":
        stimulus = loadMovies(win, stimPaths)

    elif extension == "jpg" or extension == "png":
        stimulus = loadImages(win, stimPaths)

    # Create initial message
    message = visual.TextStim(
        win, text="The measurement is about to start ...", color=[1, 1, 1]
    )
    message.draw()
    win.flip()

    return win, dim, stimulus


# --------------------------------------------
# ------------ Close Window ------------------
# --------------------------------------------
def fig_close(window):
    window.close()
    return
