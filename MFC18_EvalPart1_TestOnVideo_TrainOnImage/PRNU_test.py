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


def addCameraReference(matrix,camera):
    X = []
    Y = []
    tmp = []
    for i in range(len(matrix)):
        for j in range(len(camera)):
            if ((matrix[i][0] == camera[j][1]) and (matrix[i][1]) == camera[j][3]):
                tmp.append(matrix[i][0])
                tmp.append(matrix[i][1])
                tmp.append(matrix[i][2])
                tmp.append(camera[j][5])
                tmp.append(camera[j][2].split(".", 1)[1])
                if (camera[j][5]) == 'Y':
                    X.append(tmp)
                else:
                    Y.append(tmp)
                tmp = []
    matrix = X + Y
    return matrix

def division(finalScorePath, opHistoryPath, cameraPath, valore_soglia, valore_optout,returnFlag = 0):
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
                    tmp.append(scoreMatrix[i][0])  # Probe
                    tmp.append(scoreMatrix[i][1])  # Camera
                    tmp.append(scoreMatrix[i][3])  # Score
                    scoreMatrix_opt.append(tmp)  # Probe|Camera|Score
                    tmp = []
                else:
                    tmp.append(scoreMatrix[i][0])  # Probe
                    tmp.append(scoreMatrix[i][1])  # Camera
                    tmp.append(scoreMatrix[i][3])  # Score
                    scoreMatrix_no_opt.append(tmp)  # Probe|Camera|Score
                    tmp = []

        if match == False:
            count = count + 1
            tmp.append(scoreMatrix[i][0])  # Probe
            tmp.append(scoreMatrix[i][1])  # Camera
            tmp.append(scoreMatrix[i][3])  # Score
            noJSON.append(tmp)  # Probe|Camera|Score
            tmp = []
        match = False

        scoreMatrix_opt = addCameraReference(scoreMatrix_opt,camera)
        scoreMatrix_no_opt = addCameraReference(scoreMatrix_no_opt,camera)
        noJSON = addCameraReference(noJSON,camera)
        # ANALISI di scoreMatrix_no_opt
        MATCHED = []
        NOMATCHED = []
        for i in range(len(scoreMatrix_no_opt)):
            if (float(scoreMatrix_no_opt[i][2]) >= valore_soglia):
                MATCHED.append(scoreMatrix_no_opt[i])
            else:
                NOMATCHED.append(scoreMatrix_no_opt[i])

        # noJSON è una matrice contenente: ProbeID,score,isManipulated/notManipulated raggruppata per Y(yes is manipulated)
    if returnFlag == 0:
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
    
    if returnFlag == 1:
        return scoreMatrix_opt,MATCHED,NOMATCHED,noJSON

def AddHistoryManip(scoreMatrix,opHistory):
    tmpMatrix = []
    tmp = []
    for i in range(len(scoreMatrix)):
        for j in range(len(opHistory['probesFileID'])):
            if scoreMatrix[i][0] == opHistory['probesFileID'][j]['probeID']:
                tmp.append(scoreMatrix[i][0])
                tmp.append(scoreMatrix[i][1])
                tmp.append(scoreMatrix[i][2])
                tmp.append(scoreMatrix[i][3])
                tmp.append(scoreMatrix[i][4])
                tmp.append(opHistory['probesFileID'][j]['operations'])
                tmpMatrix.append(tmp)
                tmp = []
    return tmpMatrix  

def AddHistory(scoreMatrix,opHistory):

    tmpMatrix = []
    tmp = []
    maxlenght = 0
    for i in range(len(scoreMatrix)):
        for j in range(len(opHistory['probesFileID'])):
            if scoreMatrix[i][0] == opHistory['probesFileID'][j]['probeID']:
                tmp.append(scoreMatrix[i][0])
                tmp.append(scoreMatrix[i][1])
                tmp.append(scoreMatrix[i][3])
                tmp.append(opHistory['probesFileID'][j]['operations'])
                if len(opHistory['probesFileID'][j]['operations'])> maxlenght:
                    maxlenght = len(opHistory['probesFileID'][j]['operations'])
                tmpMatrix.append(tmp)
                tmp = []
    return tmpMatrix,maxlenght 

def countOp(matrix):
    countOp = 0
    tmp = []
    repeatOp = []
    foundOp = False    
    for i in range(len(matrix)):
        for j in range(len(matrix[i][5])):
            for k in range(len(repeatOp)):
                if matrix[i][5][j]['name'] == repeatOp[k][0]:
                    foundOp = True
                    break
            if foundOp == False:
                for t in range(len(matrix)):
                    for s in range(len(matrix[t][5])):
                        if matrix[i][5][j]['name'] == matrix[t][5][s]['name']:
                            countOp = countOp + 1
                            break
            if countOp > 0:
                tmp.append(matrix[i][5][j]['name'])
                tmp.append(countOp)
                repeatOp.append(tmp)
            countOp = 0
            tmp = []
            foundOp = False
    return repeatOp


def manipulation_analysis(finalScorePath, opHistoryPath, cameraPath, valore_soglia, valore_optout):

    scoreMatrix_opt,MATCHED,NOMATCHED,noJSON = division(finalScorePath, opHistoryPath, cameraPath, valore_soglia, valore_optout,returnFlag = 1)
    # Leggo le probe history
    with open(opHistoryPath) as f:
        opHistory = json.load(f)
    scoreOperations_one = AddHistoryManip(scoreMatrix_opt,opHistory)
    scoreOperations_no_one_matched = AddHistoryManip(MATCHED,opHistory)
    scoreOperations_no_one_no_matched = AddHistoryManip(NOMATCHED,opHistory)
    '''Conteggio ricorrenza operazioni in scoreMatrix_one, scoreMatrix_no_one_matched, scoreMatrix_no_one_no_matched'''
    repeatOp_matched = countOp(scoreOperations_no_one_matched)
    repeatOp_noMatched = countOp(scoreOperations_no_one_no_matched)
    repeatOp_one = countOp(scoreOperations_one)

    # Matrice globale contente: ProbeID,score
    print('\nNumero di ProbeID nel CSV score: ', len(scoreMatrix_opt)+ len(MATCHED)+ len(NOMATCHED) + len(noJSON))
    print('Numero di ProbeID nel JSON contente le storie: ', len(opHistory['probesFileID']))
    print("")
    print('Numero di ProbeID che matchano nel JSON contenente le storie, e quindi analizzabili: ', len(scoreMatrix_opt) + len(MATCHED)+ len(NOMATCHED))
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

    print('--------------- Probe NON trovate nel Json contente le storie-------------------- n° probe = ',len(noJSON))
    printInColumn(noJSON)

   
def _scoreFilter1(i,tmpMatrix,opFilter,occurenceMatrix,tmpMatrix2):
    tmp = []
    countOperations = 0
    objPosition = -1
    atLeastOneOp = False
    p = 0  #probeID index
    c = 1  #camera index
    s = 2  #score index
    op = 3 #operations index
    tmp.append(tmpMatrix[i][p])
    tmp.append(tmpMatrix[i][c])
    for z in range(len(opFilter)):
        currentOperation = opFilter[z]
        currentMatrix = occurenceMatrix[z]
        for j in range(len(tmpMatrix[i][op])):
            countOperations = countOperations + 1
            if (currentOperation == tmpMatrix[i][op][j]['name'].lower()):
                objPosition = countOperations
                break
        if objPosition != -1:
            tmp.append(tmpMatrix[i][op][j]['name'])
            tmp.append(objPosition)
            atLeastOneOp = True
            currentMatrix[objPosition -1][len(tmpMatrix[i][op]) - 1] = currentMatrix[objPosition -1][len(tmpMatrix[i][op]) -1] + 1
        occurenceMatrix[z] = currentMatrix
        objPosition = -1
        countOperations = 0
    tmp.append('lenght:' + " " +str(len(tmpMatrix[i][op])))
    tmp.append('score:' + " "+ str((tmpMatrix[i][s])))
    if atLeastOneOp == True:
        tmpMatrix2.append(tmp)
    tmp = []
    atLeastOneOp = False


def scoreFilter1(finalScorePath, opHistoryPath, score, opFilter, operator='null', score2 = None):
    s = 2 
    scoreMatrix = CSVreader(finalScorePath)
    scoreMatrix.remove(scoreMatrix[0])  # Rimuovo l'intestazione
    # probeHistory.json
    with open(opHistoryPath) as f:
        opHistory = json.load(f)
    opFilter= [x.lower() for x in opFilter]
    duplicateOP = check(opFilter)

    if duplicateOP == False:
        tmpMatrix,maxlenght = AddHistory(scoreMatrix,opHistory)
        result = []
        tmpMatrix2 = []
        occurenceMatrix = []

        for i in range(len(opFilter)):
            occurenceMatrix.append(np.zeros((int(maxlenght),int(maxlenght))))

        if operator == 'null':
            print('errore,inserire operazioni')

        elif (operator == 'equal'):
            for i in range(len(tmpMatrix)):
                if float(tmpMatrix[i][s]) == score:
                   _scoreFilter1(i,tmpMatrix,opFilter,occurenceMatrix,tmpMatrix2) 
            for i in range(len(tmpMatrix2)):
                result.append(tmpMatrix2[i])
            for i in range(len(occurenceMatrix)):
                print(occurenceMatrix[i])
                print("")
            return result


        elif (operator == 'over') and (score >= 0):
            for i in range(len(tmpMatrix)):
                if float(tmpMatrix[i][s]) >= score:
                   _scoreFilter1(i,tmpMatrix,opFilter,occurenceMatrix,tmpMatrix2) 
            for i in range(len(tmpMatrix2)):
                result.append(tmpMatrix2[i])
            for i in range(len(occurenceMatrix)):
                print(occurenceMatrix[i])
                print("")
            return result

        elif (operator == 'under') and (score >= 0):
            for i in range(len(tmpMatrix)):
                if (float(tmpMatrix[i][s]) < score) and (float(tmpMatrix[i][s]) != -1):
                   _scoreFilter1(i,tmpMatrix,opFilter,occurenceMatrix,tmpMatrix2) 
            for i in range(len(tmpMatrix2)):
                result.append(tmpMatrix2[i])
            for i in range(len(occurenceMatrix)):
                print(occurenceMatrix[i])
                print("")
            return result

        elif (operator == 'range') and (score2 != None) and (score2 >= 0):
            for i in range(len(tmpMatrix)):
                if (float(tmpMatrix[i][s]) >= score) and (float(tmpMatrix[i][s]) <= score2):
                   _scoreFilter1(i,tmpMatrix,opFilter,occurenceMatrix,tmpMatrix2) 
            for i in range(len(tmpMatrix2)):
                result.append(tmpMatrix2[i])
            for i in range(len(occurenceMatrix)):
                print(occurenceMatrix[i])
                print("")
            return result

        elif (score != -1) and (score < 0):
            print('errore,inserire parametri corretti')
            return None

        elif (operator) == 'over' and (score == -1):
            print('errore,inserire parametri corretti')
            return None

        elif (operator == 'range') and (score2 == None or score2 < 0):
            print('errore,inserire parametri corretti')
            return None

        elif (operator == 'under') and (score == -1):
            print('errore,inserire parametri corretti')
            return None
    else:
        print('errore,operazioni duplicate inserite')
        return None

def _scoreFilter2(i,tmpMatrix,currentOperation,previousOperations,countFirstOperation):
    p = 0  #probeID index
    c = 1  #camera index
    s = 2  #score index
    op = 3 #operations index
    atLeastOneOp = False
    found = False
    lastOp = None
    atLeastOneOp = False
    countOperations = 0
    tmp = []
    tmpOp = []
    tmpResult = []           
    for j in range(len(tmpMatrix[i][op])):
        if tmpMatrix[i][op][j]['name'].lower() != currentOperation:
            countOperations = countOperations + 1
            lastOp = tmpMatrix[i][op][j]['name']
        else:
            found = True
            if lastOp != None:
                previousOperations.append(lastOp)
            break
    if found == True:
        tmp.append(tmpMatrix[i][op][j]['name'])
        tmp.append(tmpMatrix[i][p])
        tmp.append(tmpMatrix[i][c])
        if countOperations > 0:
            tmp.append(countOperations)
        else:
            tmp.append('First operation')
            countFirstOperation = countFirstOperation + 1
        tmp.append('score:' + '' + tmpMatrix[i][s])      
        tmpResult.append(tmp)
        atLeastOneOp = True
    return atLeastOneOp,tmpResult,countFirstOperation

def countOccurrence(previousOperations):
    occurrence = []
    duplicate = False
    count = 0
    tmpOcc = []
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
    return occurrence

def scoreFilter2(finalScorePath, opHistoryPath, score, opFilter, operator='null', score2=None):
    s = 2
    atLeastOneOp = False
    scoreMatrix = CSVreader(finalScorePath)
    scoreMatrix.remove(scoreMatrix[0])  # Rimuovo l'intestazione
    # probeHistory.json
    with open(opHistoryPath) as f:
        opHistory = json.load(f)
    opFilter = [x.lower() for x in opFilter]
    duplicateOP = check(opFilter)

    if duplicateOP == False:
        tmpMatrix,maxlenght = AddHistory(scoreMatrix,opHistory)
        countOperations = 0
        previousOperations = []
        finalResult = []
        result = []
        occurrence = []
        countFirstOperation = 0
        if operator == 'null':
            print('errore,inserire operazioni')

        elif (operator == 'equal'):
            for z in range(len(opFilter)):
                currentOperation = opFilter[z]
                for i in range(len(tmpMatrix)):
                    if float(tmpMatrix[i][s]) == score:
                        atLeastOneOp,tmpResult,countFirstOperation = _scoreFilter2(i,tmpMatrix,currentOperation,previousOperations,countFirstOperation)
                        if atLeastOneOp == True:
                            result.append(tmpResult)
                occurrence = countOccurrence(previousOperations)
                finalResult.append(currentOperation +'  '+ 'N Times First Operations: ' + str(countFirstOperation))
                finalResult.append(occurrence)
                previousOperations = []
                occurrence = []
                countFirstOperation = 0

        elif (operator == 'over') and (score >= 0):
            for z in range(len(opFilter)):
                currentOperation = opFilter[z]
                for i in range(len(tmpMatrix)):
                    if float(tmpMatrix[i][s]) >= score:
                        atLeastOneOp,tmpResult,countFirstOperation = _scoreFilter2(i,tmpMatrix,currentOperation,previousOperations,countFirstOperation)
                        if atLeastOneOp == True:
                            result.append(tmpResult)
                occurrence = countOccurrence(previousOperations)
                finalResult.append(currentOperation +'  '+ 'N Times First Operations: ' + str(countFirstOperation))
                finalResult.append(occurrence)
                previousOperations = []
                occurrence = []
                countFirstOperation = 0


        elif (operator == 'under') and (score >= 0):
            for z in range(len(opFilter)):
                currentOperation = opFilter[z]
                for i in range(len(tmpMatrix)):
                    if float(tmpMatrix[i][s]) < score and float(tmpMatrix[i][s]) != -1:
                        atLeastOneOp,tmpResult,countFirstOperation = _scoreFilter2(i,tmpMatrix,currentOperation,previousOperations,countFirstOperation)
                        if atLeastOneOp == True:
                            result.append(tmpResult)
                occurrence = countOccurrence(previousOperations)
                finalResult.append(currentOperation +'  '+ 'N Times First Operations: ' + str(countFirstOperation))
                finalResult.append(occurrence)
                previousOperations = []
                occurrence = []
                countFirstOperation = 0

        elif (operator == 'range') and (score >= 0) and (score2 != None) and (score2 >= 0):
            for z in range(len(opFilter)):
                currentOperation = opFilter[z]
                for i in range(len(tmpMatrix)):
                    if float(tmpMatrix[i][s]) >= score and float(tmpMatrix[i][s]) < score2:
                        atLeastOneOp,tmpResult,countFirstOperation = _scoreFilter2(i,tmpMatrix,currentOperation,previousOperations,countFirstOperation)
                        if atLeastOneOp == True:
                            result.append(tmpResult)
                occurrence = countOccurrence(previousOperations)
                finalResult.append(currentOperation +'  '+ 'N Times First Operations: ' + str(countFirstOperation))
                finalResult.append(occurrence)
                previousOperations = []
                occurrence = []
                countFirstOperation = 0
                      
        elif (score != -1) and (score < 0):
            print('errore,inserire parametri corretti')
            return None, None

        elif (operator == 'range') and score < 0:
            print('errore,inserire parametri corretti')
            return None, None
        elif (operator == 'range') and (score2 == None or score2 < 0):
            print('errore,inserire parametri corretti')
            return None, None

        elif (operator == 'under') and (score == -1):
            print('errore,inserire parametri corretti')
            return None, None

        elif (operator == 'over') and (score == -1):
            print('errore,inserire parametri corretti')
            return None, None
        for i in range(len(finalResult)):
            try:
                finalResult[i] = sortScoreMatrix(finalResult[i])
            except IndexError:
                continue

        return result,finalResult

    else:

        print('errore,operazioni duplicate inserite!')
        return None, None


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

def cameraControl(finalScorePath,opHistoryPath,valoresoglia,valoreoptout):
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
        if float(M[i][2]) == valoreoptout:
            equal1.append(M[i][1])
        elif float(M[i][2]) < valoresoglia and float(M[i][2])!= valoreoptout :
            under50.append(M[i][1])
        elif float(M[i][2]) >= valoresoglia:
            over50.append(M[i][1])
    print("\n score =",valoreoptout)
    countcamera(equal1)
    print("\n score <",valoresoglia)
    countcamera(under50)
    print("\n score >",valoresoglia)
    countcamera(over50)
    print("")

def get_parser():
    parser = argparse.ArgumentParser(description="", formatter_class=RawTextHelpFormatter)

    subparser = parser.add_subparsers(dest='subcommand')

    # subcommand create-json-probe-history
    history_parser = subparser.add_parser('create-json-probe-history', help='Create a json file containing the probe history')
    history_parser.add_argument("-p", "--probejournaljoin", required=True, help="insert probejournalname path")
    history_parser.add_argument("-j", "--journalmask", required=True, help="insert journalmask path")
    history_parser.add_argument("-o", "--operations", required=True, help="insert json file contains all operations")

    # subcommand division for optout, matched and no_matched
    division_parse = subparser.add_parser('division', help='Mostra la seguente tabella:'
                                                           '\n|ID_probe|Camera|Score|Manip/NonManip|Formato|'
                                                           '\n   aaa      xx   46.15      Y          .avi\n')
    division_parse.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    division_parse.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    division_parse.add_argument("-cp", "--camerapath", required=True, help="path of camera reference")
    division_parse.add_argument("-vs", "--valoresoglia", type=int, required=True, help="valore di soglia")
    division_parse.add_argument("-vo", "--valoreoptout", type=int, required=True, help="valore di optout")

    # subcommand manipulation-analysis
    manipulation_parser = subparser.add_parser('manipulation-analysis', help='List all possible manipulations')
    manipulation_parser.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    manipulation_parser.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    manipulation_parser.add_argument("-cp", "--camerapath", required=True, help="path of camera reference")
    manipulation_parser.add_argument("-vs", "--valoresoglia",type=int, required=True, help="valore di soglia")
    manipulation_parser.add_argument("-vo", "--valoreoptout", type=int, required=True, help="valore di optout")

    # subcommand manipulation-analysis
    camera_parset = subparser.add_parser('camera-analysis', help='List all possible manipulations')
    camera_parset.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    camera_parset.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    camera_parset.add_argument("-vs", "--valoresoglia",type=int, required=True, help="valore di soglia")
    camera_parset.add_argument("-vo", "--valoreoptout", type=int, required=True, help="valore di optout")

    # subcommand filter1
    filter1_parser = subparser.add_parser('filter1', help='Mostra la seguente tabella'
                                                          ' \n|ID_probe|Camera|Filtro|n° di quando è stato applicato|n° di operaziono subite|'
                                                          ' \n    aaa    xxx    Blur                2                           5 ')
    filter1_parser.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    filter1_parser.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    filter1_parser.add_argument("-s", "--score", required=True, type=int, help="insert score")
    filter1_parser.add_argument("-op", "--operator", required=True, help="insert operator like over,under,equal,range")
    filter1_parser.add_argument("-s2", "--score2", required=False, type=int, help="insert score2")
    filter1_parser.add_argument("-o", "--operation", required=True, nargs='+', help="insert operation filter")

    # subcommand filter2
    filter2_parser = subparser.add_parser('filter2', help='Mostra la seguente tabella'
                                                          ' \n|ID_probe|Filtro|Operazioni precedenti in base al numero passato|'
                                                          ' \n    aaa    Blur       OutputAVI,AddNoise   2                         ')
    filter2_parser.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    filter2_parser.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    filter2_parser.add_argument("-s", "--score", required=True, type=int, help="insert score")
    filter2_parser.add_argument("-op", "--operator", required=True, help="insert operator like over,under,equal,range")
    filter2_parser.add_argument("-s2", "--score2", required=False , type=int, help="insert score2")
    filter2_parser.add_argument("-o", "--operation", required=True, nargs='+', help="insert operation filter")

    # subcommand alloperations
    all_operations_parser = subparser.add_parser('alloperations', help='Mostra tutte le operazioni che sono state fatte in tutte le probe')
    all_operations_parser.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    all_operations_parser.add_argument("-hp", "--probehistory", required=True, help="path of probe history")


    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.subcommand == 'create-json-probe-history':
        createJsonProbeHistory(probePath=args.probejournaljoin, journalPath=args.journalmask, operationsPath=args.operations)
    elif args.subcommand == 'division':
        division(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, cameraPath=args.camerapath, valore_soglia=args.valoresoglia, valore_optout=args.valoreoptout)
    elif args.subcommand == 'manipulation-analysis':
        manipulation_analysis(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, cameraPath=args.camerapath, valore_soglia=args.valoresoglia, valore_optout=args.valoreoptout)
    elif args.subcommand == 'camera-analysis':
        cameraControl(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, valoresoglia=args.valoresoglia, valoreoptout=args.valoreoptout)
    elif args.subcommand == 'filter1':
        result = scoreFilter1(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, score=args.score, opFilter=args.operation, operator=args.operator, score2 = args.score2)
        printInColumn(result)
    elif args.subcommand == 'filter2':
        result, previousOccurrence = scoreFilter2(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, score=args.score, opFilter=args.operation, operator=args.operator, score2 = args.score2)
        printInColumn(result)
        print('')
        printInColumn(previousOccurrence)
    elif args.subcommand == 'alloperations':
        allOperations(finalScorePath=args.scorepath, opHistoryPath = args.probehistory)



def mainInterattivo():
    print('Which operation do you want use?')
    print('1) Create json file containing probe history')
    print('2) Manipulation analysis and operations recurrence')
    print('3) Filter1')
    print('4) Filter2')
    print('5) Divison score in optout,matched and no matched')
    print('6) All operations')
    print('7) Camera Analysis')
    print('8) Exit')

    mainScelta = int(input())

    if (mainScelta < 1) or (mainScelta > 7):
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
        print('insert valore di soglia: ')
        valore_soglia = int(input())
        print('insert valore di optout: ')
        valore_optout = int(input())

        manipulation_analysis(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, cameraPath=cameraPath, valore_soglia=valore_soglia, valore_optout=valore_optout)

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
            opFilter = opFilter.split()
    
            if (mainScelta == 3):
                if operator == 'range':
                    result = scoreFilter1(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score = score, opFilter=opFilter, operator=operator, score2 = score2)
                    printInColumn(result)
                else:
                    result = scoreFilter1(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score, opFilter=opFilter, operator=operator)
                    printInColumn(result)

            if (mainScelta == 4):
                if operator == 'range':
                    result = scoreFilter2(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score, opFilter=opFilter, operator=operator,  score2=score2)
                    printInColumn(result)
                else:
                    result,previousOccurrence = scoreFilter2(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score, opFilter=opFilter, operator=operator)
                    printInColumn(previousOccurrence)

    elif (mainScelta == 5):
        print('Insert score path: ')
        finalScorePath = input().strip()
        print('Insert probe history path: ')
        opHistoryPath = input().strip()
        print('Insert camera reference path: ')
        cameraPath = input().strip()
        print('insert valore di soglia: ')
        valore_soglia = int(input())
        print('insert valore di optout: ')
        valore_optout = int(input())
        division(finalScorePath=finalScorePath,opHistoryPath=opHistoryPath,cameraPath=cameraPath,valore_soglia=valore_soglia,valore_optout=valore_optout)

    elif (mainScelta == 6):
        print('Insert score path: ')
        finalScorePath = input().strip()
        print('Insert probe history path: ')
        opHistoryPath = input().strip()
        allOperations(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath)


    elif (mainScelta == 7):
        print('Insert score path: ')
        finalScorePath = input().strip()
        print('Insert probe history path: ')
        opHistoryPath = input().strip()
        print('insert valore di soglia: ')
        valore_soglia = int(input())
        print('insert valore di optout: ')
        valore_optout = int(input())
        cameraControl(finalScorePath=finalScorePath,opHistoryPath=opHistoryPath,valoresoglia=valore_soglia,valoreoptout=valore_optout)

if __name__ == '__main__':
    if sys.argv[1:] != []:
        main()
    else:
        mainInterattivo()

