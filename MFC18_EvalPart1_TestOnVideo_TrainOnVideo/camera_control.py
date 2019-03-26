import csv
import json
import numpy as np
from parse import *
import sys
import argparse
from argparse import RawTextHelpFormatter

# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np

def CSVreader(path):
    with open(path) as f:
        reader = csv.reader(f, delimiter='|', quoting=csv.QUOTE_NONE)
        rows = []
        for row in reader:
            rows.append(row)
    return rows


def printInColumn(A):
    if (A is None) or (A == '[]') or (A == []) or (A == ''):
        print('None')
    else:
        for i in range(len(A)):
            print(A[i])

def sortScoreMatrix(matrix):
    for i in range(len(matrix)):
        for k in range(i,len(matrix)):
            if matrix[i][1] < matrix[k][1]:
                tmpRows = matrix[i]
                matrix[i] = matrix[k]
                matrix[k] = tmpRows
    return matrix
def countcamera(V):
    flag = False
    tmp = []
    cameraOccurrence = []
    for i in range(len(V)):
    	for j in range(len(cameraOccurrence)):
    		if V[i] == cameraOccurrence[j][0]:
    			flag = True
    	if flag == False:	
    		count = V.count(V[i])
    		tmp.append(V[i])
    		tmp.append((count/len(V))*100)
    		cameraOccurrence.append(tmp)
    	tmp = []
    	flag = False
    cameraOccurrence = sortScoreMatrix(cameraOccurrence)
    printInColumn(cameraOccurrence)

def cameraControl(finalScorePath,opHistoryPath):
    score = CSVreader(finalScorePath)
    score.remove(score[0])
    with open(opHistoryPath) as f:
        history = json.load(f)

    M = []
    for i in range(len(history['probesFileID'])):
        for j in range(len(score)):
            if history['probesFileID'][i]['probeID'] == score[j][0]:
                tmp=[]
                tmp=[score[j][0],score[j][1],score[j][3]]
                M.append(tmp)
    equal1 = []
    under50 = []
    over50 = []
    for i in range(len(M)):
        if float(M[i][2]) == -1:
            equal1.append(M[i][1])
        elif float(M[i][2]) < 50 and float(M[i][2])!= -1 :
            under50.append(M[i][1])
        elif float(M[i][2]) >= 50:
            over50.append(M[i][1])
    countcamera(equal1)
    print("\n under50")
    countcamera(under50)
    print("\n over50")
    countcamera(over50)
    print("")

scorePath = '/Users/andreasimioni/Desktop/Image-Processing-and-Security-master-4/MFC18_EvalPart1_TestOnVideo_TrainOnVideo/FinalScores/UnifiPRNUTime_1_CameraVideoVideo.csv'
opHistoryPath =  '/Users/andreasimioni/Desktop/Image-Processing-and-Security-master-4/MFC18_EvalPart1_TestOnVideo_TrainOnVideo/probeHistory.json'
cameraControl(scorePath,opHistoryPath)