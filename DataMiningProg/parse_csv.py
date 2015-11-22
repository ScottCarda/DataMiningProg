import sys

def Main():

    if len( sys.argv ) != 2:
        print("Usage error")
        return False

    csvFile = open( sys.argv[1] )
    labeled = []
    unlabeled = []

    for record in csvFile:
        record = record[:-2]
        if '?' in record:
            unlabeled.append(record)
        else:
            labeled.append(record)

    csvFile.close()

if __name__ == '__main__':
    Main()
