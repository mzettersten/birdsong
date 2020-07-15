import csv
import random
import numpy as np

#define function to shuffle and generate trial list .csv files

def main(subjCode, seed,shuffleNum=10,trialsPerBlock=3):
    seed=int(seed)
    separator=","
    trialIDFullList = ['1','2','3']
    
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
        
    #break into four blocks
    shuffledTrialList=[trialList[0]+["box"]]
    blockTrials=[]
    blockTrials1=trialList[1:trialsPerBlock+1]
    blockTrials2=trialList[trialsPerBlock+1:2*trialsPerBlock+1]
    blockTrials3=trialList[2*trialsPerBlock+1:3*trialsPerBlock+1]
    blockTrials4=trialList[3*trialsPerBlock+1:]
    
    #shuffle and expand block list while checking for repeated items
    #block 1
    i=0
    trialIDList1=[]
    trialIDList2=[]
    trialIDList3=[]
    trialIDList4=[]
    while True:
        print 1
        curBlock = shuffleBlock(blockTrials1,shuffleNum)
        temp1=[]
        for i in range(len(curBlock)):
            temp1.append(curBlock[i][1])
        check2Adj = [[[token,token] == temp1[i:i+2] for i in range(len(temp1) - 1)] for token in trialIDFullList]
        check2AdjFlatten = [item for sublist in check2Adj for item in sublist]
        if not any(check2AdjFlatten):
            i+=1
            blockTrials=blockTrials + curBlock
            trialIDList1 = temp1
            break
    #block 2
    while True:
        curBlock = shuffleBlock(blockTrials2,shuffleNum)
        temp2=[]
        for i in range(len(curBlock)):
            temp2.append(curBlock[i][1])
        checkList2 = trialIDList1 + temp2
        check2Adj = [[[token,token] == checkList2[i:i+2] for i in range(len(checkList2) - 1)] for token in trialIDFullList]
        check2AdjFlatten = [item for sublist in check2Adj for item in sublist]
        if not any(check2AdjFlatten):
            blockTrials=blockTrials + curBlock
            trialIDList2 = temp2
            break
    #block 3
    while True:
        curBlock = shuffleBlock(blockTrials3,shuffleNum)
        temp3=[]
        for i in range(len(curBlock)):
            temp3.append(curBlock[i][1])
        checkList3 = trialIDList1 +trialIDList2 + temp3
        check2Adj = [[[token,token] == checkList3[i:i+2] for i in range(len(checkList3) - 1)] for token in trialIDFullList]
        check2AdjFlatten = [item for sublist in check2Adj for item in sublist]
        if not any(check2AdjFlatten):
            blockTrials=blockTrials + curBlock
            trialIDList3 = temp3
            break
    #block 4
    while True:
        curBlock = shuffleBlock(blockTrials4,shuffleNum)
        temp4=[]
        for i in range(len(curBlock)):
            temp4.append(curBlock[i][1])
        checkList4 = trialIDList1 +trialIDList2 + trialIDList3 +temp4
        check2Adj = [[[token,token] == checkList4[i:i+2] for i in range(len(checkList4) - 1)] for token in trialIDFullList]
        check2AdjFlatten = [item for sublist in check2Adj for item in sublist]
        if not any(check2AdjFlatten):
            blockTrials=blockTrials + curBlock
            trialIDList4 = temp4
            break
            
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

            
    
    
    
  
