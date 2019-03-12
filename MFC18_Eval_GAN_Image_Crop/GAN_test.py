import csv
import json
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

def check(A):
    check = False
    if A != None:
        for i in range(len(A)):
            for j in range(len(A)):
                if A[i] == A[j] and i != j:
                    check = True
    return check


def createJsonProbeHistory(probePath, journalPath, operationsPath):
    A = CSVreader(probePath)
    A.remove(A[0])
    # creo il bigArray
    pastValue = A[0]
    Operations = []
    k = 0
    B = []
    bigArray = []

    for i in range(len(A)):
        currentValue = A[i]
        if currentValue[0] == pastValue[0]:
            B.append(currentValue)
        else:
            bigArray.append(B)
            B = []
            B.append(currentValue)  # risolve il problema che non printa la 1°
        pastValue = currentValue
        if i == len(A) - 1:
            bigArray.append(B)

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


def manipulation_analysis(finalScorePath, opHistoryPath, allOperationsPath, valore_soglia, valore_optout):
    # finalScore.csv
    scoreMatrix = CSVreader(finalScorePath)
    scoreMatrix.remove(scoreMatrix[0])  # Rimuovo l'intestazione
    # probeHistory.json
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
                if float(scoreMatrix[i][1]) == valore_optout:
                    tmp.append(scoreMatrix[i][0])  # Probe
                    tmp.append(scoreMatrix[i][1])  # Score
                    scoreMatrix_opt.append(tmp)  # Probe|Score
                    tmp = []
                else:
                    tmp.append(scoreMatrix[i][0])  # Probe
                    tmp.append(scoreMatrix[i][1])  # Score
                    scoreMatrix_no_opt.append(tmp)  # Probe|Score
                    tmp = []

        if match == False:
            count = count + 1
            tmp.append(scoreMatrix[i][0])  # Probe
            tmp.append(scoreMatrix[i][1])  # Score
            noJSON.append(tmp)  # Probe|Score
            tmp = []
        match = False


    # ANALISI di scoreMatrix_no_opt
    MATCHED = []
    NOMATCHED = []
    for i in range(len(scoreMatrix_no_opt)):
        if (float(scoreMatrix_no_opt[i][1]) >= valore_soglia):
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
            for j in range(len(scoreOperations_no_one_matched[i][2])):
                if data2['operations'][k]['name'] == scoreOperations_no_one_matched[i][2][j]['name']:
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
            for j in range(len(scoreOperations_no_one_no_matched[i][2])):
                if data2['operations'][k]['name'] == scoreOperations_no_one_no_matched[i][2][j]['name']:
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
            for j in range(len(scoreOperations_one[i][2])):
                if data2['operations'][k]['name'] == scoreOperations_one[i][2][j]['name']:
                    countOp = countOp + 1
                    break
        if countOp > 0:
            tmp.append(data2['operations'][k]['name'])
            tmp.append(countOp)
            repeatOp_one.append(tmp)
        countOp = 0
        tmp = []

    # Matrice globale contente: ProbeID,score
    global_score = scoreMatrix_opt + scoreMatrix_no_opt + noJSON
    print('\nNumero di ProbeID nel CSV score: ', len(scoreMatrix))
    print('Numero di ProbeID nel JSON contente le storie: ', len(opHistory['probesFileID']))
    print("")
    print('Numero di ProbeID che matchano nel JSON contenente le storie, e quindi analizzabili: ', len(scoreMatrix_opt) + len(scoreMatrix_no_opt))
    print('Numero di ProbeID non trovate nel JSON contenente storie: ', len(noJSON))
    print("")

    print('--------------- Probe trovate nel Json contente le storie --------------------')
    print('                     Occorrenze delle operazioni')
    repeatOp_oneSorted = sortScoreMatrix(repeatOp_one)
    repeatOp_no_MatchedSorted = sortScoreMatrix(repeatOp_noMatched)
    repeatOp_matchedSorted = sortScoreMatrix(repeatOp_matched)
    print('score =',valore_optout, ' n° probe =',len(scoreMatrix_opt))
    printInColumn(repeatOp_oneSorted)
    print("")
    print('score <', valore_soglia, ' n° probe =',len(NOMATCHED))
    printInColumn(repeatOp_no_MatchedSorted)
    print("")
    print('score >=', valore_soglia, ' n° probe =',len(MATCHED))
    printInColumn(repeatOp_matchedSorted)
    print("")

    print('--------------- Probe NON trovate nel Json contente le storie--------------------')
    printInColumn(noJSON)



def scoreFilter1(finalScorePath, opHistoryPath, score, opFilter, operator='null', score2 = None):
    # finalScore.csv
    scoreMatrix = CSVreader(finalScorePath)
    scoreMatrix.remove(scoreMatrix[0])  # Rimuovo l'intestazione
    # probeHistory.json
    with open(opHistoryPath) as f:
        opHistory = json.load(f)

    opFilter= [x.lower() for x in opFilter]

    duplicateOP = check(opFilter)
    if duplicateOP == False:
        atLeastOneOp = False
        tmp = []
        result = []
        tmpMatrix = []
        atLeastOneOp = False
        for i in range(len(scoreMatrix)):
            for j in range(len(opHistory['probesFileID'])):
                if scoreMatrix[i][0] == opHistory['probesFileID'][j]['probeID']:
                    tmp.append(scoreMatrix[i][0])
                    tmp.append(scoreMatrix[i][1])
                    tmp.append(opHistory['probesFileID'][j]['operations'])
                    tmpMatrix.append(tmp)
                    tmp = []
        tmp = []
        tmpMatrix2 = []
        countOperations = 0
        objPosition = -1
        firstMatched = False

        if operator == 'null':
            print('errore,inserire operazioni')

        elif (score != -1) and (score < 0):
            print('errore,valore inserito non corretto')
            return 0


        elif (operator == 'equal'):
            for i in range(len(tmpMatrix)):
                if float(tmpMatrix[i][1]) == score:
                    tmp.append(tmpMatrix[i][0])
                    for z in range(len(opFilter)):
                        currentOperation = opFilter[z]
                        for j in range(len(tmpMatrix[i][2])):
                            countOperations = countOperations + 1
                            if (currentOperation == tmpMatrix[i][2][j]['name'].lower()):
                                objPosition = countOperations
                                break
                        if objPosition != -1:
                            tmp.append(tmpMatrix[i][2][j]['name'])
                            tmp.append(objPosition)
                            atLeastOneOp = True
                        objPosition = -1
                        countOperations = 0
                    tmp.append('lenght:' + " " +str(len(tmpMatrix[i][2])))
                    if atLeastOneOp == True:
                        tmpMatrix2.append(tmp)
                    tmp = []
                    atLeastOneOp = False
            for i in range(len(tmpMatrix2)):
                result.append(tmpMatrix2[i])
            return result


        elif (operator) == 'over' and (score == -1):
            print('errore,valore inserito non corretto')
            return 0


        elif (operator == 'over') and (score >= 0):
            for i in range(len(tmpMatrix)):
                if float(tmpMatrix[i][1]) >= score:
                    tmp.append(tmpMatrix[i][0])
                    for z in range(len(opFilter)):
                        currentOperation = opFilter[z]
                        for j in range(len(tmpMatrix[i][2])):
                            countOperations = countOperations + 1
                            if (currentOperation == tmpMatrix[i][2][j]['name'].lower()):
                                objPosition = countOperations
                                break
                        if objPosition != -1:
                            tmp.append(tmpMatrix[i][2][j]['name'])
                            tmp.append(objPosition)
                            atLeastOneOp = True
                        objPosition = -1
                        countOperations = 0
                    tmp.append('lenght:' + " " +str(len(tmpMatrix[i][2])))
                    tmp.append('score:' + " "+ str((tmpMatrix[i][1])))
                    if atLeastOneOp == True:
                        tmpMatrix2.append(tmp)
                    tmp = []
                    atLeastOneOp = False
            for i in range(len(tmpMatrix2)):
                result.append(tmpMatrix2[i])
            return result

        elif (operator == 'under') and (score >= 0):
            for i in range(len(tmpMatrix)):
                if (float(tmpMatrix[i][1]) < score) and (float(tmpMatrix[i][1]) != -1):
                    tmp.append(tmpMatrix[i][0])
                    for z in range(len(opFilter)):
                        currentOperation = opFilter[z]
                        for j in range(len(tmpMatrix[i][2])):
                            countOperations = countOperations + 1
                            if (currentOperation == tmpMatrix[i][2][j]['name'].lower()):
                                objPosition = countOperations
                                break
                        if objPosition != -1:
                            tmp.append(tmpMatrix[i][2][j]['name'])
                            tmp.append(objPosition)
                            atLeastOneOp = True
                        objPosition = -1
                        countOperations = 0
                    tmp.append('lenght:' + " " +str(len(tmpMatrix[i][2])))
                    tmp.append('score:' + " "+ str((tmpMatrix[i][1])))
                    if atLeastOneOp == True:
                        tmpMatrix2.append(tmp)
                    tmp = []
                    atLeastOneOp = False
            for i in range(len(tmpMatrix2)):
                result.append(tmpMatrix2[i])
            return result

        elif (operator == 'range') and (score2 != None) and (score2 >= 0):
            for i in range(len(tmpMatrix)):
                if (float(tmpMatrix[i][1]) >= score) and (float(tmpMatrix[i][1]) <= score2):
                    tmp.append(tmpMatrix[i][0])
                    for z in range(len(opFilter)):
                        currentOperation = opFilter[z]
                        for j in range(len(tmpMatrix[i][2])):
                            countOperations = countOperations + 1
                            if (currentOperation == tmpMatrix[i][2][j]['name'].lower()):
                                objPosition = countOperations
                                break
                        if objPosition != -1:
                            tmp.append(tmpMatrix[i][2][j]['name'])
                            tmp.append(objPosition)
                            atLeastOneOp = True
                        objPosition = -1
                        countOperations = 0
                    tmp.append('lenght:' + " " +str(len(tmpMatrix[i][2])))
                    tmp.append('score:' + " "+ str((tmpMatrix[i][1])))
                    if atLeastOneOp == True:
                        tmpMatrix2.append(tmp)
                    tmp = []
                    atLeastOneOp = False
            for i in range(len(tmpMatrix2)):
                result.append(tmpMatrix2[i])
            return result

        elif (operator == 'range') and (score2 == None or score2 < 0):
            print('operazione non consentita')
            return 0

        elif (operator == 'under') and (score == -1):
            print('Error')
            return 0
    else:
        print('errore,operazioni duplicate inserite')
        return 0

def scoreFilter2(finalScorePath, opHistoryPath, score, opFilter, operator ='null',score2 = None):
    # finalScore.csv
    scoreMatrix = CSVreader(finalScorePath)
    scoreMatrix.remove(scoreMatrix[0])  # Rimuovo l'intestazione
    # probeHistory.json
    with open(opHistoryPath) as f:
        opHistory = json.load(f)

    opFilter = [x.lower() for x in opFilter]

    duplicateOP = check(opFilter)

    if duplicateOP == False:
        atLeastOneOp = False
        tmp = []
        tmpResult = []
        result = []
        tmpMatrix = []
        match = False
        found = False
        for i in range(len(scoreMatrix)):
            for j in range(len(opHistory['probesFileID'])):
                if scoreMatrix[i][0] == opHistory['probesFileID'][j]['probeID']:
                    tmp.append(scoreMatrix[i][0])
                    tmp.append(scoreMatrix[i][1])
                    tmp.append(opHistory['probesFileID'][j]['operations'])
                    tmpMatrix.append(tmp)
                    tmp = []
        lastOp = None
        count = 0
        tmp = []
        tmpOp = []
        countOperations = 0
        countOp = 0
        previousOperations = []
        occurrence = []
        duplicate = False
        finalResult = []
        tmpOcc = []
        if operator == 'null':
            print('errore,inserire operazioni')

        elif (operator == 'equal'):
            for z in range(len(opFilter)):
                currentOperation = opFilter[z]
                for i in range(len(tmpMatrix)):
                    if float(tmpMatrix[i][1]) == score:
                        for j in range(len(tmpMatrix[i][2])):
                            if tmpMatrix[i][2][j]['name'].lower() != currentOperation:
                                countOperations = countOperations + 1
                                lastOp = tmpMatrix[i][2][j]['name'].lower()
                            else:
                                found = True
                                if lastOp != None:
                                    previousOperations.append(lastOp)
                                break
                        if found == True:
                            tmp.append(currentOperation)
                            tmp.append(tmpMatrix[i][0])
                            tmp.append(countOperations)
                            tmpResult.append(tmp)
                            atLeastOneOp = True
                        tmp = []
                        tmpOp = []
                        countOperations = 0
                        found =  False
                        lastOp = None
                    if atLeastOneOp == True:
                        result.append(tmpResult)
                    tmpResult = []
                    atLeastOneOp = False
                for k in range(len(previousOperations)):
                    for s in range(len(occurrence)):
                        if previousOperations[k] == occurrence[s][0]:
                            duplicate = True
                    if duplicate == False:
                        for n in range(len(previousOperations)):
                            if previousOperations[k] == previousOperations[n]:
                                count = count + 1
                        tmpOcc.append(previousOperations[k])
                        tmpOcc.append(count)
                        occurrence.append(tmpOcc)
                        tmpOcc = []
                    count = 0
                    duplicate = False
                finalResult.append(currentOperation)
                finalResult.append(occurrence)
                previousOperations = []
                occurrence = []
            for i in range(len(finalResult)):
                try:
                    finalResult[i] = sortScoreMatrix(finalResult[i])
                except IndexError:
                    continue

            return result,finalResult


        elif (operator == 'over') and (score >= 0):
            for z in range(len(opFilter)):
                currentOperation = opFilter[z]
                for i in range(len(tmpMatrix)):
                    if float(tmpMatrix[i][1]) >=  score:
                        for j in range(len(tmpMatrix[i][2])):
                            if tmpMatrix[i][2][j]['name'].lower() != currentOperation:
                                countOperations = countOperations + 1
                                lastOp = tmpMatrix[i][2][j]['name'].lower()
                            else:
                                found = True
                                if lastOp != None:
                                    previousOperations.append(lastOp)
                                break
                        if found == True:
                            tmp.append(currentOperation)
                            tmp.append(tmpMatrix[i][0])
                            tmp.append(countOperations)
                            tmp.append('score:'+''+ tmpMatrix[i][1])
                            tmpResult.append(tmp)
                            atLeastOneOp = True
                        tmp = []
                        tmpOp = []
                        countOperations = 0
                        found =  False
                        lastOp = None
                    if atLeastOneOp == True:
                        result.append(tmpResult)
                    tmpResult = []
                    atLeastOneOp = False
                for k in range(len(previousOperations)):
                    for s in range(len(occurrence)):
                        if previousOperations[k] == occurrence[s][0]:
                            duplicate = True
                    if duplicate == False:
                        for n in range(len(previousOperations)):
                            if previousOperations[k] == previousOperations[n]:
                                count = count + 1
                        tmpOcc.append(previousOperations[k])
                        tmpOcc.append(count)
                        occurrence.append(tmpOcc)
                        tmpOcc = []
                    count = 0
                    duplicate = False
                finalResult.append(currentOperation)
                finalResult.append(occurrence)
                previousOperations = []
                occurrence = []
            for i in range(len(finalResult)):
                try:
                    finalResult[i] = sortScoreMatrix(finalResult[i])
                except IndexError:
                    continue
            return result,finalResult

        elif (operator == 'under') and (score >= 0):
            for z in range(len(opFilter)):
                currentOperation = opFilter[z]
                for i in range(len(tmpMatrix)):
                    if float(tmpMatrix[i][1]) < score and (float(tmpMatrix[i][1]) != -1):
                        for j in range(len(tmpMatrix[i][2])):
                            if tmpMatrix[i][2][j]['name'].lower() != currentOperation:
                                countOperations = countOperations + 1
                                lastOp = tmpMatrix[i][2][j]['name'].lower()
                            else:
                                found = True
                                if lastOp != None:
                                    previousOperations.append(lastOp)
                                break
                        if found == True:
                            tmp.append(currentOperation)
                            tmp.append(tmpMatrix[i][0])
                            tmp.append(countOperations)
                            tmp.append('score:'+''+ tmpMatrix[i][1])
                            tmpResult.append(tmp)
                            atLeastOneOp = True
                        tmp = []
                        tmpOp = []
                        countOperations = 0
                        found =  False
                        lastOp = None
                    if atLeastOneOp == True:
                        result.append(tmpResult)
                    tmpResult = []
                    atLeastOneOp = False
                for k in range(len(previousOperations)):
                    for s in range(len(occurrence)):
                        if previousOperations[k] == occurrence[s][0]:
                            duplicate = True
                    if duplicate == False:
                        for n in range(len(previousOperations)):
                            if previousOperations[k] == previousOperations[n]:
                                count = count + 1
                        tmpOcc.append(previousOperations[k])
                        tmpOcc.append(count)
                        occurrence.append(tmpOcc)
                        tmpOcc = []
                    count = 0
                    duplicate = False
                finalResult.append(currentOperation)
                finalResult.append(occurrence)
                previousOperations = []
                occurrence = []
            for i in range(len(finalResult)):
                try:
                    finalResult[i] = sortScoreMatrix(finalResult[i])
                except IndexError:
                    continue
            return result,finalResult

        elif (operator == 'range') and (score >= 0) and (score2 != None) and (score2 >= 0):
            for z in range(len(opFilter)):
                currentOperation = opFilter[z]
                for i in range(len(tmpMatrix)):
                    if float(tmpMatrix[i][1]) >= score and (float(tmpMatrix[i][1]) <= score2):
                        for j in range(len(tmpMatrix[i][2])):
                            if tmpMatrix[i][2][j]['name'].lower() != currentOperation:
                                countOperations = countOperations + 1
                                lastOp = tmpMatrix[i][2][j]['name'].lower()
                            else:
                                found = True
                                if lastOp != None:
                                    previousOperations.append(lastOp)
                                break
                        if found == True:
                            tmp.append(currentOperation)
                            tmp.append(tmpMatrix[i][0])
                            tmp.append(countOperations)
                            tmp.append('score:'+''+ tmpMatrix[i][1])
                            tmpResult.append(tmp)
                            atLeastOneOp = True
                        tmp = []
                        tmpOp = []
                        countOperations = 0
                        found =  False
                        lastOp = None
                    if atLeastOneOp == True:
                        result.append(tmpResult)
                    tmpResult = []
                    atLeastOneOp = False
                for k in range(len(previousOperations)):
                    for s in range(len(occurrence)):
                        if previousOperations[k] == occurrence[s][0]:
                            duplicate = True
                    if duplicate == False:
                        for n in range(len(previousOperations)):
                            if previousOperations[k] == previousOperations[n]:
                                count = count + 1
                        tmpOcc.append(previousOperations[k])
                        tmpOcc.append(count)
                        occurrence.append(tmpOcc)
                        tmpOcc = []
                    count = 0
                    duplicate = False
                finalResult.append(currentOperation)
                finalResult.append(occurrence)
                previousOperations = []
                occurrence = []
            for i in range(len(finalResult)):
                try:
                    finalResult[i] = sortScoreMatrix(finalResult[i])
                except IndexError:
                    continue
            return result,finalResult

        elif (score != -1) and (score < 0):
            print('errore,inserire parametri corretti')
            return 0,0

        elif (operator == 'range') and (score2 == None or score2 < 0):
            print('errore,inserire parametri corretti')
            return 0,0

        elif (operator == 'under') and (score == -1):
            print('errore,inserire parametri corretti')
            return 0,0

        elif (operator == 'over') and (score == -1):
            print('errore,inserire parametri corretti')
            return 0,0

def allOperations(finalScorePath, opHistoryPath):
    # finalScore.csv
    scoreMatrix = CSVreader(finalScorePath)
    scoreMatrix.remove(scoreMatrix[0])  # Rimuovo l'intestazione
    # Leggo le probe history
    with open(opHistoryPath) as f:
        opHistory = json.load(f)

    all_operations = []
    for i in range(len(scoreMatrix)):
        for j in range(len(opHistory['probesFileID'])):
            if scoreMatrix[i][0] == opHistory['probesFileID'][j]['probeID']:
                for z in range(len(opHistory['probesFileID'][j]['operations'])):
                    if opHistory['probesFileID'][j]['operations'][z]['name'] not in all_operations:
                        all_operations.append(opHistory['probesFileID'][j]['operations'][z]['name'])
    all_operations.sort()
    printInColumn(all_operations)


def division(finalScorePath, opHistoryPath, valore_soglia, valore_optout):
    # finalScore.csv
    scoreMatrix = CSVreader(finalScorePath)
    scoreMatrix.remove(scoreMatrix[0])  # Rimuovo l'intestazione
    # probeHistory.json

    # # Leggo csv ManipReference
    # camera = CSVreader(cameraPath)
    # camera.remove(camera[0])  # Rimuovo l'intestazione

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
                if (float(scoreMatrix[i][1]) == valore_optout):
                    tmp.append(scoreMatrix[i][0])  # Probe
                    tmp.append(scoreMatrix[i][1])  # Score
                    #tmp.append(scoreMatrix[i][3])
                    scoreMatrix_opt.append(tmp)  # Probe|Score
                    tmp = []
                else:
                    tmp.append(scoreMatrix[i][0])  # Probe
                    tmp.append(scoreMatrix[i][1])  # Score
                    #tmp.append(scoreMatrix[i][3])
                    scoreMatrix_no_opt.append(tmp)  # Probe|Camera|Score
                    tmp = []

        if match == False:
            count = count + 1
            tmp.append(scoreMatrix[i][0])  # Probe
            tmp.append(scoreMatrix[i][1])  # Score
            #tmp.append(scoreMatrix[i][3])
            noJSON.append(tmp)  # Probe|Score
            tmp = []
        match = False

        # for i in range(len(scoreMatrix)):
        #     for j in range(len(opHistory['probesFileID'])):
        #         if scoreMatrix[i][0] == opHistory['probesFileID'][j]['probeID']:
        #             match = True
        #             tmp = [scoreMatrix[i][0], scoreMatrix[i][1], scoreMatrix[i][3]]
        #             if scoreMatrix[i][3] == str(valore_optout):
        #                 scoreMatrix_opt.append(tmp)  # Probe|Camera|Score
        #             else:
        #                 scoreMatrix_no_opt.append(tmp)  # Probe|Camera|Score
        #             tmp = []
        #     if match == False:
        #         count = count + 1
        #         noJSON.append(tmp)  # Probe|Camera|Score
        #         tmp = []
        #     match = False

        # # scoreMatrix_one è una matrice contenente: ProbeID,Camera,score=-1,isManipulated/notManipulated raggruppata per Y(yes is manipulated)
        # X = []
        # Y = []
        # for i in range(len(scoreMatrix_opt)):
        #     for j in range(len(camera)):
        #         if ((scoreMatrix_opt[i][0] == camera[j][1]) and (scoreMatrix_opt[i][1]) == camera[j][3]):
        #             tmp.append(scoreMatrix_opt[i][0])
        #             tmp.append(scoreMatrix_opt[i][1])
        #             tmp.append(scoreMatrix_opt[i][2])
        #             tmp.append(camera[j][5])
        #             tmp.append(camera[j][2].split(".", 1)[1])
        #             if (camera[j][5]) == 'Y':
        #                 X.append(tmp)
        #             else:
        #                 Y.append(tmp)
        #             tmp = []
        # scoreMatrix_opt = X + Y

        # scoreMatrix_no_opt è una matrice contenente: ProbeID,Camera,score!=-1,isManipulated/notManipulated raggruppata per Y(yes is manipulated)
        # X = []
        # Y = []
        # for i in range(len(scoreMatrix_no_opt)):
        #     for j in range(len(camera)):
        #         if ((scoreMatrix_no_opt[i][0] == camera[j][1]) and (scoreMatrix_no_opt[i][1]) == camera[j][3]):
        #             tmp.append(scoreMatrix_no_opt[i][0])
        #             tmp.append(scoreMatrix_no_opt[i][1])
        #             tmp.append(scoreMatrix_no_opt[i][2])
        #             tmp.append(camera[j][5])
        #             tmp.append(camera[j][2].split(".", 1)[1])
        #             if (camera[j][5]) == 'Y':
        #                 X.append(tmp)
        #             else:
        #                 Y.append(tmp)
        #             tmp = []
        # scoreMatrix_no_opt = X + Y

        # ANALISI di scoreMatrix_no_opt
        MATCHED = []
        NOMATCHED = []
        for i in range(len(scoreMatrix_no_opt)):
            if (float(scoreMatrix_no_opt[i][1]) >= valore_soglia):
                MATCHED.append(scoreMatrix_no_opt[i])
            else:
                NOMATCHED.append(scoreMatrix_no_opt[i])

    print('')
    print('probe with score = ',valore_optout)
    printInColumn(scoreMatrix_opt)

    print('')
    print('probe with score >= ', valore_soglia)
    printInColumn(MATCHED)

    print('')
    print('probe with score < ', valore_soglia)
    printInColumn(NOMATCHED)

    print('')
    print('------------- probe not found in json history -------------------- ')
    printInColumn(noJSON)

def get_parser():
    parser = argparse.ArgumentParser(description="", formatter_class=RawTextHelpFormatter)

    subparser = parser.add_subparsers(dest='subcommand')

    # subcommand create-json-probe-history
    history_parser = subparser.add_parser('create-json-probe-history',
                                          help='Create a json file containing the probe history')
    history_parser.add_argument("-p", "--probejournaljoin", required=True, help="insert probejournalname path")
    history_parser.add_argument("-j", "--journalmask", required=True, help="insert journalmask path")
    history_parser.add_argument("-o", "--operations", required=True, help="insert json file contains all operations")

    # subcommand division for optout, matched and no_matched
    division_parse = subparser.add_parser('division', help='Mostra la seguente tabella:'
                                                           '\n|ID_probe|Camera|Score|Manip/NonManip|Formato|'
                                                           '\n   aaa      xx   46.15      Y          .avi\n')
    division_parse.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    division_parse.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    #division_parse.add_argument("-cp", "--camerapath", required=True, help="path of camera reference")
    division_parse.add_argument("-vs", "--valoresoglia", type=float, required=True, help="valore di soglia")
    division_parse.add_argument("-vo", "--valoreoptout", type=float, required=True, help="valore di optout")

    # subcommand manipulation-name
    manipulation_parser = subparser.add_parser('manipulation-analysis', help='List all possible manipulations')
    manipulation_parser.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    manipulation_parser.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    #manipulation_parser.add_argument("-cp", "--camerapath", required=True, help="path of camera reference")
    manipulation_parser.add_argument("-o", "--operations", required=True,
                                     help="insert json file path contains all operations")
    manipulation_parser.add_argument("-vs", "--valoresoglia", type=float, required=True, help="valore di soglia")
    manipulation_parser.add_argument("-vo", "--valoreoptout", type=float, required=True, help="valore di optout")

    # subcommand filter1
    filter1_parser = subparser.add_parser('filter1', help='Mostra la seguente tabella'
                                                          ' \n|ID_probe|Camera|Filtro|n° di quando è stato applicato|n° di operaziono subite|'
                                                          ' \n    aaa    xxx    Blur                2                           5 ')
    filter1_parser.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    filter1_parser.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    filter1_parser.add_argument("-s", "--score", required=True, type=float, help="insert score")
    filter1_parser.add_argument("-op", "--operator", required=True, help="insert operator like over,under,equal,range")
    filter1_parser.add_argument("-s2", "--score2", required=False, type=float, help="insert score2")
    filter1_parser.add_argument("-o", "--operation", required=True, nargs='+', help="insert operation filter")

    # subcommand filter2
    filter2_parser = subparser.add_parser('filter2', help='Mostra la seguente tabella'
                                                          ' \n|ID_probe|Filtro|Operazioni precedenti in base al numero passato|'
                                                          ' \n    aaa    Blur       OutputAVI,AddNoise   2                         ')
    filter2_parser.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    filter2_parser.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    filter2_parser.add_argument("-s", "--score", required=True, type=float, help="insert score")
    filter2_parser.add_argument("-op", "--operator", required=True, help="insert operator like over,under,equal,range")
    filter2_parser.add_argument("-s2", "--score2", required=False, type=float, help="insert score2")
    filter2_parser.add_argument("-o", "--operation", required=True, nargs='+', help="insert operation filter")
    #filter2_parser.add_argument("-po", "--prevop", type=int, required=True, help="insert preview operations")

    # subcommand alloperations
    all_operations_parser = subparser.add_parser('alloperations',
                                                 help='Mostra tutte le operazioni che sono state fatte in tutte le probe')
    all_operations_parser.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    all_operations_parser.add_argument("-hp", "--probehistory", required=True, help="path of probe history")

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.subcommand == 'create-json-probe-history':
        createJsonProbeHistory(probePath=args.probejournaljoin, journalPath=args.journalmask,operationsPath=args.operations)
    elif args.subcommand == 'division':
        division(finalScorePath=args.scorepath, opHistoryPath=args.probehistory,valore_soglia=args.valoresoglia, valore_optout=args.valoreoptout)
    elif args.subcommand == 'manipulation-analysis':
        print('manipulation_list')
        manipulation_analysis(finalScorePath=args.scorepath, opHistoryPath=args.probehistory,allOperationsPath=args.operations, valore_soglia=args.valoresoglia,valore_optout=args.valoreoptout)
    elif args.subcommand == 'filter1':
        result = scoreFilter1(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, score=args.score,opFilter=args.operation, operator=args.operator, score2=args.score2)
        printInColumn(result)
    elif args.subcommand == 'filter2':
        result, previousOccurrence = scoreFilter2(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, score=args.score,opFilter=args.operation, operator=args.operator,score2=args.score2)
        printInColumn(previousOccurrence)
    elif args.subcommand == 'alloperations':
        allOperations(finalScorePath=args.scorepath, opHistoryPath=args.probehistory)


def mainInterattivo():
    print('Which operation do you want use?')
    print('1) Create json file containing probe history')
    print('2) Manipulation analysis and operations recurrence')
    print('3) Filter1')
    print('4) Filter2')
    print('5) Divison score in optout,matched and no matched')
    print('6) All operations')
    print('7) Exit')

    mainScelta = int(input())

    if (mainScelta < 1) or (mainScelta > 6):
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
        print('Insert score path: ')
        finalScorePath = input().strip()
        print('Insert probe history path: ')
        opHistoryPath = input().strip()
        print('Insert camera reference path: ')
        cameraPath = input().strip()
        print('insert operations reference path: ')
        operationsPath = input().strip()
        print('insert valore di soglia: ')
        valore_soglia = int(input())
        print('insert valore di optout: ')
        valore_optout = int(input())

        manipulation_analysis(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath,allOperationsPath=operationsPath, valore_soglia=valore_soglia, valore_optout=valore_optout)

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
                score = float(score)
            elif operator == 3:
                operator = 'under'
                score = parse(sceltaOpzione[0] + '[' + '{}' + ']', sceltaOpzione)[0]
                score = float(score)
            elif operator == 4:
                operator = 'range'
                score = parse(sceltaOpzione[0] + '[' + '{}' + ',' + '{}' + ']', sceltaOpzione)[0]
                score2 = parse(sceltaOpzione[0] + '[' + '{}' + ',' + '{}' + ']', sceltaOpzione)[1]
                score = float(score)
                score2 = float(score2)
            else:
                sys.exit()

            # inserimento operazione
            print('Insert operation name: ')
            opFilter = input()
            opFilter = opFilter.split()

            if (mainScelta == 3):
                if operator == 'range':
                    print('')
                    result = scoreFilter1(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score, opFilter=[opFilter], operator=operator, score2=score2)
                    printInColumn(result)
                else:
                    print('')
                    result = scoreFilter1(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score,opFilter=[opFilter], operator=operator)
                    printInColumn(result)

            if (mainScelta == 4):
                # inserimento numero di operazioni precedenti
                print('Insert number of previews operations to view: ')
                prevOp = int(input())
                if operator == 'range':
                    print('')
                    result,previousOccurrence = scoreFilter2(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score,opFilter=[opFilter], operator=operator, score2=score2)
                    printInColumn(previousOccurrence)
                else:
                    print('')
                    result, previousOccurrence = scoreFilter2(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score, opFilter=[opFilter], operator=operator)
                    printInColumn(previousOccurrence)

    elif (mainScelta == 5):
        print('Insert score path: ')
        finalScorePath = input().strip()
        print('Insert probe history path: ')
        opHistoryPath = input().strip()
        #print('Insert camera reference path: ')
        #cameraPath = input().strip()
        print('insert valore di soglia: ')
        valore_soglia = int(input())
        print('insert valore di optout: ')
        valore_optout = int(input())
        division(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath,valore_soglia=valore_soglia, valore_optout=valore_optout)

    elif (mainScelta == 6):
        print('Insert score path: ')
        finalScorePath = input().strip()
        print('Insert probe history path: ')
        opHistoryPath = input().strip()
        allOperations(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath)


if __name__ == '__main__':
    if sys.argv[1:] != []:
        main()
    else:
        mainInterattivo()

