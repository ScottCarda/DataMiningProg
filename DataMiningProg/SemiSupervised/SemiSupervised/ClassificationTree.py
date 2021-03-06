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
        form {attribute name: value}. The class_attr is the name of the
        attribute that is to be the class. The optional attr_done parameter
        should be a set of attribute names.
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

        #acquire attributes from data
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

        #remove class from the attribute set
        attributes -= {class_attr}

        #create classification tree
        self.clear()
        self.update( self.__PrivateTreeGrowth( data, class_attr, attributes ) )

        #return a copy of tree
        return deepcopy(self)

    def __PrivateTreeGrowth( self, data, class_attr, attributes ):

        #acquire all possible values of class
        class_values = [record[class_attr] for record in data]

        #base cases
        if class_values.count(class_values[0]) == len(class_values):
            #data is pure
            return class_values[0]
        elif not attributes:
            #empty attributes
            return Counter(class_values).most_common()

        else:
            #get the attribute that produces the best split
            best_split = ClassificationTree.find_best_split( data, attributes,
                                                            class_attr )
            root = {best_split:{}} #initialize the tree to return
            #acquire all possible values of best split attribute
            values = {record[best_split] for record in data}
            for v in values:
                sub_data = \
                    [record for record in data if record[best_split] == v]
                sub_attr = set(attributes)  #copy attribute set
                sub_attr -= {best_split}    #remove attribute used to split
                #get subtrees
                root[best_split][v] = \
                    self.__PrivateTreeGrowth( sub_data, class_attr, sub_attr )
        #return the classification tree
        return root

    def Classify( self, record ):

        if not self:
            print("Error: tree not made yet! Use the TreeGrowth function",
                  "to create a classification tree.")
            return "Error"

        tree = deepcopy(dict(self))
        while True:
            attr = list(tree.keys())[0]
            x = tree[attr][record[attr]]
            if type(x) is not dict:
                return x
            else:
                tree = x

    @staticmethod
    def find_best_split( data, attributes, class_attr ):
        # get the values to calculate entropy
        entropies = {}
        num_records = len( data )
        rep_count = 0;
        dem_count = 0;
        attr_count = {}

        attr_vals = [ 'A=T', 'A=F', 'A=T:+', 'A=T:-', 'A=F:+', 'A=F:-' ]

        # create a dict for each attribute to hold their values
        # needed to calculate its entropy
        for attr in attributes:
            # initialize a dict for each attribute
            attr_count[attr] = {}
            # initialize the values for each attribute
            for val in attr_vals:
                attr_count[attr][val] = 0.0

        # grab the values to calculate the entropies
        for record in data:
            if record[class_attr] == '0':
                rep_count = rep_count + 1.0;
            if record[class_attr] == '1':
                dem_count = dem_count + 1.0;                
            for attr in attributes:
                if record[attr] == '1':
                    #increment A=T
                    attr_count[attr]['A=T'] += 1.0
                    if record[class_attr] == '0':
                        #increment A=T:-
                        attr_count[attr]['A=T:-'] += 1.0
                    if record[class_attr] == '1':
                        #increment A=T:+
                        attr_count[attr]['A=T:+'] += 1.0
                if record[attr] == '0':
                    #increment A=F
                    attr_count[attr]['A=F'] += 1
                    if record[class_attr] == '0':
                        #increment A=F:-
                        attr_count[attr]['A=F:-'] += 1.0
                    if record[class_attr] == '1':
                        #increment A=F:+
                        attr_count[attr]['A=F:+'] += 1.0
        
        # calculate each attribute's entropy
        Eo_rep = -1 * (rep_count/num_records) * \
            log((rep_count/num_records), 2) if rep_count != 0 else 0
        Eo_dem = -1 * (dem_count/num_records) * \
            log((dem_count/num_records), 2) if dem_count != 0 else 0
        Eorig = Eo_rep + Eo_dem

        for attr in attributes:
            # check if all the data goes one way or the other
            if attr_count[attr]['A=T'] != 0 and attr_count[attr]['A=F'] != 0:

                # Attribute = T
                # Attribute = T : positive
                t = attr_count[attr]['A=T:+'] / attr_count[attr]['A=T']
                aTp = -1 * t * log(t, 2) if t != 0 else 0
                # Attribute = T : negative
                t = attr_count[attr]['A=T:-'] / attr_count[attr]['A=T']
                aTn = -1 * t * log(t, 2) if t != 0 else 0
                E_aT = aTp + aTn

                # Attribute = F
                # Attribute = F : positive
                t = attr_count[attr]['A=F:+'] / attr_count[attr]['A=F']
                aFp = -1 * t * log(t, 2) if t != 0 else 0
                # Attribute = F : negative
                t = attr_count[attr]['A=F:-'] / attr_count[attr]['A=F']
                aFn = -1 * t * log(t, 2) if t != 0 else 0
                E_aF = aFp + aFn

                # Calculate the entropy of the attribute
                tT = attr_count[attr]['A=T'] / num_records
                tF = attr_count[attr]['A=F'] / num_records
                entropies[attr] = Eorig - tT * E_aT - tF * E_aF
            else:
                # all of the data when one way, so there is no info gain
                entropies[attr] = 0

        # determine the best of the entropies
        maxEntropyVal = -1
        maxEntropyAttr = ''
        for attr in entropies:
            if entropies[attr] > maxEntropyVal:
                maxEntropyVal = entropies[attr]
                maxEntropyAttr = attr

        # return attribute best to split
        return maxEntropyAttr
