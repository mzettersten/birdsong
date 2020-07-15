####################################
#Active Learning Experiment - Tobii#
####################################

#Version 7

#import constants for pygaze
import constants


#load pygaze libraries and custom pygaze libraries
import pygaze
from pygaze import libscreen
from pygaze import libtime
from pygaze import libinput
#from pygaze import eyetracker
from pygaze import libgazecon
from stimPresPyGaze import *

#import basic python utility libraries
import random
import math
import time, os

#load psychopy and custom psychopy libraries
from baseDefsPsychoPy import *
from stimPresPsychoPy import *

#import trial list
import Birdsong_generateTrials

import moviepy


class Exp:
    def __init__(self):
        self.expName = 'Bird'
        self.path = os.getcwd()
        self.subjInfo = {
                '1':  { 'name' : 'subjCode',
                        'prompt' : 'EXP_XXX',
                        'options': 'any',
                        'default':self.expName+'_101'},
                '2' : {	'name' : 'gender', 
			'prompt' : 'Subject Gender m/f: ', 
			'options' : ("m","f"),
			'default':'',
			'type' : str},
		'3' : {	'name' : 'age', 
			'prompt' : 'Subject Age: ', 
			'options' : 'any',
			'default':'',
			'type' : str},
		'4' : {'name' : 'seed', 
			'prompt' : 'Seed: ', 
			'options' : 'any', 
			'default' : 101, 
			'type' : 101},	
		'5' : {'name' : 'expInitials', 
			'prompt' : 'Experiment Initials: ', 
			'options' : 'any', 
			'default' : '', 
			'type' : str},
		'6' : {	'name' : 'activeMode', 
			'prompt' : 'input / gaze', 
			'options' : ("input","gaze"),
			'default':"gaze",
			'type' : str},
		'7' : { 'name' : 'inputDevice',
                        'prompt' : 'keyboard / mouse',
                        'options' : ("keyboard","mouse"),
                        'default':'keyboard'},
		'8' : { 'name' : 'eyetracker', 
			'prompt' : '(yes / no)', 
			'options' : ("yes","no"), 
			'default' : "yes", 
			'type' : str},
		'9' : { 'name' : 'pygazeVersion', 
			'prompt' : '(04 / 06)', 
			'options' : ("04","06"), 
			'default' : "06", 
			'type' : str},
		}

        optionsReceived = False
        fileOpened = False
        while not fileOpened:
            [optionsReceived, self.subjVariables] = enterSubjInfo(self.expName, self.subjInfo)
            constants.LOGFILENAME=constants.LOGFILEPATH+self.subjVariables['subjCode']
            constants.LOGFILE=constants.LOGFILENAME[:]
            if self.subjVariables['pygazeVersion'] == "06":
                from pygaze import display
                from pygaze import settings
                settings.LOGFILE = constants.LOGFILENAME[:]
                print settings.LOGFILE
            if not optionsReceived:
                popupError(self.subjVariables)
            elif not os.path.isfile('data/'+'data_'+self.subjVariables['subjCode']+'.txt'):
                
                #if using an eyetracker
                if self.subjVariables['eyetracker']=="yes":
                    #import eyetracking package from pygaze
                    from pygaze import eyetracker
                    
                    if not os.path.isfile(constants.LOGFILENAME+'_TOBII_output.tsv'):
                        fileOpened = True
                        self.outputFile = open('data/'+'data_'+self.subjVariables['subjCode']+'.txt','w')
                        
                    else:
                        fileOpened = False
                        popupError('That subject code for the eyetracking data already exists! The prompt will now close!')  
                        core.quit()  
                else:
                    fileOpened = True
                    self.outputFile = open('data/'+'data_'+self.subjVariables['subjCode']+'.txt','w')
            else:
                fileOpened = False
                popupError('That subject code already exists!')        
                    
        # create display object
        self.disp = libscreen.Display(disptype='psychopy')
        
        #create psychopy window based on Display() object 
        if self.subjVariables['pygazeVersion'] == "06":
            self.win = pygaze.expdisplay 
        else: 
            self.win = self.disp.expdisplay  
        
        if self.subjVariables['eyetracker']=="yes":
            # create eyetracker object
            self.tracker = eyetracker.EyeTracker(self.disp)
        
        if self.subjVariables['inputDevice'] == 'keyboard': 
            print "Using keyboard..."
            self.inputDevice = "keyboard"
            self.validResponses = {'1':'space','2': 'enter'}
            ## create keyboard object
            self.input = libinput.Keyboard(keylist=['space', 'enter', 'left', 'right'], timeout=None)
        elif self.subjVariables['inputDevice'] == 'mouse':
            print "Using mouse..."
            self.inputDevice = "mouse"
            self.input = libinput.Mouse(mousebuttonlist=[1], timeout=None)
            if self.subjVariables['activeMode']=="input":
                self.input.set_visible(visible=True)

        self.imagePath=self.path+'/stimuli/images/'
        self.soundPath=self.path+'/stimuli/sounds/'
        self.moviePath=self.path+'/stimuli/movies/'
        self.imageExt='.png'
        
class ExpPresentation(Exp):
    def __init__(self,experiment):
        self.experiment = experiment
        
    def initializeExperiment(self):
        
        print "Loading files..."
        loadScreen = libscreen.Screen()
        loadScreen.draw_text(text="Loading Files...",colour="lightgray", fontsize=48)
        self.experiment.disp.fill(loadScreen)
        self.experiment.disp.show()
        self.imageScreen=libscreen.Screen(disptype="psychopy")
        imageName=self.experiment.imagePath+"bunnies.png"
        image=visual.ImageStim(self.experiment.win, imageName,mask=None,interpolate=True) 
        image.setPos((0,0))
        buildScreenPsychoPy(self.imageScreen,[image]) 
        setAndPresentScreen(self.experiment.disp,self.imageScreen)
        
        self.imageScreen2=libscreen.Screen(disptype="psychopy")
        imageName2=self.experiment.imagePath+"puppies.png"
        image2=visual.ImageStim(self.experiment.win, imageName2,mask=None,interpolate=True) 
        image2.setPos((0,0))
        buildScreenPsychoPy(self.imageScreen2,[image2])
        
        trialsPath = 'trialLists/Bird_trialList_%s_%s.csv' % (self.experiment.subjVariables['subjCode'],self.experiment.subjVariables['seed'])
        
        if not os.path.isfile(trialsPath):
            print 'Trials file not found. Creating...'
            Birdsong_generateTrials.main(self.experiment.subjVariables['subjCode'],self.experiment.subjVariables['seed'])

        
        (self.trialListMatrix, self.trialFieldNames) = importTrials(trialsPath, method="sequential")
        
        #number of trials
        self.numTrials = 12
        
        #load sound files
        self.pictureMatrix = loadFiles('stimuli/images', ['png',], 'image', self.experiment.win)
        self.soundMatrix = loadFiles('stimuli/sounds',['wav'], 'sound')
        
        #load AG movie
        self.mov = visual.MovieStim3(self.experiment.win, self.experiment.moviePath+"pinwheel.mov",loop=True,noAudio=True,size=(600,445))
        
        self.locations=['center']
        self.pos={'center': (0,0)}
        
        
        self.posDims=(600,600)
        self.posImageDims=(400.0,400.0)
        
        #set duration of pauses between trial events
        #this may need to be changed
        self.ISI=500
        self.screenPause=500
        self.BoxStep = 20
        self.BoxStepCount = 600
        self.picStepSize = 1
        
        self.AGTimeOut = 20000
        self.AGFixCount = 30
        self.lookAwayPos = (-1920,-1200)
        
        
        #gaze contingent params
        self.aoiCenter=libgazecon.AOI('rectangle',pos=(640,280),size=[640,640])
        self.aoiCenterMovie=libgazecon.AOI('rectangle',pos=(560,300),size=[800,600])
        self.aoiScreen=libgazecon.AOI('rectangle',pos=(0,0),size=[1920,1200])
            
        #all geometric objects to be drawn
        self.AGCircle=visual.Circle(self.experiment.win, radius=100, fillColor="green",lineColor="green")
        self.rect = newRect(self.experiment.win,self.posDims,self.pos['center'],"white")
        self.grayRect = newRect(self.experiment.win,(600,300),(0,450),"lightgray")

        print "Files Loaded!"
        
        
    def presentAGTrial(self,curTrial, getInput,AGTime):
        
        libtime.pause(self.ISI)
        
        self.experiment.disp.show()
        
        if curTrial['AGType']=="image":
            #create picture
            curPic=self.pictureMatrix[curTrial['image']][0]
            curPic.pos=(0,0)
            
            #build screen
            agScreen=libscreen.Screen(disptype='psychopy')
            buildScreenPsychoPy(agScreen, [curPic])
            #wait 1 s
            libtime.pause(self.agWait1)
            #present screen
            setAndPresentScreen(self.experiment.disp, agScreen)
            #play audio
            playAndWait(self.soundMatrix[curTrial['audio']],waitFor=0)
            #display for rest of ag Time
            libtime.pause(AGTime)
        
        elif curTrial['AGType']=="movie":
            #load movie stim
            print(self.experiment.moviePath)
            print(curTrial['AGVideo'])
            mov = visual.MovieStim3(self.experiment.win, self.experiment.moviePath+curTrial['AGVideo'])
            while mov.status != visual.FINISHED:
                mov.draw()
                self.experiment.win.flip()
        
        #if getInput=True, wait for keyboard press before advancing
        if getInput:
            self.experiment.input.get_key()
        
       
    def presentScreen(self,screen):
        # show text screen
        setAndPresentScreen(self.experiment.disp,screen)
        if self.experiment.inputDevice=='mouse':
            self.experiment.input.get_clicked()
        else:
            self.experiment.input.get_key()    
          
    def easeInOut(self,startValue,changeInValue,currentIteration,totalIterations,direction):
        a = currentIteration / (totalIterations)
        if (a<0.5):
            return direction * (changeInValue)*2*a*a + startValue
        else:
            return direction * (-1+(4-2*a)*a)*(changeInValue) + startValue
    
    def increase(self,startValue,changeInValue,currentIteration,totalIterations,direction):
        a = currentIteration / (totalIterations)
        return direction * changeInValue * a + startValue
        
    def watchProcedure(self,curTrial,startTime,maxTime,maxLookAwayTime, aoi,looming=False,curPic=None,stim1=None,stim2=None,stim3=None):
        totalLookingTime = 0
        nonLookingTimes = []
        transitionNonLookingTimes = []
        lookAways = 0
        curNonLookingTime = 0
        looking = True
        nonLook = False
        curLookAwayTime = 0
        responded = True
        counter=0.0
        direction=1
        startValues=(300,300)
        loomCounter = 0
        transition=False
        #list to store last 150 ms of looking
        last150ms=[]
        #store current location to initiate checking of when looks go off screen
        if self.experiment.subjVariables['activeMode']=="gaze":
            lastInputpos = self.experiment.tracker.sample()
        elif self.experiment.subjVariables['activeMode']=="input" and self.experiment.subjVariables['inputDevice']=="mouse":
            lastInputpos = self.experiment.input.get_pos()
        if lastInputpos == self.lookAwayPos:
            transitionNonLookingTimeOnset = libtime.get_time()
            
        while libtime.get_time() - startTime < maxTime and curLookAwayTime < maxLookAwayTime:
            if self.experiment.subjVariables['activeMode']=="input" and self.experiment.subjVariables['inputDevice']=="keyboard":
                for key in event.getKeys():
                    if key == 'space' and looking ==True:
                        responded = False
                        event.clearEvents()
                    elif key == 'space' and looking ==False:
                        responded = True
                        event.clearEvents()
                    
            else:
                libtime.pause(10)
                #get gaze/ mouse position
                if self.experiment.subjVariables['activeMode']=="gaze":
                    curInputpos = self.experiment.tracker.sample()
                elif self.experiment.subjVariables['activeMode']=="input":
                    curInputpos = self.experiment.input.get_pos()
                #mark transition time
                if curInputpos == self.lookAwayPos and lastInputpos != self.lookAwayPos:
                    transition=True
                    transitionNonLookingTimeOnset = libtime.get_time()
                else:
                    transition = False
                
                ####smoothing eyetracking/mousetracking sample###
                
                ##add cur gaze position to the list
                last150ms.append(curInputpos)
                #
                ##if the length of the list exceeds 150 ms/25==6, then delete the earliest item in the lis
                ## 25 ms because an average run through the while loop takes between 20-30 ms
                if len(last150ms)>6:
                    del last150ms[0]
                
                ##Now, remove the (no looking data) tuples
                last150msClean=[e for e in last150ms if e != self.lookAwayPos]
                ##Now calculate the mean
                if len(last150msClean)>0:
                    #calculate mean
                    #looks a bit tricky, but that's jsut because I think the gaze positions are stored as tuples, which is a bit of an odd data structure.
                    inputpos=tuple(map(lambda y: sum(y) / float(len(y)), zip(*last150msClean)))
                else:
                    inputpos=self.lookAwayPos
 
                ####smoothing procedure end###
                
                responded = aoi.contains(inputpos)
                                
                #update last gaze position
                lastInputpos = curInputpos
              
            if not responded and looking:
                nonLookingTimeOnset = libtime.get_time()
                looking = False
                lookAways +=1
                nonLook = True
                
            
            
            if responded:
                if not looking:
                    looking = True
                    nonLookOnset = False
                    curNonLookingTime=libtime.get_time()-nonLookingTimeOnset
                    curTransitionNonLookingTime=libtime.get_time()- transitionNonLookingTimeOnset
                    nonLookingTimes.append(curNonLookingTime)
                    transitionNonLookingTimes.append(curTransitionNonLookingTime)
            
            if looking:
                curLookAwayTime = 0
            else:
                curLookAwayTime = libtime.get_time() - nonLookingTimeOnset
                if curLookAwayTime > maxLookAwayTime:
                    nonLookingTimes.append(curLookAwayTime)
                    curTransitionNonLookingTime=libtime.get_time()- transitionNonLookingTimeOnset
                    transitionNonLookingTimes.append(curTransitionNonLookingTime)
            
            if looming:
                  
                #update screen
                newScreen=libscreen.Screen(disptype='psychopy')
                counter +=1
                if counter > 100:
                    direction=(-1)*direction
                    counter = 0.0
                    startValues=(xSize,ySize)
                xSize = self.easeInOut(startValues[0],200.0,counter,100,direction)
                ySize = self.easeInOut(startValues[1],200.0,counter,100,direction)
                curPic.size = (xSize,ySize)
                buildScreenPsychoPy(newScreen,[stim1,curPic,stim2,stim3])
                setAndPresentScreen(self.experiment.disp, newScreen)
            
                
                    
        totalTime=libtime.get_time()-startTime
        totalLookingTime = totalTime - sum(nonLookingTimes)
        totalLookingTimeNonSmoothed = totalTime - sum(transitionNonLookingTimes)
        return [totalTime, lookAways, totalLookingTime,totalLookingTimeNonSmoothed]
 
              
    def presentTrial(self,curTrial,curTrialIndex):
        #self.checkExit()
        #self.experiment.disp.show()
        
        #random jitter prior to trial start
        libtime.pause(self.ISI+random.choice([0,100,200])) 
        
        
        
        #######start eye tracking##########
        if self.experiment.subjVariables['eyetracker']=="yes":
            self.experiment.tracker.start_recording()
            #log data on trial
            self.experiment.tracker.log("Experiment %s subjCode %s seed %s TrialNumber %s TrialType %s audio %s image %s" % (self.experiment.expName, self.experiment.subjVariables['subjCode'],str(self.experiment.subjVariables['seed']),str(curTrialIndex),curTrial['audioType'], curTrial['audio'],curTrial['image']))
        #start trial timer
        trialTimerStart=libtime.get_time()
        
        

        #create ag screen
        #agScreen=libscreen.Screen(disptype='psychopy')
        agScreenTime=libtime.get_time()  
        if self.experiment.subjVariables['eyetracker']=="yes":
            #log event
            self.experiment.tracker.log("agStart")
        
        agCount = 0
        keyBreak = False
        movPlaying = True
        self.mov.play()
        while self.mov.status != visual.FINISHED and libtime.get_time() - agScreenTime < self.AGTimeOut:
            self.mov.draw()
            self.experiment.win.flip()
            
            libtime.pause(10)
            
            if self.experiment.subjVariables['activeMode']=="input" and self.experiment.subjVariables['inputDevice']=="keyboard":
                for key in event.getKeys():
                    if key == 'space':
                        if self.mov.status == visual.PLAYING:
                            self.mov.pause()
                            self.experiment.win.flip()
                            movPlaying = False
                        keyBreak = True
                        
                if keyBreak:
                    break
            else:  
                if self.experiment.subjVariables['activeMode']=="gaze":
                    inputpos = self.experiment.tracker.sample()
                elif self.experiment.subjVariables['activeMode']=="input" and self.experiment.subjVariables['inputDevice']=="mouse":
                    inputpos = self.experiment.input.get_pos()
            
            
                if self.aoiCenterMovie.contains(inputpos):
                    agCount += 1
                if agCount > self.AGFixCount:
                    #if self.mov.status == visual.PLAYING:
                    break
                    
        if movPlaying:       
            if self.mov.status == visual.PLAYING:
                self.mov.pause()
                self.experiment.win.flip()
                    
        #print libtime.get_time() - agScreenTime
                
        if self.experiment.subjVariables['eyetracker']=="yes":
                    #log event
                    self.experiment.tracker.log("agEnd")
            
        #create starting screen
        startScreen=libscreen.Screen(disptype='psychopy')
        curPic=self.pictureMatrix[str(curTrial['image'])][0]
        curPicCoord=self.pos['center']
        curPic.setPos(curPicCoord)
        curPic.size = (300,300)
        curBox = self.pictureMatrix[str(curTrial['box'])][0]
        curBox.size = self.posDims
        curBox.pos = self.pos['center']
        buildScreenPsychoPy(startScreen,[self.rect,curPic,curBox,self.grayRect])
        
        #present starting screen
        setAndPresentScreen(self.experiment.disp, startScreen)
        startScreenTime=libtime.get_time()  
        if self.experiment.subjVariables['eyetracker']=="yes":
            #log event
            self.experiment.tracker.log("startScreen")
        
        libtime.pause(self.screenPause)
        
        
        #slide screen up
        for i in range(0,self.BoxStepCount+1,self.BoxStep):
                #set up box
                curBox.pos=(self.pos['center'][0],i)
                #add new screen
                curScreen=libscreen.Screen(disptype='psychopy')
                #add stimuli to the screen
                buildScreenPsychoPy(curScreen,[self.rect,curPic,curBox,self.grayRect])
                setAndPresentScreen(self.experiment.disp,curScreen)
                if i==self.BoxStepCount:
                    screenUpTime=libtime.get_time()
                    if self.experiment.subjVariables['eyetracker']=="yes":
                        #log screen slide event
                        self.experiment.tracker.log("screenUp")
        
        #play audio
        self.soundMatrix[curTrial['audio']].play()
        audioStartTime=libtime.get_time()
        if self.experiment.subjVariables['eyetracker']=="yes":
            #log audio event
            self.experiment.tracker.log("audioStart")
        
    
        
        ######Contingent Procedure######
        lookProcedureTimes = self.watchProcedure(curTrial,audioStartTime,curTrial['audioDur'],1000,self.aoiScreen,looming=True,curPic=curPic,stim1=self.rect,stim2=curBox,stim3=self.grayRect)
        #print lookProcedureTimes
        self.soundMatrix[curTrial['audio']].stop()
        self.experiment.disp.show()
        audioEndTime=libtime.get_time()-audioStartTime
        if self.experiment.subjVariables['eyetracker']=="yes":
            #log audio end event
            self.experiment.tracker.log("audioEnd")
        
        ######Stop Eyetracking######
        
        #trialEndTime
        trialTimerEnd=libtime.get_time()
        #trial time
        trialTime=trialTimerEnd-trialTimerStart
        if self.experiment.subjVariables['eyetracker']=="yes":
            #stop eye tracking
            self.experiment.tracker.stop_recording()
        
        #######Save data#########
        
        fieldVars=[]
        for curField in self.trialFieldNames:
            fieldVars.append(curTrial[curField])
   
        [header, curLine] = createRespNew(self.experiment.subjInfo, self.experiment.subjVariables, self.trialFieldNames, fieldVars,
                                        a_curTrialIndex=curTrialIndex,
                                        b_expTimer=trialTimerEnd,
                                        c_trialStart=trialTimerStart,
                                        d_trialTime=trialTime,
                                        e_totalTime = lookProcedureTimes[0],
                                        f_lookAways = lookProcedureTimes[1],
                                        g_totalLookingTime = lookProcedureTimes[2],
                                        h_totalLookingTimeNS = lookProcedureTimes[3],
                                        i_agScreenTime = agScreenTime,
                                        j_startScreenTime = startScreenTime,
                                        k_audioStartTime=audioStartTime,
                                        l_audioEndTime = audioEndTime
                                        )
        
        writeToFile(self.experiment.outputFile,curLine)
             
    def cycleThroughExperimentTrials(self, whichPart):
        
        if whichPart=="trials":
            curTrialIndex =1
            for curTrial in self.trialListMatrix.trialList:
                self.presentTrial(curTrial,curTrialIndex)
                curTrialIndex += 1
            self.experiment.outputFile.close() 

        
################
#RUN EXPERIMENT#
################  

#Create the experiment object and run the individual phases
     
#creat experiment object      
currentExp = Exp()
#load ExpPresentation class
currentPresentation = ExpPresentation(currentExp)
#initialize the experiment
currentPresentation.initializeExperiment()
#present the starting screen and wait for button press
currentPresentation.presentScreen(currentPresentation.imageScreen2)
#present trials
currentPresentation.cycleThroughExperimentTrials("trials")
if currentExp.subjVariables['eyetracker']=="yes":
    #close tracker
    currentExp.tracker.close()
#close experiment and expend libtime
currentExp.disp.close()
libtime.expend()
        