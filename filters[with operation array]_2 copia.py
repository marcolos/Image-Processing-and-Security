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
	if A != None:
		for i in range(len(A)):
			for j in range(len(A)):
				if A[i] == A[j] and i != j:
					check = True
	return check 
def sortScoreMatrix(matrix):
    for i in range(len(matrix)):
        for k in range(i,len(matrix)):
            if matrix[i][1] < matrix[k][1]:
                tmpRows = matrix[i]
                matrix[i] = matrix[k]
                matrix[k] = tmpRows
    return matrix
def operations_recurrence(finalScorePath,opHistoryPath,valore_soglia, valore_optout):
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
                    tmp.append(scoreMatrix[i][0])  #Probe
                    tmp.append(scoreMatrix[i][3])  #Score
                    scoreMatrix_opt.append(tmp)  # Probe|Score
                    tmp = []
                else:
                    tmp.append(scoreMatrix[i][0])  #Probe 
                    tmp.append(scoreMatrix[i][3])  #Score
                    scoreMatrix_no_opt.append(tmp)  # Probe|Score
                    tmp = []

        if match == False:
            count = count + 1
            tmp.append(scoreMatrix[i][0])  #Probe
            tmp.append(scoreMatrix[i][3])  #Score
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

    # print(scoreOperations_no_one_matched)
    # print("")
    # print("")
    # print(scoreOperations_no_one_no_matched)
    countOp = 0
    tmp = []
    repeatOp_matched = []
    foundOp = False
    # numero di volte in cui le operazioni si ripetono nelle matrici
    for i in range(len(scoreOperations_no_one_matched)):
    	for j in range(len(scoreOperations_no_one_matched[i][2])):
    		for k in range(len(repeatOp_matched)):
    			if scoreOperations_no_one_matched[i][2][j]['name'] == repeatOp_matched[k][0]:
    				foundOp = True
    				break
    		if foundOp == False:
    			for t in range(len(scoreOperations_no_one_matched)):
    				for s in range(len(scoreOperations_no_one_matched[t][2])):
    					if scoreOperations_no_one_matched[i][2][j]['name'] == scoreOperations_no_one_matched[t][2][s]['name']:
    						countOp = countOp + 1
    						break
    		if countOp > 0:
    			tmp.append(scoreOperations_no_one_matched[i][2][j]['name'])
    			tmp.append(countOp)
    			repeatOp_matched.append(tmp)
    		countOp = 0
    		tmp = []
    		foundOp = False

    tmp = []
    countOp = 0
    repeatOp_noMatched = []
    foundOp = False

    for i in range(len(scoreOperations_no_one_no_matched)):
    	for j in range(len(scoreOperations_no_one_no_matched[i][2])):
    		for k in range(len(repeatOp_noMatched)):
    			if scoreOperations_no_one_no_matched[i][2][j]['name'] == repeatOp_noMatched[k][0]:
    				foundOp = True
    				break
    		if foundOp == False:
    			for t in range(len(scoreOperations_no_one_no_matched)):
    				for s in range(len(scoreOperations_no_one_no_matched[t][2])):
    					if scoreOperations_no_one_no_matched[i][2][j]['name'] == scoreOperations_no_one_no_matched[t][2][s]['name']:
    						countOp = countOp + 1
    						break
    		if countOp > 0:
    			tmp.append(scoreOperations_no_one_no_matched[i][2][j]['name'])
    			tmp.append(countOp)
    			repeatOp_noMatched.append(tmp)
    		countOp = 0
    		tmp = []
    		foundOp = False
    
    tmp = []
    countOp = 0
    repeatOp_one = []
    foundOp = False

    # numero di volte in cui le operazioni si ripetono nelle matrici
    for i in range(len(scoreOperations_one)):
    	for j in range(len(scoreOperations_one[i][2])):
    		for k in range(len(repeatOp_one)):
    			if scoreOperations_one[i][2][j]['name'] == repeatOp_one[k][0]:
    				foundOp = True
    				break
    		if foundOp == False:
    			for t in range(len(scoreOperations_one)):
    				for s in range(len(scoreOperations_one[t][2])):
    					if scoreOperations_one[i][2][j]['name'] == scoreOperations_one[t][2][s]['name']:
    						countOp = countOp + 1
    						break
    		if countOp > 0:
    			tmp.append(scoreOperations_one[i][2][j]['name'])
    			tmp.append(countOp)
    			repeatOp_one.append(tmp)
    		countOp = 0
    		tmp = []
    		foundOp = False

    # Matrice globale contente: ProbeID,score
    global_score = scoreMatrix_opt + scoreMatrix_no_opt + noJSON
    print('Numero di ProbeID nel CSV score: ', len(scoreMatrix))
    print('Numero di ProbeID nel JSON: ', len(opHistory['probesFileID']))
    print("")
    print('Numero di ProbeID che matchano nel JSON: ', len(scoreMatrix_opt) + len(scoreMatrix_no_opt))
    print('Numero di ProbeID non trovati nel JSON: ', len(noJSON))
    print("")

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

def scoreFilter1(scoreMatrix,operations,score,idoperations,function='null',score2 = None):
	duplicateOP = check(idoperations)
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

def scoreFilter2(finalScorePath,opHistoryPath,score,idoperations,operator = 'null',maxPreviousOp = 0,score2 = None):

	scoreMatrix = CSVreader(finalScorePath)
	scoreMatrix.remove(scoreMatrix[0])  # Rimuovo l'intestazione
	# probeHistory.json
	with open(opHistoryPath) as f:
		opHistory = json.load(f)
	duplicateOP = check(idoperations)
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
					tmp.append(scoreMatrix[i][3])
					tmp.append(opHistory['probesFileID'][j]['operations'])
					tmpMatrix.append(tmp)
					tmp = []

		tmp = []
		tmpOp = [] 
		countOperations = 0
		prevOp = []

		if operator == 'null':
			print('errore,inserire operazioni')

		elif (score != -1) and (score < 0):
			print('errore,inserire parametri corretti')
			return 0

		elif (operator == 'equal'):
			for i in range(len(tmpMatrix)):
				if float(tmpMatrix[i][2]) == score:
					tmpResult.append(tmpMatrix[i][0])
					for z in range(len(idoperations)):
						currentOperation = idoperations[z]
						for j in range(len(tmpMatrix[i][3])):
							if tmpMatrix[i][3][j]['name'] != currentOperation:
								countOperations = countOperations + 1
								tmpOp.append(tmpMatrix[i][3][j]['name'])
							else:
								found = True
								break
						if found == True:
							tmp.append(currentOperation)
							for d in range(maxPreviousOp):
								if(len(tmpOp) - d) > 0:
									prevOp.append(tmpOp[(len(tmpOp)-1) - d])
								else:
									break
							tmp.append(prevOp)
							tmp.append(countOperations)
							tmpResult.append(tmp)
							atLeastOneOp = True
						tmp = []
						tmpOp = []
						prevOp = []
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
							for d in range(maxPreviousOp):
								if(len(tmpOp) - d) > 0:
									prevOp.append(tmpOp[(len(tmpOp)-1) - d])
								else:
									break
							tmp.append(prevOp)
							tmp.append(countOperations)
							tmpResult.append(tmp)
							atLeastOneOp = True
						tmp = []
						tmpOp = []
						countOperations = 0
						found =  False
						prevOp = []
					tmpResult.append('score:'+''+ tmpMatrix[i][2])
					if atLeastOneOp == True: 
						result.append(tmpResult)
					tmpResult = []
					atLeastOneOp = False

		elif (operator == 'under') and (score >= 0):
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
							for d in range(maxPreviousOp):
								if(len(tmpOp) - d) > 0:
									prevOp.append(tmpOp[(len(tmpOp)-1) - d])
								else:
									break
							tmp.append(prevOp)
							tmp.append(countOperations)
							tmp.append(tmpMatrix[i][2])
							tmpResult.append(tmp)
							atLeastOneOp = True
						tmp = []
						tmpOp = []
						prevOp = []
						countOperations = 0
						found =  False
					tmpResult.append('score:'+''+ tmpMatrix[i][2])
					if atLeastOneOp == True: 
						result.append(tmpResult)
					tmpResult = []
					atLeastOneOp = False

		elif (operator == 'range') and (score2 != None) and (score2 >= 0):
			for i in range(len(tmpMatrix)):
				if float(tmpMatrix[i][2]) >= score and (float(tmpMatrix[i][2]) <= score2):
					tmpResult.append(tmpMatrix[i][0])
					for z in range(len(idoperations)):
						currentOperation = idoperations[z]
						for j in range(len(tmpMatrix[i][3])):
							if tmpMatrix[i][3][j]['name'] != currentOperation:
								countOperations = countOperations + 1
								tmpOp.append(tmpMatrix[i][3][j]['name'])
							else:
								found = True
								break
						if found == True:
							tmp.append(currentOperation)
							for d in range(maxPreviousOp):
								if(len(tmpOp) - d) > 0:
									prevOp.append(tmpOp[(len(tmpOp)-1) - d])
								else:
									break
							tmp.append(prevOp)
							tmp.append(countOperations)
							tmpResult.append(tmp)
							atLeastOneOp = True
						tmp = []
						tmpOp = []
						prevOp = []
						countOperations = 0
						found =  False
					tmpResult.append('score:'+''+ tmpMatrix[i][2])
					if atLeastOneOp == True: 
						result.append(tmpResult)
					tmpResult = []
					atLeastOneOp = False

		elif (operator == 'range') and (score2 == None or score2 <0):
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




def scoreFilter3(finalScorePath, opHistoryPath, score, opFilter, operator ='null',score2 = None):

    scoreMatrix = CSVreader(finalScorePath)
    scoreMatrix.remove(scoreMatrix[0])  # Rimuovo l'intestazione
    # probeHistory.json
    with open(opHistoryPath) as f:
        opHistory = json.load(f)

    #opFilter = [x.lower() for x in opFilter]

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
                    tmp.append(scoreMatrix[i][3])
                    tmp.append(opHistory['probesFileID'][j]['operations'])
                    tmp.append(scoreMatrix[i][1])
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
        					if tmpMatrix[i][2][j]['name'] != currentOperation:
        						countOperations = countOperations + 1
        						lastOp = tmpMatrix[i][2][j]['name']
        					else:
        						found = True
        						if lastOp != None:
        							previousOperations.append(lastOp)
        						break
        				if found == True:
        					tmp.append(currentOperation)
        					tmp.append(tmpMatrix[i][0])
        					tmp.append(tmpMatrix[i][3])
        					if countOperations > 0:
        						tmp.append(countOperations)
        					else:
        						tmp.append('First operation')
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


        elif (operator == 'over') and (score >= 0):
        	for z in range(len(opFilter)):
        		currentOperation = opFilter[z]        	
        		for i in range(len(tmpMatrix)):
        			if float(tmpMatrix[i][1]) >=  score:
        				for j in range(len(tmpMatrix[i][2])):
        					if tmpMatrix[i][2][j]['name'] != currentOperation:
        						countOperations = countOperations + 1
        						lastOp = tmpMatrix[i][2][j]['name']
        					else:
        						found = True
        						if lastOp != None:
        							previousOperations.append(lastOp)
        						break
        				if found == True:
        					tmp.append(currentOperation)
        					tmp.append(tmpMatrix[i][0])
        					tmp.append(tmpMatrix[i][3])
        					if countOperations > 0:
        						tmp.append(countOperations)
        					else:
        						tmp.append('First operation')
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
        					tmp.append(tmpMatrix[i][3])
        					if countOperations > 0:
        						tmp.append(countOperations)
        					else:
        						tmp.append('First operation')
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
        					tmp.append(tmpMatrix[i][3])
        					if countOperations > 0:
        						tmp.append(countOperations)
        					else:
        						tmp.append('First operation')
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

        elif (score != -1) and (score < 0):
            print('errore,inserire parametri corretti')
            return 0,0 

        elif (operator == 'range') and score < 0:
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
        for i in range(len(finalResult)):
        	try:
        		finalResult[i] = sortScoreMatrix(finalResult[i])
        	except IndexError:
        		continue
        		
        return result,finalResult
# Leggo json
with open('/Users/andreasimioni/Downloads/Image-Processing-and-Security-master/MFC18_EvalPart1_TestOnVideo_TrainOnVideo/myoperations.json') as f:
	data = json.load(f)
# Leggo csv FinalScores
A = CSVreader('./FinalScores/UnifiPRNUTime_1_CameraVideoVideo.csv')
A.remove(A[0])  #Rimuovo l'intestazione
# Leggo csv ManipReference
B = CSVreader('./Reference/MFC18_EvalPart1-camera-ref.csv')
B.remove(B[0]) #Rimuovo l'intestazione
with open('./Reference/operations.json') as f:
	data2 = json.load(f)

score =  0
idoperations = ['OutputAVI','AddAudioSample','AntiForensicCopyExif']
z= scoreFilter2('./FinalScores/UnifiPRNUTime_1_CameraVideoVideo.csv','/Users/andreasimioni/Downloads/Image-Processing-and-Security-master/MFC18_EvalPart1_TestOnVideo_TrainOnVideo/myoperations.json', score, idoperations, operator ='over',maxPreviousOp = 3,score2 = 0)
printInColumn(z)
# print("")
# print("")
# print()
# printInColumn(result3)
# print("")
# print("")
# print(len(result3))



