# abbiamo il json , lo score, e le manipolazioni
# dobbiamo raggruppare per -1 e per i probe che non si trovano nel json

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
	pastValue = A[0]
	if A != None:
		for i in range(len(A)):
			for j in range(len(A)):
				if A[i] == A[j] and i != j:
					check = True
	return check 

def scoreFilter1(scoreMatrix,operations,score,idOperations,function='null',score2 = None):
	duplicateOP = check(idOperations)
	if duplicateOP == False:
		atLeastOneOp = False
		tmp = []
		result = []
		tmpMatrix = []
		atLeastOneOp = False
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

		if function == 'null':
			print('errore,inserire operazioni')

		elif (score != -1) and (score < 0):
			print('errore,valore inserito non corretto')
			return 0


		elif (function == 'equal'):
			for i in range(len(tmpMatrix)):
				if float(tmpMatrix[i][2]) == score:
					tmp.append(tmpMatrix[i][0])
					tmp.append(tmpMatrix[i][1])
					for z in range(len(idoperations)):
						currentOperation = idoperations[z]
						for j in range(len(tmpMatrix[i][3])):
							countOperations = countOperations + 1
							if (currentOperation == tmpMatrix[i][3][j]['name']):
								objPosition = countOperations
								break
						if objPosition != -1:
							tmp.append(currentOperation)
							tmp.append(objPosition)
							atLeastOneOp = True
						objPosition = -1
						countOperations = 0	
					tmp.append('lenght:' + " " +str(len(tmpMatrix[i][3])))
					if atLeastOneOp == True:
						tmpMatrix2.append(tmp)
					tmp = []
					atLeastOneOp = False
			for i in range(len(tmpMatrix2)):
				result.append(tmpMatrix2[i])
			return result


		elif (function) =='over' and (score == -1):
			print('errore,valore inserito non corretto')
			return 0


		elif (function == 'over') and (score >=0):
			for i in range(len(tmpMatrix)):
				if float(tmpMatrix[i][2]) >= score:
					tmp.append(tmpMatrix[i][0])
					tmp.append(tmpMatrix[i][1])
					for z in range(len(idoperations)):
						currentOperation = idoperations[z]
						for j in range(len(tmpMatrix[i][3])):
							countOperations = countOperations + 1
							if (currentOperation == tmpMatrix[i][3][j]['name']):
								objPosition = countOperations
								break
						if objPosition != -1:
							tmp.append(currentOperation)
							tmp.append(objPosition)
							atLeastOneOp = True
						objPosition = -1
						countOperations = 0	
					tmp.append('lenght:' + " " +str(len(tmpMatrix[i][3])))
					tmp.append('score:' + " "+ str((tmpMatrix[i][2])))
					if atLeastOneOp == True:
						tmpMatrix2.append(tmp)
					tmp = []
					atLeastOneOp = False
			for i in range(len(tmpMatrix2)):
				result.append(tmpMatrix2[i])
			return result

		elif (function == 'under') and (score >=0):
			for i in range(len(tmpMatrix)):
				if (float(tmpMatrix[i][2]) < score) and (float(tmpMatrix[i][2]) != -1):
					tmp.append(tmpMatrix[i][0])
					tmp.append(tmpMatrix[i][1])
					for z in range(len(idoperations)):
						currentOperation = idoperations[z]
						for j in range(len(tmpMatrix[i][3])):
							countOperations = countOperations + 1
							if (currentOperation == tmpMatrix[i][3][j]['name']):
								objPosition = countOperations
								break
						if objPosition != -1:
							tmp.append(currentOperation)
							tmp.append(objPosition)
							atLeastOneOp = True
						objPosition = -1
						countOperations = 0	
					tmp.append('lenght:' + " " +str(len(tmpMatrix[i][3])))
					tmp.append('score:' + " "+ str((tmpMatrix[i][2])))
					if atLeastOneOp == True:
						tmpMatrix2.append(tmp)
					tmp = []
					atLeastOneOp = False
			for i in range(len(tmpMatrix2)):
				result.append(tmpMatrix2[i])
			return result

		elif (function == 'range') and (score2 != None) and (score2 >= 0):
			for i in range(len(tmpMatrix)):
				if (float(tmpMatrix[i][2]) >= score) and (float(tmpMatrix[i][2]) <= score2):
					tmp.append(tmpMatrix[i][0])
					tmp.append(tmpMatrix[i][1])
					for z in range(len(idoperations)):
						currentOperation = idoperations[z]
						for j in range(len(tmpMatrix[i][3])):
							countOperations = countOperations + 1
							if (currentOperation == tmpMatrix[i][3][j]['name']):
								objPosition = countOperations
								break
						if objPosition != -1:
							tmp.append(currentOperation)
							tmp.append(objPosition)
							atLeastOneOp = True
						objPosition = -1
						countOperations = 0	
					tmp.append('lenght:' + " " +str(len(tmpMatrix[i][3])))
					tmp.append('score:' + " "+ str((tmpMatrix[i][2])))
					if atLeastOneOp == True:
						tmpMatrix2.append(tmp)
					tmp = []
					atLeastOneOp = False
			for i in range(len(tmpMatrix2)):
				result.append(tmpMatrix2[i])
			return result

		elif (function == 'range') and (score2 == None or score2 <0):
			print('dashara ritenta')
			return 0

		elif (function == 'under') and (score == -1):
			print('Error')
			return 0
	else:
		print('errore,operazioni duplicate inserite')
		return 0

def scoreFilter2(scoreMatrix,operations,score,idOperations,function = 'null',maxPreviousOp = 0,score2 = None):

	duplicateOP = check(idOperations)

	if duplicateOP == False:
		atLeastOneOp = False
		tmp = []
		tmpResult = []
		result = []
		tmpMatrix = []
		match = False
		found = False
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
		tmpOp = [] 
		countOperations = 0

		if function == 'null':
			print('errore,inserire operazioni')

		elif (score != -1) and (score < 0):
			print('errore,inserire parametri corretti')
			return 0

		elif (function == 'equal'):
			for i in range(len(tmpMatrix)):
				if float(tmpMatrix[i][2]) == score:
					tmpResult.append(tmpMatrix[i][0])
					for z in range(len(idoperations)):
						currentOperation = idoperations[z]
						for j in range(len(tmpMatrix[i][3])):
							if tmpMatrix[i][3][j]['name'] != currentOperation:
								countOperations = countOperations + 1
								if countOperations <= maxPreviousOp:
									tmpOp.append(tmpMatrix[i][3][j]['name'])
							else:
								found = True
								break
						if found == True:
							tmp.append(currentOperation)
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


		elif (function == 'over') and (score == -1):
			print('errore,inserire parametri corretti')
			return 0

		elif (function == 'over') and (score >= 0):
			for i in range(len(tmpMatrix)):
				if float(tmpMatrix[i][2]) >= score:
					tmpResult.append(tmpMatrix[i][0])
					for z in range(len(idoperations)):
						currentOperation = idoperations[z]
						for j in range(len(tmpMatrix[i][3])):
							if tmpMatrix[i][3][j]['name'] != currentOperation:
								countOperations = countOperations + 1
								if countOperations <= maxPreviousOp:
									tmpOp.append(tmpMatrix[i][3][j]['name'])
							else:
								found = True
								break
						if found == True:
							tmp.append(currentOperation)
							tmp.append(tmpOp)
							tmp.append(countOperations)
							tmpResult.append(tmp)
							atLeastOneOp = True
						tmp = []
						tmpOp = []
						countOperations = 0
						found =  False
					tmpResult.append('score:'+''+ tmpMatrix[i][2])
					if atLeastOneOp == True: 
						result.append(tmpResult)
					tmpResult = []
					atLeastOneOp = False

		elif (function == 'under') and (score >= 0):
			for i in range(len(tmpMatrix)):
				if float(tmpMatrix[i][2]) < score and (float(tmpMatrix[i][2]) != -1):
					tmpResult.append(tmpMatrix[i][0])
					for z in range(len(idoperations)):
						currentOperation = idoperations[z]
						for j in range(len(tmpMatrix[i][3])):
							if tmpMatrix[i][3][j]['name'] != currentOperation:
								countOperations = countOperations + 1
								if countOperations <= maxPreviousOp:
									tmpOp.append(tmpMatrix[i][3][j]['name'])
							else:
								found = True
								break
						if found == True:
							tmp.append(currentOperation)
							tmp.append(tmpOp)
							tmp.append(countOperations)
							tmp.append(tmpMatrix[i][2])
							tmpResult.append(tmp)
							atLeastOneOp = True
						tmp = []
						tmpOp = []
						countOperations = 0
						found =  False
					tmpResult.append('score:'+''+ tmpMatrix[i][2])
					if atLeastOneOp == True: 
						result.append(tmpResult)
					tmpResult = []
					atLeastOneOp = False

		elif (function == 'range') and (score2 != None) and (score2 >= 0):
			for i in range(len(tmpMatrix)):
				if float(tmpMatrix[i][2]) >= score and (float(tmpMatrix[i][2]) <= score2):
					tmpResult.append(tmpMatrix[i][0])
					for z in range(len(idoperations)):
						currentOperation = idoperations[z]
						for j in range(len(tmpMatrix[i][3])):
							if tmpMatrix[i][3][j]['name'] != currentOperation:
								countOperations = countOperations + 1
								if countOperations <= maxPreviousOp:
									tmpOp.append(tmpMatrix[i][3][j]['name'])
							else:
								found = True
								break
						if found == True:
							tmp.append(currentOperation)
							tmp.append(tmpOp)
							tmp.append(countOperations)
							tmpResult.append(tmp)
							atLeastOneOp = True
						tmp = []
						tmpOp = []
						countOperations = 0
						found =  False
					tmpResult.append('score:'+''+ tmpMatrix[i][2])
					if atLeastOneOp == True: 
						result.append(tmpResult)
					tmpResult = []
					atLeastOneOp = False

		elif (function == 'range') and (score2 == None or score2 <0):
			print('errore,inserire parametri corretti')
			return 0

		elif (function == 'under') and (score == -1):
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
# Leggo json
with open('./myoperations.json') as f:
	data = json.load(f)
# Leggo csv FinalScores
A = CSVreader('./FinalScores/UnifiPRNUTime_1_CameraVideoVideo.csv')
A.remove(A[0])  #Rimuovo l'intestazione
# Leggo csv ManipReference
B = CSVreader('./Reference/MFC18_EvalPart1-camera-ref.csv')
B.remove(B[0]) #Rimuovo l'intestazione
with open('./Reference/operations.json') as f:
	data2 = json.load(f)

score =  20
idoperations = ['OutputAVI','AntiForensicCopyExif']

result2 = scoreFilter1(A,data,score,idoperations,'over')
result3 = scoreFilter2(A,data,score,idoperations,'over',maxPreviousOp = 3,score2 = 3333)
printInColumn(result2)
print("")
print("")
print(len(result2))
print("")
print("")
printInColumn(result3)
print("")
print("")
print(len(result3))



