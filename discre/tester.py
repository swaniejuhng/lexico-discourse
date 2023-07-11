from discourseParsing.SenseLabeller import SenseLabeller
from discourseParsing import PDTBAppendixSenses
from unitTests import typoTests

def main():
    typoTests.senseTypoTest(SenseLabeller(), PDTBAppendixSenses)
    typoTests.discourseConnectiveTypoTest(PDTBAppendixSenses)

if __name__=='__main__':
    main()
