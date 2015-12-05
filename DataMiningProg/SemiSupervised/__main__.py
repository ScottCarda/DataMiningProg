import sys
import SemiSupervised as ss

def Main():
    
    if len( sys.argv ) != 2:
        print("Usage error")
        return False

    tree = ss.CreateLearner( *ss.ReadDataFile( sys.argv[1] ) )

    attributes, data = ss.GetData(sys.argv[1])
    classes = []

    for record in data:
        record = ss.ConvertToDictionary(record, attributes)
        classes.append(tree.Classify(record))
            
    ss.ErrorComp( data, classes )
    ss.conf_matrix( data, classes )

    return tree

if __name__ == '__main__':
    Main()
