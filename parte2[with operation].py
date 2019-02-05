# abbiamo il json , lo score, e le manipolazioni
# dobbiamo raggruppare per -1 e per i probe che non si trovano nel json

import csv
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter

def CSVreader(path):
	with open(path) as f:
		reader = csv.reader(f,delimiter=';', quoting=csv.QUOTE_NONE)
		rows = []
		for row in reader:
			rows.append(row)
	return rows

def printInColumn(A):
	for i in range(len(A)):
		print(A[i])


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

# Leggo json
with open('./json/myoperations.json') as f:
	data = json.load(f)

# Leggo csv FinalScores
A = CSVreader('./FinalScores/UnifiPRNUTime_1_CameraVideoImg.csv')
A.remove(A[0])  #Rimuovo l'intestazione
# Leggo csv ManipReference
B = CSVreader('./ManipReference/MFC18_EvalPart1-camera-ref.csv')
B.remove(B[0]) #Rimuovo l'intestazione

# Conto doppioni in A
duplicati = 0
tot_duplicati = 0
countFinal = []
for i in range(len(A)):
	duplicati = 0
	for j in range(len(A)):
		if (A[i][0] == A[j][0]) and (i != j):
			duplicati = duplicati + 1
	tot_duplicati = tot_duplicati + duplicati
	countFinal.append([duplicati,A[i][0]])
#print(tot_duplicati)


# Matrice contenente: ProbeID,score=-1
scoreMatrix_one = []
# Matrice contente ProbeID,score!=-1
scoreMatrix_no_one = []
# Matrice contenente i ProbeID che non si trovano nel json
noJSON = []
tmp = []
count = 0
match = False
for i in range(len(A)):
	for j in range(len(data['probesFileID'])):
		if A[i][0] == data['probesFileID'][j]['probeID']:
			match = True
			if A[i][3] == '-1':
				tmp.append(A[i][0])
				tmp.append(A[i][1])
				tmp.append(A[i][3])
				scoreMatrix_one.append(tmp)
				tmp = []
			else:
				tmp.append(A[i][0])
				tmp.append(A[i][1])
				tmp.append(A[i][3])
				scoreMatrix_no_one.append(tmp)
				tmp = []

	if match == False:
		count = count + 1
		tmp.append(A[i][0])
		tmp.append(A[i][1])
		tmp.append(A[i][3])
		noJSON.append(tmp)
		tmp = []
	match = False

# Matrice globale contente: ProbeID,score
global_score = scoreMatrix_one + scoreMatrix_no_one + noJSON
g_s = []
g_s.append(scoreMatrix_one)
g_s.append(scoreMatrix_no_one)
g_s.append(noJSON)


tmp3 = []

# print('Numero di ProbeID nel CSV: ', len(global_score))
# print('Numero di ProbeID nel JSON: ',len(data['probesFileID']))
# print('Numero di ProbeID non trovati nel JSON: ',count)
# print("")


# scoreMatrix_one è una matrice contenente: ProbeID,score=-1,isManipulated/notManipulated raggruppata per Y(yes is manipulated)
X = []
Y = []
for i in range(len(scoreMatrix_one)):
	for j in range(len(B)):
		if(scoreMatrix_one[i][0] == B[j][1]) and (scoreMatrix_one[i][1] == B[j][3]):
			tmp.append(scoreMatrix_one[i][0])
			tmp.append(scoreMatrix_one[i][1])
			tmp.append(scoreMatrix_one[i][2])
			tmp.append(B[j][5])
			if (B[j][5]) == 'Y':
				X.append(tmp)
			else:
				Y.append(tmp)
			tmp = []
scoreMatrix_one = X+Y


# scoreMatrix_no_one è una matrice contenente: ProbeID,score!=-1,isManipulated/notManipulated raggruppata per Y(yes is manipulated)
X = []
Y = []
for i in range(len(scoreMatrix_no_one)):
	for j in range(len(B)):
		if(scoreMatrix_no_one[i][0] == B[j][1]) and (scoreMatrix_no_one[i][1] == B[j][3]):
			tmp.append(scoreMatrix_no_one[i][0])
			tmp.append(scoreMatrix_no_one[i][1])
			tmp.append(scoreMatrix_no_one[i][2])
			tmp.append(B[j][5])
			if (float(scoreMatrix_no_one[i][2]) >= 50):
				tmp.append('MATCHED')
			else:
				tmp.append('NOMATCHED')
			if (B[j][5]) == 'Y':
				X.append(tmp)
			else:
				Y.append(tmp)
			tmp = []
scoreMatrix_no_one = X+Y


# noJSON è una matrice contenente: ProbeID,score,isManipulated/notManipulated raggruppata per Y(yes is manipulated)
X = []
Y = []
for i in range(len(noJSON)):
	for j in range(len(B)):
		if(noJSON[i][0] == B[j][1]) and (noJSON[i][1] == B[j][3]):
			tmp.append(noJSON[i][0])
			tmp.append(noJSON[i][1])
			tmp.append(noJSON[i][2])
			tmp.append(B[j][5])
			if (B[j][5]) == 'Y':
				X.append(tmp)
			else:
				Y.append(tmp)
			tmp = []
noJSON = X+Y



finalMatrix = []

finalMatrix.append(scoreMatrix_one)
finalMatrix.append(scoreMatrix_no_one)
finalMatrix.append(noJSON)


# ANALISI di noJSON
# W = Probe che non sono nel JSON ma sono manipolati
# U = Probe che non sono nel JSON e sono manipolati
W = []
U = []
for i in range(len(noJSON)):
	for j in range(len(B)):
		if(noJSON[i][0] == B[j][1]):
			tmp.append(noJSON[i][0])
			tmp.append(noJSON[i][1])
			tmp.append(noJSON[i][2])
			tmp.append(B[j][5])
			if (B[j][5]) == 'Y':
				W.append(tmp)
			else:
				U.append(tmp)
			tmp = []

# ANALISI di scoreMatrix_no_one
MATCHED = []
NOMATCHED = []
for i in range(len(scoreMatrix_no_one)):
	if (float(scoreMatrix_no_one[i][2]) >= 50):
		MATCHED.append(scoreMatrix_no_one[i])
	else:
		NOMATCHED.append(scoreMatrix_no_one[i])


tmp2 = []
scoreOperations_one = []
for i in range(len(scoreMatrix_one)):	
	for j in range(len(data['probesFileID'])):
		if scoreMatrix_one[i][0] == data['probesFileID'][j]['probeID']:
			tmp2.append(scoreMatrix_one[i][0])
			tmp2.append(scoreMatrix_one[i][1])
			tmp2.append(scoreMatrix_one[i][2])
			tmp2.append(scoreMatrix_one[i][3])
			tmp2.append(data['probesFileID'][j]['operations'])
			scoreOperations_one.append(tmp2)
			tmp2 = []

scoreOperations_no_one = []
for i in range(len(scoreMatrix_no_one)):	
	for j in range(len(data['probesFileID'])):
		if scoreMatrix_no_one[i][0] == data['probesFileID'][j]['probeID']:
			tmp2.append(scoreMatrix_no_one[i][0])
			tmp2.append(scoreMatrix_no_one[i][1])
			tmp2.append(scoreMatrix_no_one[i][2])
			tmp2.append(scoreMatrix_no_one[i][3])
			tmp2.append(scoreMatrix_no_one[i][4])
			tmp2.append(data['probesFileID'][j]['operations'])
			scoreOperations_no_one.append(tmp2)
			tmp2 = []

countOp =  0
tmp4 =  []
repeatOp_no_one = []
with open('./json/operations.json') as f:
	data2 = json.load(f)



###numero di volte in cui le operazioni si ripetono nelle matrici 
for k in range(len(data2['operations'])):
	for i in range(len(scoreOperations_no_one)):
		for j in range(len( scoreOperations_no_one[i][5])):
			if data2['operations'][k]['name'] == scoreOperations_no_one[i][5][j]['name']:
				countOp =  countOp + 1
	if countOp > 0:
		tmp4.append(data2['operations'][k]['name'])
		tmp4.append(countOp)			
		repeatOp_no_one.append(tmp4)
	countOp = 0
	tmp4 = []

#print(repeatOp_no_one)


tmp4 = []
countOp = 0
repeatOp_one = []

for k in range(len(data2['operations'])):
	for i in range(len(scoreOperations_one)):
		for j in range(len(scoreOperations_one[i][4])):
			if data2['operations'][k]['name'] == scoreOperations_one[i][4][j]['name']:
				countOp =  countOp + 1
	if countOp > 0:
		tmp4.append(data2['operations'][k]['name'])
		tmp4.append(countOp)			
		repeatOp_one.append(tmp4)
	countOp = 0
	tmp4 = []


repeatOp_oneSorted = sortScoreMatrix(repeatOp_one)
repeatOp_no_oneSorted = sortScoreMatrix(repeatOp_no_one)

print(repeatOp_oneSorted)
print("")
print("")
print(repeatOp_no_oneSorted)

x = []
y = []
for i in  range(len(repeatOp_oneSorted)):
	x.append(repeatOp_oneSorted[i][0])
	y.append(repeatOp_oneSorted[i][1])


# centers = range(len(x))
# plt.bar(centers,y,align='center', tick_label= x)
# plt.show()

