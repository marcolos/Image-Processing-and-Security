# abbiamo il json , lo score, e le manipolazioni
# dobbiamo raggruppare per -1 e per i probe che non si trovano nel json

import csv
import json


# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# from collections import Counter

def CSVreader(path):
    with open(path) as f:
        reader = csv.reader(f, delimiter='|', quoting=csv.QUOTE_NONE)
        rows = []
        for row in reader:
            rows.append(row)
    return rows


def printInColumn(A):
    for i in range(len(A)):
        print(A[i])


def scoreFilter1(scoreMatrix, operations, score, idOperation, function='null'):
    tmp = []
    result = []
    tmpMatrix = []
    for i in range(len(scoreMatrix)):
        for j in range(len(operations['probesFileID'])):
            if scoreMatrix[i][0] == operations['probesFileID'][j]['probeID']:
                tmp.append(scoreMatrix[i][0])
                tmp.append(scoreMatrix[i][1])
                tmp.append(scoreMatrix[i][3])
                tmp.append(operations['probesFileID'][j]['operations'])
                tmpMatrix.append(tmp)
                tmp = []
    tmp = []
    tmpMatrix2 = []
    countOperations = 0
    objPosition = -1
    firstMatched = False

    if (score != -1) and (score < 0):
        print('errore,valore inserito non corretto')
        return 0

    elif (function == 'null') and (score == -1):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][2]) == -1:
                for j in range(len(tmpMatrix[i][3])):
                    countOperations = countOperations + 1
                    if (idOperation == tmpMatrix[i][3][j]['name']) and (firstMatched == False):
                        objPosition = countOperations
                        firstMatched = True
                tmp.append(tmpMatrix[i][0])
                tmp.append(tmpMatrix[i][1])
                tmp.append(objPosition)
                tmp.append(countOperations)
                tmpMatrix2.append(tmp)
                tmp = []
            firstMatched = False
            objPosition = -1
            countOperations = 0
        for i in range(len(tmpMatrix2)):
            if tmpMatrix2[i][2] != -1:
                result.append(tmpMatrix2[i])
        return result


    elif (function) == 'over' and (score == -1):
        print('dashara ritenta')
        return 0


    elif (function == 'over') and (score >= 0):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][2]) >= score:
                for j in range(len(tmpMatrix[i][3])):
                    countOperations = countOperations + 1
                    if (idOperation == tmpMatrix[i][3][j]['name']) and (firstMatched == False):
                        objPosition = countOperations
                        firstMatched = True
                tmp.append(tmpMatrix[i][0])
                tmp.append(tmpMatrix[i][1])
                tmp.append(objPosition)
                tmp.append(countOperations)
                tmpMatrix2.append(tmp)
                tmp = []
            firstMatched = False
            objPosition = -1
            countOperations = 0
        for i in range(len(tmpMatrix2)):
            if tmpMatrix2[i][2] != -1:
                result.append(tmpMatrix2[i])
        return result

    elif (function == 'under') and (score >= 0):
        for i in range(len(tmpMatrix)):
            if float((tmpMatrix[i][2]) < score) and float((tmpMatrix[i][2]) != -1):
                for j in range(len(tmpMatrix[i][3])):
                    print(tmpMatrix[i][3][j]['name'])
                    countOperations = countOperations + 1
                    if (idOperation == tmpMatrix[i][3][j]['name']) and (firstMatched == False):
                        objPosition = countOperations
                        firstMatched = True
                tmp.append(tmpMatrix[i][0])
                tmp.append(tmpMatrix[i][1])
                tmp.append(objPosition)
                tmp.append(countOperations)
                tmpMatrix2.append(tmp)
                print("")
                tmp = []
            firstMatched = False
            objPosition = -1
            countOperations = 0
        for i in range(len(tmpMatrix2)):
            if tmpMatrix2[i][2] != -1:
                result.append(tmpMatrix2[i])
        return result

    elif (function == 'under') and (score == -1):
        print('Error')
        return 0


def scoreFilter2(scoreMatrix, operations, score, idOperation, function='null', maxPreviousOp=0):
    tmp = []
    result = []
    tmpMatrix = []
    match = False
    for i in range(len(scoreMatrix)):
        for j in range(len(operations['probesFileID'])):
            if scoreMatrix[i][0] == operations['probesFileID'][j]['probeID']:
                for k in range(len(operations['probesFileID'][j]['operations'])):
                    if idOperation == operations['probesFileID'][j]['operations'][k]['name']:
                        match = True
                        break
                if match == True:
                    tmp.append(scoreMatrix[i][0])
                    tmp.append(scoreMatrix[i][1])
                    tmp.append(scoreMatrix[i][3])
                    tmp.append(operations['probesFileID'][j]['operations'])
                    tmpMatrix.append(tmp)
                tmp = []
                match = False

    tmp = []
    tmpOp = []
    countOperations = 0

    if (score != -1) and (score < 0):
        print('errore,valore inserito non corretto')
        return 0

    elif (function == 'null') and (score == -1):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][2]) == -1:
                tmp.append(tmpMatrix[i][0])
                for j in range(len(tmpMatrix[i][3])):
                    if tmpMatrix[i][3][j]['name'] != idOperation:
                        countOperations = countOperations + 1
                        if countOperations <= maxPreviousOp:
                            tmpOp.append(tmpMatrix[i][3][j]['name'])
                    else:
                        break
                tmp.append(tmpOp)
                tmp.append(countOperations)
                result.append(tmp)
                tmp = []
                tmpOp = []
                countOperations = 0

    elif (function == 'over') and (score == -1):
        print('errore,inserire parametri corretti')
        return 0

    elif (function == 'over') and (score >= 0):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][2]) >= score:
                tmp.append(tmpMatrix[i][0])
                for j in range(len(tmpMatrix[i][3])):
                    if tmpMatrix[i][3][j]['name'] != idOperation:
                        countOperations = countOperations + 1
                        if countOperations <= maxPreviousOp:
                            tmpOp.append(tmpMatrix[i][3][j]['name'])
                    else:
                        break
                tmp.append(tmpOp)
                tmp.append(countOperations)
                result.append(tmp)
                tmp = []
                tmpOp = []
                countOperations = 0

    elif (function == 'under') and (score >= 0):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][2]) < score and (float(tmpMatrix[i][2]) != -1):
                tmp.append(tmpMatrix[i][0])
                for j in range(len(tmpMatrix[i][3])):
                    if tmpMatrix[i][3][j]['name'] != idOperation:
                        countOperations = countOperations + 1
                        if countOperations <= maxPreviousOp:
                            tmpOp.append(tmpMatrix[i][3][j]['name'])
                    else:
                        break
                tmp.append(tmpOp)
                tmp.append(countOperations)
                result.append(tmp)
                tmp = []
                tmpOp = []
                countOperations = 0

    elif (function == 'under') and (score == -1):
        print('errore,inserire parametri corretti')
        return 0

    if result != []:
        for i in range(len(result)):
            if float(result[i][2]) == 0:
                result[i][2] = 'First Operation'
        return result


# Leggo json
with open('./myoperations.json') as f:
    data = json.load(f)
# Leggo csv FinalScores
A = CSVreader('./FinalScores/UnifiPRNUTime_1_CameraVideoVideo.csv')
A.remove(A[0])  # Rimuovo l'intestazione
# Leggo csv ManipReference
B = CSVreader('./Reference/MFC18_EvalPart1-camera-ref.csv')
B.remove(B[0])  # Rimuovo l'intestazione
with open('./Reference/operations.json') as f:
    data2 = json.load(f)

score = 50

result1 = scoreFilter1(A, data, score, 'AddAudioSample',function='under')
print(result1)

# result2 = scoreFilter2(A, data, score, 'AddAudioSample', 'null', 2)
# printInColumn(result2)
