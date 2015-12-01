from collections import Counter
from copy import deepcopy
from math import log

class ClassificationTree(dict):

    def __init__(self):
        super().__init__()

    #need to find a way to prevent setting the
    #class's evaluation value outside of class

    def TreeGrowth( self, data, class_attr ):
        '''
        Returns a classification tree. The data parameter should be a list of
        records, each record being a dictionary of the
        form {attribute name: value}. The class_attr is the name of the attribute
        that is to be the class. The optional attr_done parameter should
        be a set of attribute names.
        '''
        #things to stop on:
        #done- empty data (ERROR)
        #done- data is not well formatted or wrong type (ERROR)
        #void- attr_done is not well formatted or wrong type (ERROR)
        #done- class_attr is not a string (ERROR)
        #done- class_attr is not an attribute (ERROR)

        if type(class_attr) is not str:
            print("Error: class is not a string")
            return "Error"
        elif not data:
            print("Error: empty data")
            return "Error"
        elif type(data) is not list:
            print("Error: data is not a list of dictionaries")
            return "Error"
        elif type(data[0]) is not dict:
            print("Error: data is not a list of dictionaries")
            return "Error"

        attributes = {key for key in data[0].keys()}

        for record in data:
            if type(record) is not dict:
                print("Error: data is not a list of dictionaries")
                return "Error"
            elif record.keys() != attributes:
                print("Error: all records in data do not share attribute set")
                return "Error"

        if class_attr not in attributes:
            print("Error: class is not an attribute")
            return "Error"

        attributes -= {class_attr}

        self.update( self.__PrivateTreeGrowth( data, class_attr, attributes ) )
        return deepcopy(self)

    def __PrivateTreeGrowth( self, data, class_attr, attributes ):
        #attributes = {key for key in data[0].keys()}
        #attributes -= attr_done
        #attributes -= {class_attr}
        class_values = [record[class_attr] for record in data]
        if class_values.count(class_values[0]) == len(class_values):
            #data is pure
            return class_values[0]
        elif not attributes:
            #empty attributes
            return Counter(class_values).most_common()
        else:
            best_split = ClassificationTree.find_best_split( data, attributes )
            root = {best_split:{}}
            values = {record[best_split] for record in data}
            for v in values:
                sub_data = [record for record in data if record[best_split] == v]
                sub_attr = set(attr_done)
                sub_attr -= {best_split}
                root[best_split][v] = self.__PrivateTreeGrowth( sub_data, class_attr, sub_attr )
        return root

    def Classify( self, record ):

        if not self:
            print("Error: tree not made yet! Use the TreeGrowth function",
                  "to create a classification tree.")
            return "Error"

        tree = deepcopy(dict(self))
        #count = 0
        #LIMIT = 500
        #while True and count < LIMIT:
        while True:
            attr = list(tree.keys())[0]
            x = tree[attr][record[attr]]
            if type(x) is not dict:
                return x
            else:
                tree = x
                #count += 1

        #print( "Error: Required tree depth too large!" )
        #return "Error"

    def BuildFakeTree( self ):
        tree = { 'a': {
            10: "blue", 1: { 'b': {
                5: "red", 2: { 'c': {
                    9: "yellow", 3: "green"
            } } } } } }
        self.update( tree )

    # This is a dummy
    @staticmethod
    def find_best_split( data, attributes, class_attr ):
        # get the values to calculate entropy
        entropies = {}
        num_records = len( data )
        rep_count = 0;
        dem_count = 0;
        attr_count = {}

        attr_vals = [ 'A=T', 'A=F', 'A=T:+', 'A=T:-', 'A=F:+', 'A=F:-' ]

        # create a dict for each attribute to hold thier values
        # needed to calculate its entropy
        for attr in attributes:
            # initialize a dict for each attribute
            attr_count[attr] = {}
            # initialize the values for each attribute
            for val in attr_vals:
                attr_count[attr][val] = 0.0

        # grab the values to calculate the entropies
        for record in data:
            if record[class_atter] == 'republican':
                rep_count = rep_count + 1.0;
            if record[class_atter] == 'democrat':
                dem_count = dem_count + 1.0;                
            for attr in attributes:
                if record[attr] == 1:
                    #increment A=T
                    attr_count[attr]['A=T'] += 1.0
                    if record[class_atter] == 'republican':
                        #increment A=T:-
                        attr_count[attr]['A=T:-'] += 1.0
                    if record[class_atter] == 'democrat':
                        #increment A=T:+
                        attr_count[attr]['A=T:+'] += 1.0
                if record[attr] == 0:
                    #increment A=F
                    attr_count[attr]['A=F'] += 1
                    if record[class_atter] == 'republican':
                        #increment A=F:-
                        attr_count[attr]['A=F:-'] += 1.0
                    if record[class_atter] == 'democrat':
                        #increment A=F:+
                        attr_count[attr]['A=F:+'] += 1.0
        
        # calculate each attribute's entropy
        Eorig = -1 * (rep_count/num_records) * log((rep_count/num_records), 2) - (dem_count/num_records) * log((dem_count/num_records), 2)

        for attr in attributes:
            # Attribute = T
            # Attribute = T : positive
            t = attr_count[attr]['A=T:+'] / attr_count[attr]['A=T']
            aTp = -1 * t * log(t, 2)
            # Attribute = T : negative
            t = attr_count[attr]['A=T:-'] / attr_count[attr]['A=T']
            aTn = -1 * t * log(t, 2)
            E_aT = aTp + aTn

            # Attribute = F
            # Attribute = F : positive
            t = attr_count[attr]['A=F:+'] / attr_count[attr]['A=F']
            aFp = -1 * t * log(t, 2)
            # Attribute = F : negative
            t = attr_count[attr]['A=F:-'] / attr_count[attr]['A=F']
            aFn = -1 * t * log(t, 2)
            E_aF = aFp + aFn

            # Calculate the entropy of the attribute
            tT = attr_count[attr]['A=T'] / num_records
            tF = attr_count[attr]['A=f'] / num_records
            entropies[attr] = Eorig - tT * log(E_aT, 2) - tF * log(E_aF, 2)

        # determine the best of the entropies
        maxEntropyVal = -1
        maxEntropyAttr = ''
        for attr in entropies:
            if entropies[attr] > maxEntropyVal:
                maxEntropyAttr = attr
    

        # return attribute best to split
        return attr

def FakeData():
    data = list()
    for i in range(1, 30, 3):
        val = i%4
        if val == 0:
            classVal = 'red'
        elif val == 1:
            classVal = 'green'
        elif val == 2:
            classVal = 'blue'
        elif val == 3:
            classVal = 'yellow'
        record = {'a':i, 'b':i+1, 'c':i+2, 'class': classVal}
        data.append(record)
    return data

def FakeBadData():
    data = [
        {'a':6, 'b':2},
        {'a':5, 'c':8},
        {'a':3, 'b':7},
        ]
    return data

if __name__ == '__main__':
    z = ClassificationTree()
    y = z.TreeGrowth( FakeData(), "class" )
    print("Function Return:")
    print(y)
    print("ClassificationTree Value:")
    print(z)
