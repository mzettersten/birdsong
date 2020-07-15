import csv
import random
import numpy as np

#define function to shuffle and generate trial list .csv files

def main(subjCode, seed,shuffleNum=10,trialsPerBlock=2):
    seed=int(seed)
    separator=","
    
    ####shuffle and create trial list####
    #read in trial list
    filename='Bird_trialList.csv'
    
    trialList=[]
    with open(filename, 'rU') as csvfile:
        reader=csv.reader(csvfile, delimiter=",")
        for row in reader:
            trialList.append(row) 
            
    shuffledTrialList = []
    boxList = ["wp1","wp2","wp3","wp4","wp5","wp6","wp7","wp8","wp9","wp10","wp11","wp12"]
    
    #shuffle boxes
    np.random.seed(seed)
    for i in range(shuffleNum):
        np.random.shuffle(boxList)
        
    #break into six blocks
    shuffledTrialList=[trialList[0]+["box"]]
    blockTrials=[]
    blockTrials1=trialList[1:trialsPerBlock+1]
    blockTrials2=trialList[trialsPerBlock+1:2*trialsPerBlock+1]
    blockTrials3=trialList[2*trialsPerBlock+1:3*trialsPerBlock+1]
    blockTrials4=trialList[3*trialsPerBlock+1:4*trialsPerBlock+1]
    blockTrials5=trialList[4*trialsPerBlock+1:5*trialsPerBlock+1]
    blockTrials6=trialList[5*trialsPerBlock+1:]
    
    #shuffle and expand block list while checking for repeated items
    #block 1
    curBlock = shuffleBlock(blockTrials1,shuffleNum)
    blockTrials=blockTrials + curBlock
    
    #block 2
    curBlock = shuffleBlock(blockTrials2,shuffleNum)
    blockTrials=blockTrials + curBlock
    
    #block 3
    curBlock = shuffleBlock(blockTrials3,shuffleNum)
    blockTrials=blockTrials + curBlock
    
    #block 4
    curBlock = shuffleBlock(blockTrials4,shuffleNum)
    blockTrials=blockTrials + curBlock
    
    #block 5
    curBlock = shuffleBlock(blockTrials5,shuffleNum)
    blockTrials=blockTrials + curBlock
    
    #block 6
    curBlock = shuffleBlock(blockTrials6,shuffleNum)
    blockTrials=blockTrials + curBlock
            
    #add a random box to each trial
    #then add to trial list
    i=0
    for trial in blockTrials:
        trial.append(boxList[i])
        i+=1
        
        #add to trial list
        shuffledTrialList+=[trial]
    
    
        
                    
    #write shuffled list to csv trial list
    trialFile=open('trialLists/Bird_trialList_'+subjCode+'_'+str(seed)+'.csv', 'w')
    for trial in shuffledTrialList:
        trial = map(str,trial)
        trial = separator.join(trial)
        print >>trialFile, trial
    trialFile.close()
   
def shuffleBlock(myList,shuffleNum):
    for i in range(shuffleNum):
        np.random.shuffle(myList)
    return myList

            
    
    
    
  
