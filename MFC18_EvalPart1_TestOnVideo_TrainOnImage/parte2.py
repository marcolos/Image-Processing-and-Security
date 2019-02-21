# abbiamo il json , lo score, e le manipolazioni
# dobbiamo raggruppare per -1 e per i probe che non si trovano nel json

import csv
import json
import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# from collections import Counter

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
with open('./myoperations.json') as f:
	data = json.load(f)

# Leggo csv FinalScores
A = CSVreader('./FinalScores/UnifiPRNUTime_1_CameraVideoImg.csv')
A.remove(A[0])  #Rimuovo l'intestazione
# Leggo csv ManipReference
B = CSVreader('./Reference/MFC18_EvalPart1-camera-ref.csv')
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
#print(countFinal)

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
print('Numero di ProbeID nel CSV score: ', len(A))
print('Numero di ProbeID nel JSON: ',len(data['probesFileID']))
print("")
print('Numero di ProbeID che matchano nel JSON: ',len(scoreMatrix_one)+len(scoreMatrix_no_one))
print('Numero di ProbeID non trovati nel JSON: ',count)
print("")


# scoreMatrix_one è una matrice contenente: ProbeID,score=-1,isManipulated/notManipulated raggruppata per Y(yes is manipulated)
X = []
Y = []
for i in range(len(scoreMatrix_one)):
	for j in range(len(B)):
		if((scoreMatrix_one[i][0] == B[j][1]) and (scoreMatrix_one[i][1]) == B[j][3]):
			tmp.append(scoreMatrix_one[i][0])
			tmp.append(scoreMatrix_one[i][1])
			tmp.append(scoreMatrix_one[i][2])
			tmp.append(B[j][5])
			tmp.append(B[j][2].split(".",1)[1])
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
		if((scoreMatrix_no_one[i][0] == B[j][1]) and (scoreMatrix_no_one[i][1]) == B[j][3]):
			tmp.append(scoreMatrix_no_one[i][0])
			tmp.append(scoreMatrix_no_one[i][1])
			tmp.append(scoreMatrix_no_one[i][2])
			tmp.append(B[j][5])
			tmp.append(B[j][2].split(".", 1)[1])
			if (B[j][5]) == 'Y':
				X.append(tmp)
			else:
				Y.append(tmp)
			tmp = []
scoreMatrix_no_one = X+Y

# ANALISI di scoreMatrix_no_one
MATCHED = []
NOMATCHED = []
for i in range(len(scoreMatrix_no_one)):
	if (float(scoreMatrix_no_one[i][2]) >= 50):
		MATCHED.append(scoreMatrix_no_one[i])
	else:
		NOMATCHED.append(scoreMatrix_no_one[i])


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
			if (B[j][5]) == 'Y':
				X.append(tmp)
			else:
				Y.append(tmp)
			tmp = []
noJSON = X+Y

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
			tmp.append(B[j][2].split(".", 1)[1])
			if (B[j][5]) == 'Y':
				W.append(tmp)
			else:
				U.append(tmp)
			tmp = []
#print(W)



# Controllo se i probe noJSON sono presenti nel journal
# probe_journal_join_csv = CSVreader('./Reference/probejournaljoin.csv')
# probe_journal_join_csv.remove(probe_journal_join_csv[0])
# count = 0
# for i in range(len(probe_journal_join_csv)):
# 	for j in range(len(noJSON)):
# 		if probe_journal_join_csv[i][0] == noJSON[j][0]:
# 			count = count + 1
# print(count)


'''Conteggio ricorrenza operazioni in scoreMatrix_one, scoreMatrix_no_one_matched, scoreMatrix_no_one_no_matched'''
tmp = []
scoreOperations_one = []
for i in range(len(scoreMatrix_one)):
	for j in range(len(data['probesFileID'])):
		if scoreMatrix_one[i][0] == data['probesFileID'][j]['probeID']:
			tmp.append(scoreMatrix_one[i][0])
			tmp.append(scoreMatrix_one[i][1])
			tmp.append(scoreMatrix_one[i][2])
			tmp.append(scoreMatrix_one[i][3])
			tmp.append(data['probesFileID'][j]['operations'])
			scoreOperations_one.append(tmp)
			tmp = []

tmp = []
scoreOperations_no_one_matched = []
for i in range(len(MATCHED)):
	for j in range(len(data['probesFileID'])):
		if MATCHED[i][0] == data['probesFileID'][j]['probeID']:
			tmp.append(MATCHED[i][0])
			tmp.append(MATCHED[i][1])
			tmp.append(MATCHED[i][2])
			tmp.append(MATCHED[i][3])
			tmp.append(data['probesFileID'][j]['operations'])
			scoreOperations_no_one_matched.append(tmp)
			tmp = []

tmp = []
scoreOperations_no_one_no_matched = []
for i in range(len(NOMATCHED)):
	for j in range(len(data['probesFileID'])):
		if NOMATCHED[i][0] == data['probesFileID'][j]['probeID']:
			tmp.append(NOMATCHED[i][0])
			tmp.append(NOMATCHED[i][1])
			tmp.append(NOMATCHED[i][2])
			tmp.append(NOMATCHED[i][3])
			tmp.append(data['probesFileID'][j]['operations'])
			scoreOperations_no_one_no_matched.append(tmp)
			tmp = []


countOp =  0
tmp =  []
repeatOp_matched = []
with open('./Reference/operations.json') as f:
	data2 = json.load(f)
#numero di volte in cui le operazioni si ripetono nelle matrici
for k in range(len(data2['operations'])):
	for i in range(len(scoreOperations_no_one_matched)):
		for j in range(len( scoreOperations_no_one_matched[i][4])):
			if data2['operations'][k]['name'] == scoreOperations_no_one_matched[i][4][j]['name']:
				countOp =  countOp + 1
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
				countOp =  countOp + 1
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
				countOp =  countOp + 1
				break
	if countOp > 0:
		tmp.append(data2['operations'][k]['name'])
		tmp.append(countOp)
		repeatOp_one.append(tmp)
	countOp = 0
	tmp = []

repeatOp_oneSorted = sortScoreMatrix(repeatOp_one)
repeatOp_no_MatchedSorted = sortScoreMatrix(repeatOp_noMatched)
repeatOp_matchedSorted = sortScoreMatrix(repeatOp_matched)
# print(repeatOp_oneSorted)
# print("")
# print(repeatOp_no_MatchedSorted)
# print("")
# print(repeatOp_matchedSorted)

'''PLOT
x = []
y = []
for i in range(4):
	x.append(repeatOp_oneSorted[i][0])
	y.append(repeatOp_oneSorted[i][1])
centers = range(len(x))
plt.bar(centers,y,align='center', tick_label= x)
plt.show()
'''

count = 0
for i in range(len(scoreMatrix_one)):
	if scoreMatrix_one[i][4] == "mts":
		count = count +1
#print(count)



with open('./one.json', 'w') as fp:
	json.dump(scoreOperations_one, fp, indent = 4, ensure_ascii = False)


with open('./no_one_matched.json', 'w') as fp:
	json.dump(scoreOperations_no_one_matched, fp, indent = 4, ensure_ascii = False)


with open('./no_one_no_matched.json', 'w') as fp:
	json.dump(scoreOperations_no_one_no_matched, fp, indent = 4, ensure_ascii = False)


print(repeatOp_one)
print("")
print(repeatOp_matchedSorted)


trovato = False
for i in range(len(repeatOp_one)):
	for j in range(len(repeatOp_matchedSorted)):
		if(repeatOp_one[i][0]) ==(repeatOp_matchedSorted[j][0]):
			trovato = True
	if trovato == False:
		print(repeatOp_one[i][0])
	trovato = False




# PLOT
# x = []
# y = []
# for i in  range(len(repeatOp_oneSorted)):
# 	x.append(repeatOp_oneSorted[i][0])
# 	y.append(repeatOp_oneSorted[i][1])
# centers = range(len(x))
# plt.bar(centers,y,align='center', tick_label= x)
# plt.show()


#print(scoreMatrix_one)

print(repeatOp_no_MatchedSorted)
print("")
print(repeatOp_matchedSorted)



# # MAIN
# if sys.argv[1:] != []:
#     # construct the argument parse and parse the arguments
#     ap = argparse.ArgumentParser(
#         description='Filtro1: Ci da le Probe che hanno l operazione in input con la loro posizione e il numero tot di operazioni fatti nella probe \n\n Filtro2: ... ')
#     ap.add_argument("-f", "--filter", type=int, required=True,
#                     help="type of filter that you want use: insert 1 to use filter1 or 2 to use filter2")
#     ap.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
#     ap.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
#     ap.add_argument("-s", "--score", required=True, type=int, help="insert score")
#     ap.add_argument("-op", "--operator", required=True, help="insert operator like over,under,equal")
#     ap.add_argument("-o", "--operation", required=True, help="insert operation filter")
#     ap.add_argument("-po", "--prevop", type=int, required=False, help="insert preview operations")
#     args = vars(ap.parse_args())
#
#     # save value from command line
#     sceltaFiltro = args["filter"]
#     sp = args["scorepath"]
#     hp = args["probehistory"]
#     score = args["score"]
#     operator = args["operator"]
#     opFilter = args["operation"]
#     if sceltaFiltro == 2:
#         prevOp = args['prevop']
#         if prevOp == None:
#             print('To use filter2 you must insert the preview operations numbers also')
#             sys.exit()
#     go()
#