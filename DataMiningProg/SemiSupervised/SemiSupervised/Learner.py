from . import ClassificationTree
from . import cen_sel_random
import random

def ConvertToBinary( record ):
    for i in range( 0, len(record)):
        if record[i] == 'y' or record[i] == 'democrat':
            record[i] = '1'
        elif record[i] == 'n' or record[i] == 'republican':
            record[i] = '0'
        else:
            record[i] = ''
    return ''.join(record)

def ConvertToDictionary( binstring, attributes ):
    count = len(binstring)
    return_dict = dict()
    for i in range(0, count):
        return_dict[attributes[i]] = binstring[i]
    return return_dict

def ReadDataFile( filename ):

    labeled = [] #label records in csv file
    unlabeled = [] #unlabel records in csv file

    with open( filename ) as csvFile:
        attributes = csvFile.readline()[:-1].split(',')
        for Record in csvFile: # add one to record 
            record = Record.strip()
            if record:
                rand_val = random.randint(0,1) # select either zero or one
                #if val is one remove the class from each record
                if rand_val == 1:
                    new_record = record.split(',')
                    new_record = new_record[1:]
                    new_record = ConvertToBinary(new_record)     
                    #append new_record to the unlabeled list
                    unlabeled.append(new_record)
                else:
                    new_record = record.split(',')
                    new_record = ConvertToBinary(new_record)
                    labeled.append(new_record)

    return attributes, labeled, unlabeled

def CreateLearner( attributes, labeled, unlabeled ):

    #convert labeled data into dictionary format
    labeled_dicts = list()
    for record in labeled:
        labeled_dicts.append( ConvertToDictionary( record, attributes ) )

    #classify labeled data
    tree = ClassificationTree()
    tree.TreeGrowth( labeled_dicts, attributes[0] )

    #cluster unlabeled data
    clusters = cen_sel_random(unlabeled)

    #classify unlabeled data
    centroids = list()
    data = list(labeled)
    for cluster in clusters:
        #get centroids from clusters
        centroid = ConvertToDictionary( cluster.pop(0), attributes[1:] )
        #classify centroid
        clss = tree.Classify( centroid )
        #apply class to all records in a cluster
        for record in cluster:
            data.append( clss + record )

    #convert labeled data into dictionary format
    data_dicts = list()
    for record in data:
        data_dicts.append( ConvertToDictionary( record, attributes ) )

    #regrow tree
    tree.TreeGrowth( data_dicts, attributes[0] )

    return tree
