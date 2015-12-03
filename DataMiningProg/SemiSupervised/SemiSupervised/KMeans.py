import sys
import csv
import random
import math

def MaxDisCentriodSelc(bi_unlabeled):
    
    points = []
    counterFurthest = 0    
    counterC1 = 0 # tracks the hamming distance from centriod 1
    
    for record in bi_unlabeled: # add one to record 
        rand_val = random.randint(0,3.0)
        
        if rand_val == 3:
            points.append(record)
            
    rand_1 = random.randint(0,len(points))#Obtain first centriod
    c1 = points[rand_1]
    
    #loop through each character in binary string
    #and compute the hamming distance
    for point in points:
        counterC1 = 0
        for i in range(0,len(c1)):
            if(c1[i] != point[i]):
                counterC1 += 1
        if counterC1 > counterFurthest:
            furthest = point
            counterFurthest = counterC1
            
    finalClusters = KMeans(bi_unlabeled, c1, furthest)
    return finalClusters

def cen_sel_random(bi_unlabeled):
    rand_1 = random.randint(0,len(bi_unlabeled)) #randomly select the 2 centroid from the unlabeled data
    rand_2 = random.randint(0,len(bi_unlabeled))

    # if the two random centroids happen to be equal re select centroid 2
    while rand_1 == rand_2:
       rand_centroid_2 = random.randint(0,len(bi_unlabeled))
    # set the centroid equal to the value in the unlabeled list of records
    rand_centroid_1 = bi_unlabeled[rand_1]
    rand_centroid_2 = bi_unlabeled[rand_2]

    finalClusters = KMeans(bi_unlabeled, rand_centroid_1, rand_centroid_2)
    return finalClusters

def KMeans(bi_unlabeled, rand_centroid_1, rand_centroid_2):
    att_num = 16 # number of attributes in the data file
    cen_temp_1 = '' # temp centroid for compares
    cen_temp_2 = '' # tracks perv. centroid
    c1Calc = [] #list of points associated with centroid 1
    c2Calc = [] #list of points associated with centroid 2
    counter = 0

    #loop until centriods stablize
    while rand_centroid_1 != cen_temp_1 and rand_centroid_2 != cen_temp_2:
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

    

    finalClusters = convertOutput(rand_centroid_1,rand_centroid_2,c1Calc,c2Calc)
    return finalClusters

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

def convertOutput(c1,c2,c1Calc,c2Calc):
    final_c1 = {}
    final_c2 = {}
    cen1_final_list = []
    cen2_final_list =[]

    cen1_final_list.append(c1)
    cen2_final_list.append(c2)

    for i in range(0,len(c1Calc)):
        cen1_final_list.append(c1Calc[i])

    for i in range(0,len(c2Calc)):
        cen2_final_list.append(c2Calc[i])

    return cen1_final_list, cen2_final_list
