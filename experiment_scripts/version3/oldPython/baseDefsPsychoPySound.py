from psychopy import prefs

##import sound##
try:
    import winsound
    winSoundLoaded=True
    
except ImportError:
    print "Warning: winsound not found; will try using pyo/pyaudio"
    winSoundLoaded=False
    
try:
    import pyo
    print "Attempting to use pyo for sounds"
    prefs.general['audioLib'] = ['pyo']
    prefs.general['audioDriver'] = ['ASIO']
except:
    print 'could not load pyo'
    
from psychopy import sound,core,visual
print sound.Sound




if prefs.general['audioLib'][0] == 'pyo':
    print 'initializing pyo to 48000'
    sound.init(48000,buffer=128)
    print 'Using %s(with %s) for sounds' %(sound.audioLib, sound.audioDriver)

from psychopy import core,logging,event,visual,data,gui,misc
import glob,os,random,sys,gc,time,hashlib,subprocess
from math import *

def loadFileSounds(directory,extension,fileType,win='',whichFiles='*',stimList=[]):
	""" Load all the pics and sounds"""
	path = os.getcwd() #set path to current directory
	if isinstance(extension,list):
		fileList = []
		for curExtension in extension:
			fileList.extend(glob.glob(os.path.join(path,directory,whichFiles+curExtension)))
	else:
		fileList = glob.glob(os.path.join(path,directory,whichFiles+extension))
	fileMatrix = {} #initialize fileMatrix  as a dict because it'll be accessed by picture names, cound names, whatver
	for num,curFile in enumerate(fileList):
		fullPath = curFile
		fullFileName = os.path.basename(fullPath)
		stimFile = os.path.splitext(fullFileName)[0]
		if fileType=="sound":
			soundRef = sound.Sound(fullPath)
			fileMatrix[stimFile] = ((soundRef))
		elif fileType=="winSound":
			soundRef = open(fullPath,"rb").read()
			fileMatrix[stimFile] = ((soundRef))
			fileMatrix[stimFile+'-path'] = fullPath #this allows asynchronous playing in winSound.

	#check 
	if stimList and set(fileMatrix.keys()).intersection(stimList) != set(stimList):
		popupError(str(set(stimList).difference(fileMatrix.keys())) + " does not exist in " + path+'\\'+directory) 
	return fileMatrix

def playAndWait(sound,soundPath='',winSound=False,waitFor=-1):
	"""Sound (other than winSound) runs on a separate thread. Waitfor controls how long to pause before resuming. -1 for length of sound"""
	if not winSoundLoaded:
		winSound=False
	if prefs.general['audioLib'] == ['pygame']:
                #default to using winsound
                winSound=True
	if winSound:
                print 'using winsound to play sound'
		if waitFor != 0:
			winsound.PlaySound(sound,winsound.SND_MEMORY)
		else: #playing asynchronously - need to load the path.
			if soundPath:
				winsound.PlaySound(soundPath, winsound.SND_FILENAME|winsound.SND_ASYNC)
			else:
				sys.exit("sound path not provided to playAndWait")
		return
	else:		
		if waitFor<0:
			waitDurationInSecs = sound.getDuration()
		elif waitFor>0:
			waitDurationInSecs = waitFor
		else:
			waitDurationInSecs=0
		
		if waitDurationInSecs>0:
			sound.play()
			core.wait(waitDurationInSecs)
			sound.stop()
			return
		else:
			sound.play()
			print 'returning right away'
			return
	
def popupError(text):
	errorDlg = gui.Dlg(title="Error", pos=(200,400))
	errorDlg.addText('Error: '+text, color='Red')
	errorDlg.show()