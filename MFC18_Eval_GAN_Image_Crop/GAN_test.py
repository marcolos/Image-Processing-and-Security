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
    if A != None:
        for i in range(len(A)):
            print(A[i])
    else:
        print('None')


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
    division_parse = subparser.add_parser('division', help='Division for optout, matched and no_matched')
    division_parse.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    division_parse.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    division_parse.add_argument("-cp", "--camerapath", required=True, help="path of camera reference")
    division_parse.add_argument("-vs", "--valoresoglia", type=int, required=True, help="valore di soglia")
    division_parse.add_argument("-vo", "--valoreoptout", type=int, required=True, help="valore di optout")

    # subcommand manipulation-name
    manipulation_parser = subparser.add_parser('manipulation-list', help='List all possible manipulations')
    manipulation_parser.add_argument("-sp", "--scorepath", required=True, help="path of score csv")
    manipulation_parser.add_argument("-hp", "--probehistory", required=True, help="path of probe history")
    manipulation_parser.add_argument("-cp", "--camerapath", required=True, help="path of camera reference")
    manipulation_parser.add_argument("-o", "--operations", required=True,
                                     help="insert json file path contains all operations")
    manipulation_parser.add_argument("-vs", "--valoresoglia", type=int, required=True, help="valore di soglia")
    manipulation_parser.add_argument("-vo", "--valoreoptout", type=int, required=True, help="valore di optout")

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
    filter2_parser.add_argument("-s2", "--score2", required=False, type=int, help="insert score2")
    filter2_parser.add_argument("-o", "--operation", required=True, nargs='+', help="insert operation filter")
    filter2_parser.add_argument("-po", "--prevop", type=int, required=True, help="insert preview operations")

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
        print('division')
        #division(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, cameraPath=args.camerapath,valore_soglia=args.valoresoglia, valore_optout=args.valoreoptout)
    elif args.subcommand == 'manipulation-list':
        print('manipulation_list')
        #manipulation_list(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, cameraPath=args.camerapath,allOperationsPath=args.operations, valore_soglia=args.valoresoglia,valore_optout=args.valoreoptout)
    elif args.subcommand == 'filter1':
        print('filter1')
        #result = scoreFilter1(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, score=args.score,opFilter=args.operation, operator=args.operator, score2=args.score2)
        #printInColumn(result)
    elif args.subcommand == 'filter2':
        print('filter2')
        #result = scoreFilter2(finalScorePath=args.scorepath, opHistoryPath=args.probehistory, score=args.score,opFilter=args.operation, operator=args.operator, maxPreviousOp=args.prevop,score2=args.score2)
        #printInColumn(result)
    elif args.subcommand == 'alloperations':
        print('allOperations')
        #allOperations(finalScorePath=args.scorepath, opHistoryPath=args.probehistory)


def mainInterattivo():
    print('Which operation do you want use?')
    print('1) Create json file containing probe history')
    print('2) Manipulation list')
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

        #manipulation_list(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, cameraPath=cameraPath,allOperationsPath=operationsPath, valore_soglia=valore_soglia, valore_optout=valore_optout)

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
                    print('')
                    # result = scoreFilter1(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score, opFilter=[opFilter], operator=operator, score2=score2)
                    # printInColumn(result)
                else:
                    print('')
                    # result = scoreFilter1(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score,opFilter=[opFilter], operator=operator)
                    # printInColumn(result)

            if (mainScelta == 4):
                # inserimento numero di operazioni precedenti
                print('Insert number of previews operations to view: ')
                prevOp = int(input())
                if operator == 'range':
                    print('')
                    # result = scoreFilter2(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score,opFilter=[opFilter], operator=operator, maxPreviousOp=prevOp, score2=score2)
                    # printInColumn(result)
                else:
                    print('')
                    # result = scoreFilter2(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, score=score, opFilter=[opFilter], operator=operator, maxPreviousOp=prevOp)
                    # printInColumn(result)

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
        #division(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath, cameraPath=cameraPath,valore_soglia=valore_soglia, valore_optout=valore_optout)

    elif (mainScelta == 6):
        print('Insert score path: ')
        finalScorePath = input().strip()
        print('Insert probe history path: ')
        opHistoryPath = input().strip()
        #allOperations(finalScorePath=finalScorePath, opHistoryPath=opHistoryPath)


if __name__ == '__main__':
    if sys.argv[1:] != []:
        main()
    else:
        mainInterattivo()

