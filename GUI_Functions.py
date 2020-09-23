# ---------------------------------------------------------------------
#                       GUI for Trial-Set-Up
# ---------------------------------------------------------------------

import tkinter as tk
from tkinter import filedialog, X, LEFT
import os
import mainLoop

ParadigmList = ["1 Back","2 Back","N-Back","Oddball"]
formatList = ['.mp4', 'jpg','png']
runTypeList = ['Custom', '1', '2', '3']
file_path = "Kein Pfad ausgewählt"

def dropDown(frame,app, options, label, width):
    var = tk.Label(frame, text=label, font=('Helvetica', 10), width = 15)
    var.pack(side = LEFT, padx=5, pady=5)
    variable = tk.StringVar(app)
    variable.set(options[0])
    opt = tk.OptionMenu(frame, variable, *options)
    opt.config(font=('Helvetica', 10), width = width)
    opt.pack(side = LEFT, padx=5, pady=5)
    return variable

def createButtons(frame,buttonName, commandFct, side, width):
    text_button = tk.Button(frame, text= buttonName, command = commandFct)
    text_button.pack(padx=40, pady=20,side=side)
    text_button.config(font=('Helvetica', 10), width = width)
    
def browseButton():
    global file_path
    file_path = filedialog.askdirectory()

# Create Labels and Boxes
def LabelsAndBoxes(app,frame, header):
    trials = tk.Label(frame, text=header, font=('Helvetica', 10), width = 15)
    trials.pack(side=LEFT, padx=5, pady=5)
    varName = tk.StringVar(app)
    varName.set('0')
    entry = tk.Entry(frame, textvariable=varName)
    entry.pack(side = LEFT, padx=5, expand=True)
    
    return varName

def createFrame(app, packOpt, padx, pady):
    frame = tk.Frame(app)
    frame.pack(fill = X, padx=padx, pady=pady)
    return frame

def runFile(app,file_path,cueType,paradigm, trialNr,blkSc, breakLen, cueLen, fixC, runType, runNr, condNr, imagePres, nMaxConsecTrials, t_mean_rand_break, t_zero_trial):
    
    isDirectory = os.path.isdir(file_path)
    startLoop = True
    
    if runType == 'Custom':
        if trialNr == '0' or cueLen == '0' or condNr == '0' or nMaxConsecTrials == '0':
            print('Set: Nr of Conditions, Nr of Trials/Cond, Task Length, Consecutive Trials ')
            startLoop = False
        else: 
            startLoop = True

    if isDirectory and startLoop:
        global stop
        stop = mainLoop.loop(file_path, cueType,paradigm, trialNr, blkSc, breakLen, cueLen, fixC, runType, runNr, condNr, imagePres, nMaxConsecTrials, t_mean_rand_break, t_zero_trial)
 
        if stop:
           app.destroy()
    else: 
        print('Invalid Input: Directory or Trial-Settings')
        
def openGUI():
    
    app = tk.Tk()
    app.geometry('800x450')
    app.title("GUI for Trial-Set-Up")
    
    # Space to top frame
    frame = createFrame(app, [], 5, 5)
    trials = tk.Label(app, text='GUI for Trial Set-Up', font=('Helvetica', 10))
    trials.pack()
    
    frame = createFrame(app, [], 5, 5)
    # Choose Paradigm
    paradigm = dropDown(frame, app, ParadigmList, "Paradigm:", 30)
    # Choose Run Type (Custom (set parameters yourself), Standard, ...)
    runType = dropDown(frame, app, runTypeList, "Run Type:", 10)


    frame = createFrame(app, [], 0, 0)
    # Cue Type
    cueType = dropDown(frame, app, formatList, "File Format:",10)
    # Folder containing stimulus videos or images
    createButtons(frame,'File Folder... ', browseButton, 'right', 25)
    # Time before actual trial starts
    t_zero_trial = LabelsAndBoxes(app,frame,"Time-0-Trial (s):")

    frame = createFrame(app, [], 5, 5)
    # Nr of current run (important for save name)
    runNr = LabelsAndBoxes(app,frame,"Run Nr.:")
    # Nr of different videos/images
    condNr = LabelsAndBoxes(app,frame,"Nr of Conditions.:")
    
    frame = createFrame(app, [], 5, 5)
    # Trials (how many trials per condition)
    trialNr = LabelsAndBoxes(app,frame, "Nr of Trials/Cond:")
    # Cue Length (in s) - total time per rial
    cueLen = LabelsAndBoxes(app,frame,"Task Length (eg.15s):")

    frame = createFrame(app, [], 5, 5)
    # Fixation Cross Display (in s)
    fixC = LabelsAndBoxes(app,frame,"Fixation Cross (s):")
    # Break Length - time after trial
    breakLen = LabelsAndBoxes(app,frame,"Break (eg 2.5):")
    
    frame = createFrame(app, [], 5, 5)
    # Number of consecutive trials
    nMaxConsecTrials = LabelsAndBoxes(app,frame,"Consecutive Trials:")
    # Random Break Length 
    t_mean_rand_break = LabelsAndBoxes(app,frame,"Random Break:")
    
    frame = createFrame(app, [], 5, 5)
    # Black Screen Length (Display of black screen in seconds - usually 0/auto)
    blkSc = LabelsAndBoxes(app,frame,"Black-Screen:")
    # Time for image presentation (in s)
    imagePres = LabelsAndBoxes(app,frame,"Image Presentation:")
   
    frame = createFrame(app, [], 150, 0)
    # Start Button
    createButtons(frame,'Start',lambda: runFile(app, file_path, cueType.get(), paradigm.get(), trialNr.get(), blkSc.get(), breakLen.get(), cueLen.get(), fixC.get(), runType.get(), runNr.get(), condNr.get(), imagePres.get(), nMaxConsecTrials.get(), t_mean_rand_break.get(), t_zero_trial.get()), 'left', 5)
    # Schließen des Pop-Up Fensters
    createButtons(frame,'Exit', app.destroy, 'right', 5)
    
    # Opens Pop-Up and waits for input
    app.mainloop()

    return 

# Run this file:
# It opens the GUI in which all parameters can be set
# By pressing start, the mainLoop function is activated and 
# runs all trials 
openGUI()


