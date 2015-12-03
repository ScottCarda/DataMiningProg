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
        #if data[i][0]=='d' and classes[i] == '0':
        #    counter += 1
        #elif data[i][0]=='r' and classes[i] == '1':
        #    counter += 1
        if data[i][0] != classes[i]:
            counter += 1

    return counter/len(data)
