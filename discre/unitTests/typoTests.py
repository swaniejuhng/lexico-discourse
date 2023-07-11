

def senseTypoTest(senseLabeller,pdtbAppendixSenses):

    for conn in pdtbAppendixSenses.explicitConnectiveRelationDict:
        for sense in pdtbAppendixSenses.explicitConnectiveRelationDict[conn]:
            for one in sense.split('/'):
                if one not in senseLabeller.senseMap:
                    print(conn,one)
    for conn in pdtbAppendixSenses.implicitConnectiveRelationDict:
        for sense in pdtbAppendixSenses.implicitConnectiveRelationDict[conn]:
            for one in sense.split('/'):
                if one not in senseLabeller.senseMap:
                    print(conn,one)
    print("Search Done")

def discourseConnectiveTypoTest(pdtbAppendixSenses):
    connFile=open('./utils/PDTB_discourse_connectives_full_list.txt','r')
    conns=set()
    for conn in connFile:
        conns.add(conn.strip())
    
    connFile.close()
    explicitConns=pdtbAppendixSenses.explicitConnectiveRelationDict.keys()
    implicitConns=pdtbAppendixSenses.implicitConnectiveRelationDict.keys()
    for conn in explicitConns:
        if conn not in conns:
            print('Explicit: ',conn)
    for conn in implicitConns:
        if conn not in conns:
            print('Implicit: ',conn)
    
def main():
    discourseConnectiveTypoTest()
    
if __name__=='__main__':
    main()
