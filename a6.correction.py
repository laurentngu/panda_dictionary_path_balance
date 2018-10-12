# -*- coding: utf-8 -*-
"""
Created on Sat May 13 14:54:56 2017
"""
import pandas as pd
from datetime import datetime
import sys
a=12.5
#b=22
data=pd.read_csv("C:\Users\laure\OneDrive - students.itu.edu/PYTHON/RMS2.log",sep=";")
#data=pd.read_csv("/Users/ln/OneDrive_ITU/OneDrive - students.itu.edu/PYTHON/RMS2.log",sep=";")
#data=pd.read_csv("C:\Users\hiallo\OneDrive - students.itu.edu/PYTHON/RMS2.log",sep=";")
# remove column where string contains VIHOST
data=data[data.nom_omc.str.contains("VIHOST")==False]

data=data.sort_values(['bts','annee','semaine','lac','nom_omc','ci'],ascending=[True,True,True,True,True,True])
data.reset_index(drop=True,inplace=True)

ABC=data['bts'].unique().tolist()

#d2=data.set_index("bts",inplace=False)
#del data
global d3 


idx_dict = data.groupby(by='bts').apply(lambda x: x.index.tolist()).to_dict()

def searchTMA(x,data):
    #d3=d2.loc[[x]].copy()
    ##d3=d2[d2.index.values==x].copy()
    ##d3.reset_index(level=0,inplace=True)
    d3=data.iloc[idx_dict[x]].copy()
    d3['pathbalance']=(d3['avg_path_balance']>a) 
    #& (d3['RMS_UL_RxLevel_avg']>d3['RMS_DL_RxLevel_avg']) \
   #   & (d3['annee']>2016)
    return d3 
#ABC=['GRENOBLE_CENTRE_d1','GRENOBLE_CENTRE_3','ZB_DOUILLET_LE_JOLY_1G2']
#ABC=['ZB_DOUILLET_LE_JOLY_1G2']
startTime = datetime.now()
for cellname in ABC:
    d3=searchTMA(cellname,data)
    
    # false, then true (start)    
    start=d3.index[d3['pathbalance'] & ~ d3['pathbalance'].shift(1).fillna(False)]

    # true, then false (end)
    end=d3.index[d3['pathbalance'] & ~ d3['pathbalance'].shift(-1).fillna(False) ]
    # 1. detect PATH_BALANCE (column 8) >12dB for 7 days continuous, in the past
    PB=[(i,j) for i,j in zip (start,end) if j>i+6]
    if (PB):
        #sys.stdout.write ("\n"+d3['bts'][PB[0][0]] +" ; ")
        sys.stdout.write ("\n"+d3['bts'][PB[0][0]] + " "+ str(PB)+" ; ")
        for k in range(0,len(PB)):
            #print(d3[['annee','semaine']].ix[PB[k][0]]).round(1).to_frame().T.to_csv(header=False,index=False,line_terminator=''),("to"),(d3[['annee','semaine','avg_path_balance']].ix[PB[k][1]]).round(1).to_frame().T.to_csv(header=False,index=False,line_terminator='')
            if ((k!=len(PB)-1) & (d3[['annee']].ix[PB[k][1]]>2016).any()):
                sys.stdout.write("["+d3[['semaine','annee']].ix[PB[k][0]].to_frame().T.\
                to_csv(header=False,index=False,line_terminator='',sep='.')
                +("] ")+\
                (d3[['avg_path_balance']].ix[PB[k][0]]).round(1).to_frame().T.\
                to_csv(header=False,index=False,line_terminator='')
                + (" to ") +\
                ("["+(d3[['semaine','annee']].ix[PB[k][1]]).to_frame().T.\
                to_csv(header=False,index=False,line_terminator='',sep='.')) +"] "  +((d3[['avg_path_balance']].\
                ix[PB[k][1]]).round(1).to_frame().T.to_csv(header=False,index=False,line_terminator=''))+" ;\n")
            else:
                    sys.stdout.write("["+d3[['semaine','annee']].ix[PB[k][0]].to_frame().T.\
                    to_csv(header=False,index=False,line_terminator='',sep='.')+("] ")+\
                    (d3[['avg_path_balance']].ix[PB[k][0]]).round(1).to_frame().T.\
                    to_csv(header=False,index=False,line_terminator='')
                    + (" to ") +\
                    ("["+(d3[['semaine','annee']].ix[PB[k][1]]).to_frame().T.\
                    to_csv(header=False,index=False,line_terminator='',sep='.')) +"] "  +((d3[['avg_path_balance']].\
                    ix[PB[k][1]]).round(1).to_frame().T.to_csv(header=False,index=False,line_terminator=''))+"\n")
       
       
#del d2  
#del data   
#del d3
print (("\n"),datetime.now()-startTime)