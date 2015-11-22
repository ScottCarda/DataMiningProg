import sys
from random import randint

def Main():

    if len( sys.argv ) != 2:
        print ("Usage error")
        return False

    csvFile = open( sys.argv[1] )
    labeled = []
    unlabeled = []
    unlabeled_count = 0
    labeled_count = 0

    for record in csvFile:
        #record = record[:-2]
        rand_val = randint(0,1.0)
        if rand_val == 1:
            if record[0] == 'd':
                record = record[9:]
            if record[0] == 'r':
                record = record[11:]
            unlabeled_count += 1
            unlabeled.append(record)
            print(record,'\n')
        else:
            labeled_count += 1
            labeled.append(record)

    print("unlabeled_count ", unlabeled_count)
    #print(' ', unlabeled)

    csvFile.close()

if __name__ == '__main__':
    Main()