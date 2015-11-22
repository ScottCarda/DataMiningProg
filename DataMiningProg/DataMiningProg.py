from collections import Counter
from copy import deepcopy

class ClassificationTree(dict):

    def __init__(self):
        super().__init__()

    #need to find a way to prevent setting the
    #classes evaluation value outside of class

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

        self.update( self.__PrivateTreeGrowth( data, class_attr, set() ) )
        return deepcopy(self)

    def __PrivateTreeGrowth( self, data, class_attr, attr_done ):
        #'''
        #Returns a classification tree. The data parameter should be a list of
        #records, each record being a dictionary of the
        #form {attribute name: value}. The class_attr is the name of the attribute
        #that is to be the class. The optional attr_done parameter should
        #be a set of attribute names.
        #'''
        ##things to stop on:
        ##done- empty data (ERROR)
        ##done- data is not well formatted or wrong type (ERROR)
        ##    - attr_done is not well formatted or wrong type (ERROR)
        ##done- class_attr is not a string (ERROR)
        ##done- class_attr is not an attribute (ERROR)

        #if type(class_attr) is not str:
        #    print("Error: class is not a string")
        #    return "Error"
        #elif not data:
        #    print("Error: empty data")
        #    return "Error"
        #elif type(data) is not list:
        #    print("Error: data is not a list of dictionaries")
        #    return "Error"
        #elif type(data[0]) is not dict:
        #    print("Error: data is not a list of dictionaries")
        #    return "Error"

        attributes = {key for key in data[0].keys()}

        #for record in data:
        #    if type(record) is not dict:
        #        print("Error: data is not a list of dictionaries")
        #        return "Error"
        #    elif record.keys() != attributes:
        #        print("Error: all records in data do not share attribute set")
        #        return "Error"

        #if class_attr not in attributes:
        #    print("Error: class is not an attribute")
        #    return "Error"

        attributes -= attr_done
        attributes -= {class_attr}
        class_values = [record[class_attr] for record in data]

        #things to stop on:
        #done- empty attributes (will happen, return majority class?)
        #done- data pure (will happen, return class)
        if class_values.count(class_values[0]) == len(class_values):
            #data is pure
            return class_values[0]
        elif not attributes:
            #empty attributes
            return Counter(class_values).most_common()
        else:
            best_split = ClassificationTree.find_best_split( data, attributes )
            #root.test_cond = find_best_split( data, attributes )
            root = {best_split:{}}
            values = {record[best_split] for record in data}
            for v in values:
                sub_data = [record for record in data if record[best_split] == v]
                #sub_attributes = attributes - {best_split}
                #sub_attributes = {attr for atr in attributes if attr != best_split}
                #sub_attributes = attributes.copy()
                #sub_attributes.remove(root.test_cond)
                sub_attr_done = set(attr_done)
                sub_attr_done.add(best_split)
                root[best_split][v] = self.__PrivateTreeGrowth( sub_data, class_attr, sub_attr_done )
        return root

    def Classify(record):
        print("Not Implemented")

    # This is a dummy
    @staticmethod
    def find_best_split( data, attributes ):
        return list(attributes)[0]

def FakeData():
    data = list()
    for i in range(1, 30, 3):
        record = {'a':i, 'b':i+1, 'c':i+2, 'class': i%4}
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