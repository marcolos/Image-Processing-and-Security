import csv
import json
import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# from collections import Counter
#'./probeHistory.json'
#'./FinalScores/UnifiPRNUTime_1_CameraVideoImg.csv'
#'./Reference/MFC18_EvalPart1-camera-ref.csv'
def CSVreader(path):
	with open(path) as f:
		reader = csv.reader(f,delimiter='|', quoting=csv.QUOTE_NONE)
		rows = []
		for row in reader:
			rows.append(row)
	return rows

def printInColumn(A):
	for i in range(len(A)):
		print(A[i])

def findNOJSON(scorePath,ReferencePath,opHistoryPath):

	# Leggo json
	with open(opHistoryPath) as f:
		data = json.load(f)

	# Leggo csv FinalScores
	A = CSVreader(scorePath)
	A.remove(A[0])  #Rimuovo l'intestazione
	# Leggo csv ManipReference
	B = CSVreader(ReferencePath)
	B.remove(B[0]) #Rimuovo l'intestazione

	noJSON = []
	tmp = []
	count = 0
	match = False
	for i in range(len(A)):
		for j in range(len(data['probesFileID'])):
			if A[i][0] == data['probesFileID'][j]['probeID']:
				match = True
		if match == False:
			count = count + 1
			tmp.append(A[i][0])
			tmp.append(A[i][1])
			tmp.append(A[i][3])
			noJSON.append(tmp)
			tmp = []
		match = False

	# noJSON è una matrice contenente: ProbeID,score,isManipulated/notManipulated raggruppata per Y(yes is manipulated)
	X = []
	Y = []
	for i in range(len(noJSON)):
		for j in range(len(B)):
			if((noJSON[i][0] == B[j][1]) and (noJSON[i][1]) == B[j][3]):
				tmp.append(noJSON[i][0])
				tmp.append(noJSON[i][1])
				tmp.append(noJSON[i][2])
				tmp.append(B[j][5])
				tmp.append(B[j][2].split(".", 1)[1])
				if (B[j][5]) == 'Y':
					X.append(tmp)
				else:
					Y.append(tmp)
				tmp = []
	noJSON = X+Y

	return noJSON

def NoJsonAnalyze(noJSON,optout,threshold,target):
	countOptout = 0
	countOverThresh = 0
	countUnderTresh = 0
	countTarget = 0
	countOptTarget = 0
	countUnderTreshTarget = 0
	countOverThreshTarget = 0 

	for i in range(len(noJSON)):
		if noJSON[i][4] == target:
			countTarget = countTarget + 1
		if float(noJSON[i][2]) == optout:
			countOptout = countOptout + 1
			if noJSON[i][4] == target:
				countOptTarget = countOptTarget + 1
		elif float(noJSON[i][2]) >= threshold:
			countOverThresh = countOverThresh + 1
			if noJSON[i][4] == target:
				countOverThreshTarget = countOverThreshTarget + 1			
		elif (float(noJSON[i][2])) < threshold and (float(noJSON[i][2]))>= 0:
			countUnderTresh = countUnderTresh + 1
			if noJSON[i][4] == target:
				countUnderTreshTarget = countUnderTreshTarget + 1	

	print('numero elementi totali non trovati nel file JSON:  ',len(noJSON))
	print("")
	print('numero elementi non trovati nel file JSON con formato '+target+':',str(countTarget))
	print("")
	print('numero elementi non trovati nel file JSON con score uguale al valore optout '+ str(optout) +': '+ str(countOptout)+', avente inoltre formato '+target+' '+str(countOptTarget))
	print("")
	print('numero elementi non trovati nel file JSON con score maggiore o uguale del valore soglia '+ str(threshold) +': '+ str(countOverThresh)+', avente inoltre formato '+target+' '+ str(countOverThreshTarget))
	print("")
	print('numero elementi non trovati nel file JSON con score minore del valore soglia '+ str(threshold) +': '+ str(countUnderTresh)+', avente inoltre formato '+target+' '+ str(countUnderTreshTarget))
	print("")

noJSON = findNOJSON('./FinalScores/UnifiPRNUTime_1_CameraVideoImg.csv','./Reference/MFC18_EvalPart1-camera-ref.csv','./probeHistory.json')
NoJsonAnalyze(noJSON,-1,50,'mts')
print(len(noJSON))

#