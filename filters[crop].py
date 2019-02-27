import csv
import json

def printInColumn(A):
    if A != None:
        for i in range(len(A)):
            print(A[i])
    else:
        print('None')


def CSVreader(path):
	with open(path) as f:
		reader = csv.reader(f,delimiter='|', quoting=csv.QUOTE_NONE)
		rows = []
		for row in reader:
			rows.append(row)
	return rows
def check(A):
	check = False
	if A != None:
		for i in range(len(A)):
			for j in range(len(A)):
				if A[i] == A[j] and i != j:
					check = True
	return check 

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

def scoreFilter2(finalScorePath, opHistoryPath, score, opFilter, operator ='null', maxPreviousOp = 0, score2 = None):
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

        tmp = []
        tmpOp = []
        countOperations = 0

        if operator == 'null':
            print('errore,inserire operazioni')

        elif (score != -1) and (score < 0):
            print('errore,inserire parametri corretti')
            return 0

        elif (operator == 'equal'):
            for i in range(len(tmpMatrix)):
                if float(tmpMatrix[i][1]) == score:
                    tmpResult.append(tmpMatrix[i][0])
                    for z in range(len(opFilter)):
                        currentOperation = opFilter[z]
                        for j in range(len(tmpMatrix[i][2])):
                            if tmpMatrix[i][2][j]['name'].lower() != currentOperation:
                                countOperations = countOperations + 1
                                if countOperations <= maxPreviousOp:
                                    tmpOp.append(tmpMatrix[i][2][j]['name'])
                            else:
                                found = True
                                break
                        if found == True:
                            tmp.append(tmpMatrix[i][2][j]['name'])
                            tmp.append(tmpOp)
                            tmp.append(countOperations)
                            tmpResult.append(tmp)
                            atLeastOneOp = True
                        tmp = []
                        tmpOp = []
                        countOperations = 0
                        found =  False
                    if atLeastOneOp == True:
                        result.append(tmpResult)
                    tmpResult = []
                    atLeastOneOp = False


        elif (operator == 'over') and (score == -1):
            print('errore,inserire parametri corretti')
            return 0

        elif (operator == 'over') and (score >= 0):
            for i in range(len(tmpMatrix)):
                if float(tmpMatrix[i][1]) >= score:
                    tmpResult.append(tmpMatrix[i][0])
                    for z in range(len(opFilter)):
                        currentOperation = opFilter[z]
                        for j in range(len(tmpMatrix[i][2])):
                            if tmpMatrix[i][2][j]['name'].lower() != currentOperation:
                                countOperations = countOperations + 1
                                if countOperations <= maxPreviousOp:
                                    tmpOp.append(tmpMatrix[i][2][j]['name'])
                            else:
                                found = True
                                break
                        if found == True:
                            tmp.append(tmpMatrix[i][2][j]['name'])
                            tmp.append(tmpOp)
                            tmp.append(countOperations)
                            tmpResult.append(tmp)
                            atLeastOneOp = True
                        tmp = []
                        tmpOp = []
                        countOperations = 0
                        found =  False
                    tmpResult.append('score:'+''+ tmpMatrix[i][1])
                    if atLeastOneOp == True:
                        result.append(tmpResult)
                    tmpResult = []
                    atLeastOneOp = False

        elif (operator == 'under') and (score >= 0):
            for i in range(len(tmpMatrix)):
                if float(tmpMatrix[i][1]) < score and (float(tmpMatrix[i][1]) != -1):
                    tmpResult.append(tmpMatrix[i][0])
                    for z in range(len(opFilter)):
                        currentOperation = opFilter[z]
                        for j in range(len(tmpMatrix[i][2])):
                            if tmpMatrix[i][2][j]['name'].lower() != currentOperation:
                                countOperations = countOperations + 1
                                if countOperations <= maxPreviousOp:
                                    tmpOp.append(tmpMatrix[i][2][j]['name'])
                            else:
                                found = True
                                break
                        if found == True:
                            tmp.append(tmpMatrix[i][2][j]['name'])
                            tmp.append(tmpOp)
                            tmp.append(countOperations)
                            tmpResult.append(tmp)
                            atLeastOneOp = True
                        tmp = []
                        tmpOp = []
                        countOperations = 0
                        found =  False
                    tmpResult.append('score:'+''+ tmpMatrix[i][1])
                    if atLeastOneOp == True:
                        result.append(tmpResult)
                    tmpResult = []
                    atLeastOneOp = False

        elif (operator == 'range') and (score2 != None) and (score2 >= 0):
            for i in range(len(tmpMatrix)):
                if float(tmpMatrix[i][1]) >= score and (float(tmpMatrix[i][1]) <= score2):
                    tmpResult.append(tmpMatrix[i][0])
                    for z in range(len(opFilter)):
                        currentOperation = opFilter[z]
                        for j in range(len(tmpMatrix[i][2])):
                            if tmpMatrix[i][2][j]['name'].lower() != currentOperation:
                                countOperations = countOperations + 1
                                if countOperations <= maxPreviousOp:
                                    tmpOp.append(tmpMatrix[i][2][j]['name'])
                            else:
                                found = True
                                break
                        if found == True:
                            tmp.append(tmpMatrix[i][2][j]['name'])
                            tmp.append(tmpOp)
                            tmp.append(countOperations)
                            tmpResult.append(tmp)
                            atLeastOneOp = True
                        tmp = []
                        tmpOp = []
                        countOperations = 0
                        found =  False
                    tmpResult.append('score:'+''+ tmpMatrix[i][1])
                    if atLeastOneOp == True:
                        result.append(tmpResult)
                    tmpResult = []
                    atLeastOneOp = False

        elif (operator == 'range') and (score2 == None or score2 < 0):
            print('errore,inserire parametri corretti')
            return 0

        elif (operator == 'under') and (score == -1):
            print('errore,inserire parametri corretti')
            return 0

        if result != []:
            for i in range(len(result)):
                for j in range(1,len(result[i])):
                    if result[i][j][2] == 0:
                        result[i][j][2] = 'first Operation'
        return result
    else:
        print('errore,operazioni duplicate inserite')
        return 0


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

# Leggo json
# Leggo csv FinalScores
A = './FinalScores/UnifiGLCM_1_GANImageCrop.csv'
data = './myoperations.json'
# for i in range(len(A[0])):
# 	if A[0][i] == 'ConfidenceScore':
# 		print (i)
# A.remove(A[0])  #Rimuovo l'intestazione
# Leggo csv ManipReference
with open('./Reference/operations.json') as f:
	data2 = json.load(f)


score =  -1

idoperations = ['AntiForensicJPGCompression']
allOperations(A,data)
result2 = scoreFilter1(A,data,score,idoperations,'equal',score2 = 0.456639)

printInColumn(result2)




