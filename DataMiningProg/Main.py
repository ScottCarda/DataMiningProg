import sys
import ClassificationTree as CTree

def ConvertToBinary( record ):
    for i in range( 0, len(record)):
        if record == 'y' or record == 'democrat':
            record[i] = '1'
        elif record == 'n' or record == 'republican':
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

def Main():
    
    if len( sys.argv ) != 2:
        print("Usage error")
        return False

    csvFile = open( sys.argv[1] )
    labeled = [] #label records in csv file
    unlabeled = [] #unlabel records in csv file

    attributes = csvFile.readline()[:-1].split(',')
    for record in csvFile: # add one to record 
        rand_val = random.randint(0,1) # select either zero or one
        #if val is one remove the class from each record
        if rand_val == 1:
            new_record = record.split(',')
            new_record = new_record[1:]
            new_record = ConvertToBinary(new_record)     
            #append record to the unlabel list and new_record to binary list
            unlabeled.append(new_record)
        else:
            new_record = record.split(',')
            new_record = ConvertToBinary(new_record)
            labeled.append(new_record)

    csvFile.close()

    #convert labeled data into dictionary format
    labeled_dicts = list()
    for record in labeled:
        labeled_dicts.append( ConvertToDictionary( record, attributes ) )

    #classify labeled data
    tree = CTree.ClassificationTree()
    tree.TreeGrowth( labeled_data, attributes[0] )

    #cluster unlabeled data
    clusters = cen_sel_random(unlabeled)

    #get centroids from clusters
    centroids = list()
    for cluster in clusters:
        centroid = ConvertToDictionary( cluster.pop(0), attributes[1:] )
        clss = tree.Classify( centroid )
        if clss == 'democrat':
            clss = '1'
        elif clss == 'republican':
            clss = '0'
        for record in cluster:


    #classify centroids
if __name__ == '__main__':
    Main()