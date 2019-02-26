# abbiamo il json , lo score, e le manipolazioni
# dobbiamo raggruppare per -1 e per i probe che non si trovano nel json

import csv
import json
from parse import *
import sys
import argparse

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
    if A != None:
        for i in range(len(A)):
            print(A[i])
    else:
        print('None')

def sortScoreMatrix(matrix):
	tmpRows = []
	for i in range(len(matrix)):
		for k in range(i,len(matrix)):
			if matrix[i][1] < matrix[k][1]:
				tmpRows = matrix[i]
				matrix[i] = matrix[k]
				matrix[k] = tmpRows
				tmpRows = []
	return matrix


def createJsonProbeHistory(probePath, journalPath, operationsPath):
    A = CSVreader(probePath)
    # creo il bigArray
    pastValue = A[1]
    Operations = []
    k = 0
    B = []
    bigArray = []

    for i in range(1, len(A)):
        currentValue = A[i]
        if currentValue[0] == pastValue[0]:
            B.append(currentValue)
        else:
            bigArray.append(B)
            B = []
            B.append(currentValue)  # risolve il problema che non printa la 1°
        pastValue = currentValue

    # ordino secondo Sequence che è la quarta posizione della tabella
    tmpRows = []
    for i in range(len(bigArray)):
        for j in range(len(bigArray[i])):
            for k in range(j, len(bigArray[i])):
                if bigArray[i][j][4] < bigArray[i][k][4]:
                    tmpRows = bigArray[i][j]
                    bigArray[i][j] = bigArray[i][k]
                    bigArray[i][k] = tmpRows
                    tmpRows = []

    # confronto con l'altro csv per stampare l' Operation.  Inserisco tutto dentro C
    B = CSVreader(journalPath)
    C = []
    C2 = []
    tmpOP = []
    for i in range(len(bigArray)):
        for j in range(len(bigArray[i])):
            for k in range(len(B)):
                if (bigArray[i][j][1] == B[k][0]) and (bigArray[i][j][2] == B[k][1]) and (
                (bigArray[i][j][3] == B[k][2])):
                    # print(B[k][0],B[k][3],B[k][5],B[k][6])
                    tmp = [bigArray[i][j][0], B[k][3], B[k][5], B[k][6], ""]
                    tmpOP.append([bigArray[i][j][0], B[k][3], B[k][5], B[k][6], ""])
                    C.append(tmp)
        C2.append(tmpOP)
        tmpOP = []

    # apro il JSON e inserisco la descrizione dentro l'array C.
    with open(operationsPath) as f:
        data = json.load(f)
    # pprint(data)  #stampa tutto
    # print(data.keys()) # stampa tutte le keys principali
    # print(data['operations'][0].keys()) # stampa tutte le keys di operations[0]
    # print(data['operations'][0]['name'])  #stampa il valore della key name dentro operations[0]
    # print(len(data['operations'])) #stampa il numero di operation presenti in operations

    for i in range(len(C2)):
        for k in range(len(C2[i])):
            for j in range(len(data['operations'])):
                if C2[i][k][1] == data['operations'][j]['name']:
                    C2[i][k][4] = data['operations'][j]['description']
                # print(i, B[k][3], B[k][5], B[k][6], B[k][7])

    # Creo un file JSON
    totalProbes = []
    probes = {}
    tmpOperations = {}
    for i in range(len(C2)):
        probeOperations = []
        for j in range(len(C2[i])):
            tmpOperations = {
                "name": C2[i][j][1],
                "purpose": C2[i][j][2],
                "operationArgument": C2[i][j][3],
                "description": C2[i][j][4]
            }
            probeOperations.append(tmpOperations)

        probes = {

            "probeID": C2[i][0][0],
            "operations": probeOperations
        }
        totalProbes.append(probes)

    probesFile = {

        "probesFileID": totalProbes
    }
    with open('./probeHistory.json', 'w') as fp:
        json.dump(probesFile, fp, indent=4, ensure_ascii=False)

    print('JSON file has been created')


def manipulation_list(finalScorePath, opHistoryPath, cameraPath, allOperationsPath, valore_soglia, valore_optout):
    # finalScore.csv
    scoreMatrix = CSVreader(finalScorePath)
    scoreMatrix.remove(scoreMatrix[0])  # Rimuovo l'intestazione
    # probeHistory.json

    # Leggo csv ManipReference
    camera = CSVreader(cameraPath)
    camera.remove(camera[0])  # Rimuovo l'intestazione

    # Leggo le probe history
    with open(opHistoryPath) as f:
        opHistory = json.load(f)

    # Matrice contenente: ProbeID,score=valore_optout
    scoreMatrix_opt = []
    # Matrice contenente ProbeID,score!= valore_opyout
    scoreMatrix_no_opt = []
    # Matrice contenente i ProbeID che non si trovano nel json
    noJSON = []
    tmp = []
    count = 0
    match = False
    for i in range(len(scoreMatrix)):
        for j in range(len(opHistory['probesFileID'])):
            if scoreMatrix[i][0] == opHistory['probesFileID'][j]['probeID']:
                match = True
                if scoreMatrix[i][3] == str(valore_optout):
                    tmp.append(scoreMatrix[i][0])  #Probe
                    tmp.append(scoreMatrix[i][1])  #Camera
                    tmp.append(scoreMatrix[i][3])  #Score
                    scoreMatrix_opt.append(tmp)  # Probe|Camera|Score
                    tmp = []
                else:
                    tmp.append(scoreMatrix[i][0])  #Probe
                    tmp.append(scoreMatrix[i][1])  #Camera
                    tmp.append(scoreMatrix[i][3])  #Score
                    scoreMatrix_no_opt.append(tmp)  # Probe|Camera|Score
                    tmp = []

        if match == False:
            count = count + 1
            tmp.append(scoreMatrix[i][0])  #Probe
            tmp.append(scoreMatrix[i][1])  #Camera
            tmp.append(scoreMatrix[i][3])  #Score
            noJSON.append(tmp)  # Probe|Camera|Score
            tmp = []
        match = False

    # Matrice globale contente: ProbeID,score
    global_score = scoreMatrix_opt + scoreMatrix_no_opt + noJSON
    print('Numero di ProbeID nel CSV score: ', len(scoreMatrix))
    print('Numero di ProbeID nel JSON: ', len(opHistory['probesFileID']))
    print("")
    print('Numero di ProbeID che matchano nel JSON: ', len(scoreMatrix_opt) + len(scoreMatrix_no_opt))
    print('Numero di ProbeID non trovati nel JSON: ', len(noJSON))
    print("")

    # scoreMatrix_one è una matrice contenente: ProbeID,Camera,score=-1,isManipulated/notManipulated raggruppata per Y(yes is manipulated)
    X = []
    Y = []
    for i in range(len(scoreMatrix_opt)):
        for j in range(len(camera)):
            if ((scoreMatrix_opt[i][0] == camera[j][1]) and (scoreMatrix_opt[i][1]) == camera[j][3]):
                tmp.append(scoreMatrix_opt[i][0])
                tmp.append(scoreMatrix_opt[i][1])
                tmp.append(scoreMatrix_opt[i][2])
                tmp.append(camera[j][5])
                tmp.append(camera[j][2].split(".", 1)[1])
                if (camera[j][5]) == 'Y':
                    X.append(tmp)
                else:
                    Y.append(tmp)
                tmp = []
    scoreMatrix_opt = X + Y

    # scoreMatrix_no_opt è una matrice contenente: ProbeID,Camera,score!=-1,isManipulated/notManipulated raggruppata per Y(yes is manipulated)
    X = []
    Y = []
    for i in range(len(scoreMatrix_no_opt)):
        for j in range(len(camera)):
            if ((scoreMatrix_no_opt[i][0] == camera[j][1]) and (scoreMatrix_no_opt[i][1]) == camera[j][3]):
                tmp.append(scoreMatrix_no_opt[i][0])
                tmp.append(scoreMatrix_no_opt[i][1])
                tmp.append(scoreMatrix_no_opt[i][2])
                tmp.append(camera[j][5])
                tmp.append(camera[j][2].split(".", 1)[1])
                if (camera[j][5]) == 'Y':
                    X.append(tmp)
                else:
                    Y.append(tmp)
                tmp = []
    scoreMatrix_no_opt = X + Y

    # ANALISI di scoreMatrix_no_opt
    MATCHED = []
    NOMATCHED = []
    for i in range(len(scoreMatrix_no_opt)):
        if (float(scoreMatrix_no_opt[i][2]) >= valore_soglia):
            MATCHED.append(scoreMatrix_no_opt[i])
        else:
            NOMATCHED.append(scoreMatrix_no_opt[i])


    '''Conteggio ricorrenza operazioni in scoreMatrix_one, scoreMatrix_no_one_matched, scoreMatrix_no_one_no_matched'''
    tmp = []
    scoreOperations_one = []
    for i in range(len(scoreMatrix_opt)):
        for j in range(len(opHistory['probesFileID'])):
            if scoreMatrix_opt[i][0] == opHistory['probesFileID'][j]['probeID']:
                tmp.append(scoreMatrix_opt[i][0])
                tmp.append(scoreMatrix_opt[i][1])
                tmp.append(scoreMatrix_opt[i][2])
                tmp.append(scoreMatrix_opt[i][3])
                tmp.append(opHistory['probesFileID'][j]['operations'])
                scoreOperations_one.append(tmp)
                tmp = []

    tmp = []
    scoreOperations_no_one_matched = []
    for i in range(len(MATCHED)):
        for j in range(len(opHistory['probesFileID'])):
            if MATCHED[i][0] == opHistory['probesFileID'][j]['probeID']:
                tmp.append(MATCHED[i][0])
                tmp.append(MATCHED[i][1])
                tmp.append(MATCHED[i][2])
                tmp.append(MATCHED[i][3])
                tmp.append(opHistory['probesFileID'][j]['operations'])
                scoreOperations_no_one_matched.append(tmp)
                tmp = []

    tmp = []
    scoreOperations_no_one_no_matched = []
    for i in range(len(NOMATCHED)):
        for j in range(len(opHistory['probesFileID'])):
            if NOMATCHED[i][0] == opHistory['probesFileID'][j]['probeID']:
                tmp.append(NOMATCHED[i][0])
                tmp.append(NOMATCHED[i][1])
                tmp.append(NOMATCHED[i][2])
                tmp.append(NOMATCHED[i][3])
                tmp.append(opHistory['probesFileID'][j]['operations'])
                scoreOperations_no_one_no_matched.append(tmp)
                tmp = []

    countOp = 0
    tmp = []
    repeatOp_matched = []
    with open(allOperationsPath) as f:
        data2 = json.load(f)
    # numero di volte in cui le operazioni si ripetono nelle matrici
    for k in range(len(data2['operations'])):
        for i in range(len(scoreOperations_no_one_matched)):
            for j in range(len(scoreOperations_no_one_matched[i][4])):
                if data2['operations'][k]['name'] == scoreOperations_no_one_matched[i][4][j]['name']:
                    countOp = countOp + 1
                    break
        if countOp > 0:
            tmp.append(data2['operations'][k]['name'])
            tmp.append(countOp)
            repeatOp_matched.append(tmp)
        countOp = 0
        tmp = []

    tmp = []
    countOp = 0
    repeatOp_noMatched = []
    for k in range(len(data2['operations'])):
        for i in range(len(scoreOperations_no_one_no_matched)):
            for j in range(len(scoreOperations_no_one_no_matched[i][4])):
                if data2['operations'][k]['name'] == scoreOperations_no_one_no_matched[i][4][j]['name']:
                    countOp = countOp + 1
                    break
        if countOp > 0:
            tmp.append(data2['operations'][k]['name'])
            tmp.append(countOp)
            repeatOp_noMatched.append(tmp)
        countOp = 0
        tmp = []

    tmp = []
    countOp = 0
    repeatOp_one = []
    # numero di volte in cui le operazioni si ripetono nelle matrici
    for k in range(len(data2['operations'])):
        for i in range(len(scoreOperations_one)):
            for j in range(len(scoreOperations_one[i][4])):
                if data2['operations'][k]['name'] == scoreOperations_one[i][4][j]['name']:
                    countOp = countOp + 1
                    break
        if countOp > 0:
            tmp.append(data2['operations'][k]['name'])
            tmp.append(countOp)
            repeatOp_one.append(tmp)
        countOp = 0
        tmp = []

    print('')
    repeatOp_oneSorted = sortScoreMatrix(repeatOp_one)
    repeatOp_no_MatchedSorted = sortScoreMatrix(repeatOp_noMatched)
    repeatOp_matchedSorted = sortScoreMatrix(repeatOp_matched)
    print('')
    print('score =',valore_optout)
    printInColumn(repeatOp_oneSorted)
    print("")
    print('score <', valore_soglia)
    printInColumn(repeatOp_no_MatchedSorted)
    print("")
    print('score >=', valore_soglia)
    printInColumn(repeatOp_matchedSorted)

def scoreFilter1(finalScorePath, opHistoryPath, score, opFilter, operator='equal', score2 = None):
    # init >> Faccio i join tra le probe nello score del csv e le probe presenti nell'history

    # finalScore.csv
    scoreMatrix = CSVreader(finalScorePath)
    scoreMatrix.remove(scoreMatrix[0])  # Rimuovo l'intestazione
    # probeHistory.json
    with open(opHistoryPath) as f:
        opHistory = json.load(f)

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
                    if (opFilter == tmpMatrix[i][oH][j]['name']) and (firstMatched == False):
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
        print('Error')
        return 0


def scoreFilter2(finalScorePath, opHistoryPath, score, opFilter, operator='equal', maxPreviousOp=0, score2 = None):
    # finalScore.csv
    scoreMatrix = CSVreader(finalScorePath)
    scoreMatrix.remove(scoreMatrix[0])  # Rimuovo l'intestazione
    # probeHistory.json
    with open(opHistoryPath) as f:
        opHistory = json.load(f)

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

    elif (operator == 'range') and (score >= 0) and (score2 != None) and (score2 >= 0):
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



def get_parser():
    parser = argparse.ArgumentParser(description="")

    subparser = parser.add_subparsers(dest='subcommand')

    # subcommand create-json-probe-history
    history_parser = subparser.add_parser('create-json-probe-history', help='Create a json file containing the probe history')
    history_parser.add_argument("-p", "--probejournaljoin", required=True, help="insert probejournalname path")
    history_parser.add_argument("-j", "--journalmask", required=True, help="insert journalmask path")
    history_parser.add_argument("-o", "--operations", required=True, help="insert json file contains all operations")

    # subcommand manipulation-name
    manipulation_parser = subparser.add_parser('manipulation-list', help='List all possible manipulations')
    manipulation_parser.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    manipulation_parser.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    manipulation_parser.add_argument("-cp", "--camerapath", required=True, help="path of camera reference")
    manipulation_parser.add_argument("-o", "--operations", required=True, help="insert json file contains all operations")
    manipulation_parser.add_argument("-vs", "--valoresoglia",type=int, required=True, help="valore di soglia")
    manipulation_parser.add_argument("-vo", "--valoreoptout", type=int, required=True, help="valore di optout")

    # subcommand filter1
    filter1_parser = subparser.add_parser('filter1', help='Evaluate scores ...')
    filter1_parser.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    filter1_parser.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    filter1_parser.add_argument("-s", "--score", required=True, type=int, help="insert score")
    filter1_parser.add_argument("-op", "--operator", required=True, help="insert operator like over,under,equal,range")
    filter1_parser.add_argument("-s2", "--score2", required=False, type=int, help="insert score2")
    filter1_parser.add_argument("-o", "--operation", required=True, help="insert operation filter")

    # subcommand filter2
    filter2_parser = subparser.add_parser('filter2', help='Evaluate scores ...')
    filter2_parser.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    filter2_parser.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    filter2_parser.add_argument("-s", "--score", required=True, type=int, help="insert score")
    filter2_parser.add_argument("-op", "--operator", required=True, help="insert operator like over,under,equal,range")
    filter2_parser.add_argument("-s2", "--score2", required=False , type=int, help="insert score2")
    filter2_parser.add_argument("-o", "--operation", required=True, help="insert operation filter")
    filter2_parser.add_argument("-po", "--prevop", type=int, required=True, help="insert preview operations")

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.subcommand == 'create-json-probe-history':
        createJsonProbeHistory(probePath=args.probejournaljoin, journalPath=args.journalmask, operationsPath=args.operations)
    elif args.subcommand == 'manipulation-list':
        manipulation_list(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, cameraPath=args.camerapath, allOperationsPath=args.operations, valore_soglia=args.valoresoglia, valore_optout=args.valoreoptout)
    elif args.subcommand == 'filter1':
        result = scoreFilter1(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, score=args.score, opFilter=args.operation, operator=args.operator, score2 = args.score2)
        printInColumn(result)
    elif args.subcommand == 'filter2':
        result = scoreFilter2(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, score=args.score, opFilter=args.operation, operator=args.operator, maxPreviousOp=args.prevop, score2 = args.score2)
        printInColumn(result)


def mainInterattivo():
    print('Which operation do you want use?')
    print('1) Create json file containing probe history')
    print('2) Manipulation list')
    print('3) Filter1')
    print('4) Filter2')
    print('5) Exit')

    mainScelta = int(input())

    if (mainScelta < 1) or (mainScelta > 4):
        sys.exit()

    elif (mainScelta == 1):
        print("Enter the path of probejournaljoin :")
        probePath = input().strip()

        print("Enter the path of journalmask :")
        journalPath = input().strip()

        print("Enter the path of operations :")
        operationsPath = input().strip()

        createJsonProbeHistory(probePath=probePath, journalPath=journalPath, operationsPath=operationsPath)

    elif (mainScelta == 2):
        print('boa fallo!!')

    elif (mainScelta == 3) or (mainScelta == 4):
        # score.csv
        print('Insert score path: ')
        finalScorePath = input().strip()

        # probeHistory.json
        print('Insert probe history path: ')
        opHistoryPath = input().strip()

        while (True):
            # opzione di score
            print('Choose score options:')
            print('1) score = [valore]')
            print('2) score >= [valore]')
            print('3) score < [valore]')
            print('4) range[val1,val2]')
            print('5) Exit')
            sceltaOpzione = input()

            operator = int(sceltaOpzione[0])  # operator=1 equal , operator=2 >=, operator=3  <, operator=4 range
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
                score = parse(sceltaOpzione[0] + '[' + '{}' + ',' + '{}' + ']', sceltaOpzione)[0]
                score2 = parse(sceltaOpzione[0] + '[' + '{}' + ',' + '{}' + ']', sceltaOpzione)[1]
                score = int(score)
                score2 = int(score2)
            else:
                sys.exit()

            # inserimento operazione
            print('Insert operation name: ')
            opFilter = input()
    
            if (mainScelta == 3):
                if operator == 'range':
                    result = scoreFilter1(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score = score, opFilter=opFilter, operator=operator, score2 = score2)
                    printInColumn(result)
                else:
                    result = scoreFilter1(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score, opFilter=opFilter, operator=operator)
                    printInColumn(result)

            if (mainScelta == 4):
                # inserimento numero di operazioni precedenti
                print('Insert number of previews operations to view: ')
                prevOp = int(input())
                if operator == 'range':
                    result = scoreFilter2(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score, opFilter=opFilter, operator=operator, maxPreviousOp=prevOp, score2=score2)
                    printInColumn(result)
                else:
                    result = scoreFilter2(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score, opFilter=opFilter, operator=operator, maxPreviousOp=prevOp)
                    printInColumn(result)



if __name__ == '__main__':
    if sys.argv[1:] != []:
        main()
    else:
        mainInterattivo()

