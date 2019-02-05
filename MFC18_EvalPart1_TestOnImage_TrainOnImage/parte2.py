# abbiamo il json , lo score, e le manipolazioni
# dobbiamo raggruppare per -1 e per i probe che non si trovano nel json

import csv
import json

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
# g_s = []
# g_s.append(scoreMatrix_one)
# g_s.append(scoreMatrix_no_one)
# g_s.append(noJSON)


print('Numero di ProbeID nel CSV score: ', len(global_score))
print('Numero di ProbeID nel JSON: ',len(data['probesFileID']))
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
			if (B[j][5]) == 'Y':
				W.append(tmp)
			else:
				U.append(tmp)
			tmp = []
#print(W)


# ANALISI di scoreMatrix_no_one
MATCHED = []
NOMATCHED = []
for i in range(len(scoreMatrix_no_one)):
	if (float(scoreMatrix_no_one[i][2]) <= 50):
		MATCHED.append(scoreMatrix_no_one[i])
	else:
		NOMATCHED.append(scoreMatrix_no_one[i])



finalMatrix = []
finalMatrix.append(scoreMatrix_one)
finalMatrix.append(scoreMatrix_no_one)
finalMatrix.append(noJSON)
#print(finalMatrix[0])  # Stampa scoreMatrix_one
#print(finalMatrix[1])  # Stampa scoreMatrix_no_one
#print(finalMatrix[2])  # Stampa noJSON

probe_journal_join_csv = CSVreader('./Reference/probejournaljoin.csv')
probe_journal_join_csv.remove(probe_journal_join_csv[0])

count = 0
for i in range(len(probe_journal_join_csv)):
	for j in range(len(noJSON)):
		if probe_journal_join_csv[i][0] == noJSON[j][0]:
			count = count + 1
print(boa)
