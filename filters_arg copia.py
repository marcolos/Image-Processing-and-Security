# abbiamo il json , lo score, e le manipolazioni
# dobbiamo raggruppare per -1 e per i probe che non si trovano nel json

import csv
import json
import re
from parse import *
import sys
import argparse

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
    if A != None:
        for i in range(len(A)):
            print(A[i])
    else:
        print('None')


def scoreFilter1(scoreMatrix, opHistory, score, opFilter, operator='equal',score2 = None):
    # init >> Faccio i join tra le probe nello score del csv e le probe presenti nell'history
    tmp = []
    result = []
    tmpMatrix = []
    for i in range(len(scoreMatrix)):
        for j in range(len(opHistory['probesFileID'])):
            if scoreMatrix[i][0] == opHistory['probesFileID'][j]['probeID']:
                tmp.append(scoreMatrix[i][0])  # ProbeID
                tmp.append(scoreMatrix[i][1])  # Camera
                tmp.append(opFilter)  # opFiltro
                tmp.append(scoreMatrix[i][3])  # Score
                tmp.append(opHistory['probesFileID'][j]['operations'])  # [opHistory]
                tmpMatrix.append(tmp)  # ProbeID|Camera|opFiltro|Score|[opHistory]
                tmp = []

    p = 0
    c = 1
    oF = 2
    s = 3
    oH = 4
    # end >> Ho costruito tmpMatrix ProbeID|Camera|opFiltro|Score|[opHistory]

    tmp = []
    tmpMatrix2 = []
    countOperations = 0
    objPosition = -1
    firstMatched = False

    if (score != -1) and (score < 0):
        print('errore,valore inserito non corretto')
        return 0

    elif (operator == 'equal'):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][s]) == score:  # Score ==-1
                for j in range(len(tmpMatrix[i][oH])):  # [opHistory]
                    countOperations = countOperations + 1
                    if (opFilter == tmpMatrix[i][oH][j]['name']) and (firstMatched == False):
                        objPosition = countOperations
                        firstMatched = True
                tmp.append(tmpMatrix[i][p])  # ProbeID
                tmp.append(tmpMatrix[i][c])  # Camera
                tmp.append(tmpMatrix[i][oF])  # opFiltro
                # tmp.append(tmpMatrix[i][s])  #Score
                tmp.append(objPosition)  # posOpFilter
                tmp.append(countOperations)  # numOp
                tmpMatrix2.append(tmp)  # ProbeID|Camera|opFilter|posOpFilter|numOp
                tmp = []
            firstMatched = False
            objPosition = -1
            countOperations = 0
        for i in range(len(tmpMatrix2)):  # se opFilter non è presente opFilter=-1
            if tmpMatrix2[i][3] != -1:  # opFilter
                result.append(tmpMatrix2[i])
        return result


    elif (operator) == 'over' and (score == -1):
        print('ritenta')
        return 0


    elif (operator == 'over') and (score >= 0):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][s]) >= score:  # Score
                for j in range(len(tmpMatrix[i][oH])):
                    countOperations = countOperations + 1
                    if (opFilter == tmpMatrix[i][oH][j]['name']) and (firstMatched == False):
                        objPosition = countOperations
                        firstMatched = True
                tmp.append(tmpMatrix[i][p])  # ProbeID
                tmp.append(tmpMatrix[i][c])  # Camera
                tmp.append(tmpMatrix[i][oF])  # opFiltro
                # tmp.append(tmpMatrix[i][s])  #Score
                tmp.append(objPosition)  # posOpFilter
                tmp.append(countOperations)  # numOp
                tmpMatrix2.append(tmp)  # ProbeID|Camera|opFilter|posOpFilter|numOp
                tmp = []
            firstMatched = False
            objPosition = -1
            countOperations = 0
        for i in range(len(tmpMatrix2)):
            if tmpMatrix2[i][3] != -1:
                result.append(tmpMatrix2[i])
        return result

    elif (operator == 'under') and (score >= 0):
        for i in range(len(tmpMatrix)):
            if (float(tmpMatrix[i][s]) < score) and (float(tmpMatrix[i][s]) != -1):
                for j in range(len(tmpMatrix[i][oH])):
                    countOperations = countOperations + 1
                    if (opFilter == tmpMatrix[i][oH][j]['name']) and (firstMatched == False):
                        objPosition = countOperations
                        firstMatched = True
                tmp.append(tmpMatrix[i][p])  # ProbeID
                tmp.append(tmpMatrix[i][c])  # Camera
                tmp.append(tmpMatrix[i][oF])  # opFiltro
                # tmp.append(tmpMatrix[i][s])  #Score
                tmp.append(objPosition)  # posOpFilter
                tmp.append(countOperations)  # numOp
                tmpMatrix2.append(tmp)  # ProbeID|Camera|opFilter|posOpFilter|numOp
                tmp = []
            firstMatched = False
            objPosition = -1
            countOperations = 0
        for i in range(len(tmpMatrix2)):
            if tmpMatrix2[i][3] != -1:
                result.append(tmpMatrix2[i])
        return result

    
    elif (operator == 'range') and (score >= 0) and (score2 != None) and (score2 >= 0):
        for i in range(len(tmpMatrix)):
            if (float(tmpMatrix[i][s]) >= score) and (float(tmpMatrix[i][s]) <= score2):
                for j in range(len(tmpMatrix[i][oH])):
                    countOperations = countOperations + 1
                    if (idOperation == tmpMatrix[i][oH][j]['name']) and (firstMatched == False):
                        objPosition = countOperations
                        firstMatched = True
                tmp.append(tmpMatrix[i][p])
                tmp.append(tmpMatrix[i][c])
                tmp.append(tmpMatrix[i][oF])
                tmp.append(objPosition)
                tmp.append(countOperations)
                tmpMatrix2.append(tmp)
                tmp = []
            firstMatched = False
            objPosition = -1
            countOperations = 0
        for i in range(len(tmpMatrix2)):
            if tmpMatrix2[i][3] != -1:
                result.append(tmpMatrix2[i])
        return result

    elif (operator == 'range') and (score == None or score < 0):
        print('errore,inserire parametri corretti')
        return 0


    elif (operator == 'under') and (score == -1):
        print('Errore,inserire parametri corretti')
        return 0


def scoreFilter2(scoreMatrix, opHistory, score, opFilter, operator='equal', maxPreviousOp=0,score2 = None):
    tmp = []
    result = []
    tmpMatrix = []
    match = False
    for i in range(len(scoreMatrix)):
        for j in range(len(opHistory['probesFileID'])):
            if scoreMatrix[i][0] == opHistory['probesFileID'][j]['probeID']:
                for k in range(len(opHistory['probesFileID'][j]['operations'])):
                    if opFilter == opHistory['probesFileID'][j]['operations'][k]['name']:
                        match = True
                        break
                if match == True:
                    tmp.append(scoreMatrix[i][0])
                    tmp.append(scoreMatrix[i][1])
                    tmp.append(scoreMatrix[i][3])
                    tmp.append(opHistory['probesFileID'][j]['operations'])
                    tmpMatrix.append(tmp)
                tmp = []
                match = False

    tmp = []
    tmpOp = []
    countOperations = 0

    if (score != -1) and (score < 0):
        print('errore,valore inserito non corretto')
        return 0

    elif (operator == 'equal'):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][2]) == score:
                tmp.append(tmpMatrix[i][0])
                for j in range(len(tmpMatrix[i][3])):
                    if tmpMatrix[i][3][j]['name'] != opFilter:
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

    elif (operator == 'over') and (score == -1):
        print('errore,inserire parametri corretti')
        return 0

    elif (operator == 'over') and (score >= 0):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][2]) >= score:
                tmp.append(tmpMatrix[i][0])
                for j in range(len(tmpMatrix[i][3])):
                    if tmpMatrix[i][3][j]['name'] != opFilter:
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

    elif (operator == 'under') and (score >= 0):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][2]) < score and (float(tmpMatrix[i][2]) != -1):
                tmp.append(tmpMatrix[i][0])
                for j in range(len(tmpMatrix[i][3])):
                    if tmpMatrix[i][3][j]['name'] != opFilter:
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

    elif (function == 'range') and (score >= 0) and (score2 != None) and (score2 >= 0):
        for i in range(len(tmpMatrix)):
            if (float(tmpMatrix[i][2]) >= score) and (float(tmpMatrix[i][2]) <= score2):
                tmp.append(tmpMatrix[i][0])
                for j in range(len(tmpMatrix[i][3])):
                    if tmpMatrix[i][3][j]['name'] != opFilter:
                        countOperations = countOperations + 1
                        if countOperations <= maxPreviousOp:
                            tmpOp.append(tmpMatrix[i][3][j]['name'])
                    else:
                        break
                tmp.append(tmpOp)
                tmp.append(countOperations)
                tmp.append(tmpMatrix[i][2])
                result.append(tmp)
                tmp = []
                tmpOp = []
                countOperations = 0 


    elif (operator == 'range') and (score == None or score < 0):
        print('errore,inserire parametri corretti')
        return 0


    elif (operator == 'under') and (score == -1):
        print('errore,inserire parametri corretti')
        return 0

    if result != []:
        for i in range(len(result)):
            if float(result[i][2]) == 0:
                result[i][2] = 'First Operation'
        return result


#MAIN
if sys.argv[1:] != []:
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filter",required=True, help="type of filter that you want use: insert 1 to use filter1 or 2 to use filter2")
    ap.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    ap.add_argument("-hp","--probehistory", required=True, help="path of probe history")
    ap.add_argument("-s","--score", required=True, help="insert score")
    ap.add_argument("-op","--operator", required=True, help="insert operator like over,under,equal")
    ap.add_argument("-o","--operation", required=True, help="insert operation filter")
    ap.add_argument("-po", "--prevop", required=False, help="insert preview operations")
    ap.add_argument("-s2","--secondscore",required = False, help = "insert second score")
    args = vars(ap.parse_args())


    #save value from command line
    sceltaFiltro = int(args["filter"])
    sp = args["scorepath"]
    hp = args["probehistory"]
    score = int(args["score"])
    operator = args["operator"]
    opFilter = args["operation"]
    prevOp = int(args['prevop'])
    score2 = int(args["secondscore"])

#Script interattivo
else:
    print('Which filter do you want use?')
    print('1) Filter1')
    print('2) Filter2')
    sceltaFiltro = int(input())

    if (sceltaFiltro < 1) or (sceltaFiltro > 2):
        sys.exit()

    # score.csv
    print('Insert score path: ')
    sp = input().strip()

    # probeHistory.json
    print('Insert probe history path: ')
    hp = input().strip()

    while (True):
        # opzione di score
        print('Choose score options:')
        print('1) score = [valore]')
        print('2) score >= [valore]')
        print('3) score < [valore]')
        print('4) intervall[val1,val2]')
        print('5) Exit')

        sceltaOpzione = input()
        operator = int(sceltaOpzione[0])  # operator=0 equal , #operator=1 >=, #operator=2  <
        if operator == 1:
            operator = 'equal'
            score = parse(sceltaOpzione[0] + '[' + '{}' + ']', sceltaOpzione)[0]
            score = int(score)
        elif operator == 2:
            operator = 'over'
            score = parse(sceltaOpzione[0] + '[' + '{}' + ']', sceltaOpzione)[0]
            score = int(score)
        elif operator == 3:
            operator = 'under'
            score = parse(sceltaOpzione[0] + '[' + '{}' + ']', sceltaOpzione)[0]
            score = int(score)
        elif operator == 4:
            operator = 'range'
            score = parse(sceltaOpzione[0] + '[' + '{}' + ',', sceltaOpzione)[0]
            score2 = parse(sceltaOpzione[0] + ',' + '{}' + ']',sceltaOpzione)[0]
            score = int(score)
            score2 = int(score2)
        else:
            sys.exit()

        # inserimento operazione
        print('Insert operation name: ')
        opFilter = input()

#finalScore.csv
finalScore = CSVreader(sp)
finalScore.remove(finalScore[0])  # Rimuovo l'intestazione

#probeHistory.json
with open(hp) as f:
    opHistory = json.load(f)

print('')
if (sceltaFiltro == 1):
    if operator == 'equal':
        result = scoreFilter1(finalScore, opHistory, score, opFilter=opFilter, operator='equal')
        printInColumn(result)
    if operator == 'over':
        result=scoreFilter1(finalScore, opHistory, score, opFilter=opFilter, operator='over')
        printInColumn(result)
    if  operator == 'under':
        result=scoreFilter1(finalScore, opHistory, score, opFilter=opFilter, operator='under')
        printInColumn(result)
    if operator == 'range':
        result = scoreFilter1(finalScore,opHistory,score,opFilter= opFilter,operator = 'range',score2 = score2)

if (sceltaFiltro == 2):
    if (sys.argv[1:] == []):
        print('Insert number of previews operations to view: ')
        prevOp = int(input())
    if operator == 'equal':
        result=scoreFilter2(finalScore, opHistory, score, opFilter=opFilter, operator='equal', maxPreviousOp=prevOp)
        printInColumn(result)
    if operator == 'over':
        result=scoreFilter2(finalScore, opHistory, score, opFilter=opFilter, operator='over', maxPreviousOp=prevOp)
        printInColumn(result)
    if operator == 'under':
        result=scoreFilter2(finalScore, opHistory, score, opFilter=opFilter, operator='under', maxPreviousOp=prevOp)
        printInColumn(result)
    if operator == 'range':
        result = scoreFilter2(finalScore,opHistory,score, opFilter = opFilter, operator = 'range',maxPreviousOp = prevOp,score2 = score2)
print('')
