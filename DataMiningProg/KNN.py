import sys
import csv
import random
import math

def cen_sel_random(unlabeled, bi_unlabeled):
    rand_1 = random.randint(0,len(unlabeled))
    rand_2 = random.randint(0,len(unlabeled))
    while rand_1 == rand_2:
       rand_centroid_2 = random.randint(0,len(unlabeled))
    rand_centroid_1 = unlabeled[rand_1]
    rand_centroid_2 = unlabeled[rand_2]
    new_record = ''
    for i in rand_centroid_1:
                if i == 'n':
                    new_record = new_record + '0'
                if i == 'y':
                    new_record = new_record + '1'
                if i == '?':
                    new_record = new_record + '5'
    
    rand_centroid_1 = new_record
    new_record = ''
    for i in rand_centroid_2:
                if i == 'n':
                    new_record = new_record + '0'
                if i == 'y':
                    new_record = new_record + '1'
                if i == '?':
                    new_record = new_record + '5'
    
    rand_centroid_2 = new_record
    KNN(bi_unlabeled, rand_centroid_1, rand_centroid_2)
        

def KNN(bi_unlabeled, rand_centroid_1, rand_centroid_2):
    att_num = 16
    cen_temp_1 = ''
    cen_temp_2 = ''
    c1Calc = []
    c2Calc = []
    counter = 0

    while rand_centroid_1 != cen_temp_1 and rand_centroid_2 != cen_temp_2:
        c1Calc = []
        c2Calc = []
        for record in bi_unlabeled:
            closest = mindist(rand_centroid_1, rand_centroid_2, record)
            if (closest == 1):
                c1Calc.append(list(record))
            else:
                c2Calc.append(list(record))

        cen_temp_1 = rand_centroid_1
        cen_temp_2 = rand_centroid_2
        rand_centroid_1 = ''
        rand_centroid_2 = ''
        counter = 0
        
        for val in range(0,att_num):
            for point in c1Calc:
                counter += point[val]
            counter = counter / len(c1Calc)
            if(counter >= .5):
                rand_centroid_1.append('1')
            else:
                rand_centroid_1.append('0')
                
        counter = 0
        for val in range(0,att_num):
            for point in range(0,len(c2Calc)):
                print(point[val])
                counter += int(c2Calc[(point[val])])
            counter = counter / len(c2Calc)
            if(counter >= .5):
                rand_centroid_2.append('1')
            else:
                rand_centroid_2.append('0')

    #print("done", '\n')
    #print("c1: ", rand_centroid_1, '\n')
    #print("c2: ", rand_centroid_2, '\n')
        



def mindist(c1,c2,point):
    #print("c1: ", c1, " c2: ",c2, " point: ", point)
    counterC1 = 0
    counterC2 = 0
    convertPoints = list(point)
    convertC1 = list(c1)
    convertC2 = list(c2)
    for i in range(0,len(convertC1)):
        if(convertC1[i] != convertPoints[i]):
            counterC1 += 1
        if(convertC2[i] != convertPoints[i]):
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
    
    csvFile = open( "../data-with-labels.csv" )
    labeled = []
    unlabeled = []
    bi_unlabeled = []
    unlabeled_count = 0
    labeled_count = 0
    record_num = 1
    selected_records = ''
    counter = 1

    csvFile.readline()
    for record in csvFile:
        record_num += 1
        #record = record[:-2]
        rand_val = random.randint(0,1.0)
        if rand_val == 1:
            if record[0] == 'd':
                record = record[9:]
            if record[0] == 'r':
                record = record[11:]
            new_record = ''
            for i in record:
                if i == 'n':
                    new_record = new_record + '0'
                if i == 'y':
                    new_record = new_record + '1'
                if i == '?':
                    new_record = new_record + '5'
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
