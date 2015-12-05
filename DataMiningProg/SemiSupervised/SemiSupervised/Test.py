import sys
from . import ConvertToBinary

def GetData( filename ):

    data = [] #label records in csv file

    with open( filename ) as csvFile:
        attributes = csvFile.readline()[:-1].split(',')
        for Record in csvFile: # add one to record 
            record = Record.strip()
            if record:
                record = record.split(',')
                record = ConvertToBinary(record)
                data.append(record)
            
    return attributes, data


def ErrorComp(data, classes):
    counter = 0
    for i in range(0, len(data)):
        if data[i][0] != classes[i]:
            counter += 1

    print("Percent Error For Run: ", counter/len(data))

def conf_matrix(data,classes):
    correct_demo = 0
    correct_rep = 0
    incorrect_demo = 0
    incorrect_rep = 0

    for i in range(0, len(data)):
        if data[i][0]=='1' and classes[i] == '0':
            incorrect_demo += 1
        elif data[i][0]=='0' and classes[i] == '1':
            incorrect_rep += 1
        elif data[i][0]=='1' and classes[i] == '1':
            correct_demo += 1
        elif data[i][0]=='0' and classes[i] == '0':
            correct_rep += 1

    # prints the confusion matrix
    print("         R       D")
    print("   ----------------")
    print("R  |   ",
          correct_rep,
          "   ",
          incorrect_rep)
    print("D  |   ",
          incorrect_demo,
          "   ",
          correct_demo)
    print("Predicted (X) Actual (Y)")
