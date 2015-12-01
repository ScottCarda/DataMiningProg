def convertOutput(c1,c2,att_name):
    att_list = att_name.split(',')
    final_c1 = {}
    final_c2 = {}
    
    
    for j in range(1, len(att_list)):
        print(att_list[j], ' ', c1[j-1])
        final_c1[att_list[j]] = c1[j-1]

            
    for j in range(1, len(att_list)):
        print(att_list[j], ' ', c2[j-1])
        final_c2[att_list[j]] = c2[j-1]
