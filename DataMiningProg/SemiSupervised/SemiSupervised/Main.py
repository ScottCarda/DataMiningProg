import sys
import Learner

def Main():
    
    if len( sys.argv ) != 2:
        print("Usage error")
        return False

    tree = Learner.CreateLearner( *Learner.ReadDataFile( sys.argv[1] ) )

if __name__ == '__main__':
    Main()