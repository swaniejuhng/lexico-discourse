import pickle
import sys
import csv

if len(sys.argv)!=2:
    print("USAGE> avgToSparse.py [avgDump]")

avgRelDump=pickle.load(open(sys.argv[1],'rb'))
avgRelSparse=open(sys.argv[1].replace('.dict','_sparse.csv'),'w')
avgRelSCSV=csv.writer(avgRelSparse)
# id | group_id | feat | value | group_norm |

id_=1
for msgId in avgRelDump:
    # 
    for dim in range(len(avgRelDump[msgId][0])):
        # real msgId is msgId+1
        avgRelSCSV.writerow([id_,msgId+1,dim,avgRelDump[msgId][0][dim],avgRelDump[msgId][0][dim]])
        id_ += 1

avgRelSparse.close()
