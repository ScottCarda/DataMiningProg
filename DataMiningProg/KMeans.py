import sys
import csv
import random
import math

def cen_sel_random(unlabeled, bi_unlabeled):
    rand_1 = random.randint(0,len(bi_unlabeled)) #randomly select the 2 centroid from the unlabeled data
    rand_2 = random.randint(0,len(bi_unlabeled))

    # if the two random centroids happen to be equal re select centroid 2
    while rand_1 == rand_2:
       rand_centroid_2 = random.randint(0,len(unlabeled))
    # set the centroid equal to the value in the unlabeled list of records
    rand_centroid_1 = bi_unlabeled[rand_1]
    rand_centroid_2 = bi_unlabeled[rand_2]

    KMeans(bi_unlabeled, rand_centroid_1, rand_centroid_2)
        

def KMeans(bi_unlabeled, rand_centroid_1, rand_centroid_2):
    att_num = 16 # number of attributes in the data file
    cen_temp_1 = '' # temp centroid for compares
    cen_temp_2 = '' # tracks perv. centroid
    c1Calc = [] #list of points associated with centroid 1
    c2Calc = [] #list of points associated with centroid 2
    counter = 0

    #loop until centriods stablize
    while rand_centroid_1 != cen_temp_1 and rand_centroid_2 != cen_temp_2:
        print("cen1: ", rand_centroid_1, ' ', "cen2: ", rand_centroid_2)
        c1Calc = [] #Reset c1Calc and c2Calc
        c2Calc = []
        #Determine which points reside closest to the centriods
        for record in bi_unlabeled:
            closest = mindist(rand_centroid_1, rand_centroid_2, record)
            if (closest == 1):
                c1Calc.append(record)
            else:
                c2Calc.append(record)

        #Store the previous values of each centriod
        cen_temp_1 = rand_centroid_1
        cen_temp_2 = rand_centroid_2
        rand_centroid_1 = ''
        rand_centroid_2 = ''
        counter = 0

        #Recalculate centroid 1 
        for val in range(0,att_num):
            #loop through one attribute and calculate the average
            for point in c1Calc:
                counter += int(point[val])
            counter = counter / len(c1Calc)
            #Round up or down
            if(counter >= .5):
                rand_centroid_1 = rand_centroid_1 + '1'
            else:
                rand_centroid_1 = rand_centroid_1 + '0'

        #Recalculate centriod 2        
        counter = 0
        for val in range(0,att_num):
            #loop through one attribute and calculate the average
            for point in c2Calc:
                counter += int(point[val])
            counter = counter / len(c2Calc)
            #Round up or down
            if(counter >= .5):
                rand_centroid_2 = rand_centroid_2 +'1'
            else:
                rand_centroid_2 = rand_centroid_2 + '0'

        
    #print("done", '\n')
    #print("c1: ", rand_centroid_1, '\n')
    #print("c2: ", rand_centroid_2, '\n')
        



def mindist(c1,c2,point):
    #print("c1: ", c1, " c2: ",c2, " point: ", point)
    counterC1 = 0 # tracks the hamming distance from centriod 1
    counterC2 = 0 # tracks the hamming distance from centroid 2
    #loop through each character in binary string
    #and compute the hamming distance
    for i in range(0,len(c1)):
        if(c1[i] != point[i]):
            counterC1 += 1
        if(c2[i] != point[i]):
            counterC2 += 1
    if (counterC1 < counterC2):
        return 1
    else:
        return 2
        

    

def Main():
    
    '''
    if len( sys.argv ) != 2:
        print ("Usage error")
        return False
    '''
    
    csvFile = open( "data-with-labels-pre-processed.csv" )
    labeled = [] #label records in csv file
    unlabeled = [] #unlabel records in csv file
    bi_unlabeled = [] #unlabeled records converted to binary string 
    unlabeled_count = 0 
    labeled_count = 0
    record_num = 1
    selected_records = ''
    counter = 1

    csvFile.readline() # skip header line
    for record in csvFile: # add one to record 
        record_num += 1
        rand_val = random.randint(0,1.0) # select either zero or one
        #if val is one remove the class from each record
        if rand_val == 1:
            #if class is democrat
            if record[0] == 'd':
                record = record[9:]
            #if class is republican
            if record[0] == 'r':
                record = record[11:]

            #new record is the binary string     
            new_record = ''
            
            for i in record:
                #if record is n add 0
                if i == 'n':
                    new_record = new_record + '0'
                #if record is n add 1
                if i == 'y':
                    new_record = new_record + '1'
                    
            #append record to the unlabel list and new_record to binary list
            unlabeled_count += 1
            unlabeled.append(record)
            selected_records = selected_records + ' ' + str(counter) + '.' + str(record_num) + ','
            bi_unlabeled.append(new_record)
            counter += 1
        
            #print(record, ' ', new_record,'\n')
        else:
            labeled_count += 1
            labeled.append(record)
    #print(unlabeled[0], '\n', unlabeled[1], '\n', unlabeled[2])
    #print("unlabeled_count ", unlabeled_count)
    #print("selected_records ", selected_records)
    #print(' ', unlabeled)

    csvFile.close()
    cen_sel_random(unlabeled, bi_unlabeled)

if __name__ == '__main__':
    Main()
