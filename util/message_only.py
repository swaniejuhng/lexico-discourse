import csv
import sys
import pandas as pd

if len(sys.argv) != 2:
    print("Usage> message_only.py [message table csv file]")
    sys.exit()

mesg_df=pd.read_csv(sys.argv[1])
output_name=sys.argv[1].replace('.csv','.txt')

if 'message' not in mesg_df.columns:
    print("message text file must have 'message' column")
    sys.exit()

with open(output_name,'w') as output_file:
    for i,row in mesg_df.iterrows():
        output_file.write(str(row['message'])+'\n')