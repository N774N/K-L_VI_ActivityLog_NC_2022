#Import all potentially relevant modules at the start. 
import pandas as pd
import tkinter as tk
from tkinter import filedialog

#Import CSV - due to it being an irregular file with many empty cells, 255 columns without headers are manually assigned. 
file_path = filedialog.askopenfilename()
T= pd.read_csv(file_path,  header=None, names=range(255), na_filter= False,  keep_default_na=False)


#Create dataframe from first column, we will be finding positions of various strings using index locations. 
headers=T.iloc[:, [0]]
nRows=len(headers)


#Date, Subject, and Database titles are stored in cells adjacent to the actual Date etc. values. Here we find and create lists of the index location of these values.  
dateIX=[]
subjIX=[]
dbgIX=[]

for i in range(nRows):        
    if ('Date' == (headers.iloc[i]).values[0]):
        dateIX.extend([i])
        
    if ('Subject Id' == headers.iloc[i].values[0]):
        subjIX.extend([i])
        
    if ('DB Group' == headers.iloc[i].values[0]):
        dbgIX.extend([i])

#Pull values from column 1 using the title indexes identified in column 0 above. Also count subjects.
Date = T[1].iloc[dateIX]
Subject = T[1].iloc[subjIX]
DBGroup = T[1].iloc[dbgIX]
nRat = len(subjIX)

#String labels replace numeric labels for DBGroup
for i in range(len(DBGroup)):
    if DBGroup.iloc[i] == '1':
        DBGroup.iloc[i] = 'LEFT'
    else:
        DBGroup.iloc[i] = 'RIGHT'

Date = Date.reset_index(drop=True)
Subject = Subject.reset_index(drop=True)
DBGroup = DBGroup.reset_index(drop=True)

#Same as earlier, we pull index locations of ACTIVITYLOG and ENDDATA, data of interest is contained in these blocks. 
stIX=[]
edIX=[]
for i in range(nRows):        
    if ('ACTIVITYLOG' == (headers.iloc[i]).values[0]):
        stIX.extend([i])

    if ('ENDDATA' == headers.iloc[i].values[0]):
         edIX.extend([i])


#User inputs drug info for each subject, stored as list
Drug = []
for x in range(len(Subject)):
    tempsub = Subject.iloc[x]
    tempdate = Date.iloc[x]
    tempdrug = input(f"Subject {tempsub} on date {tempdate} was on dose: ")
    Drug.append(tempdrug)

#Loop over subjects. Then loop for rows that start with 'DATA'. Then loop through everything, scraping out values that are attached to certain arbitrary signifiers ('200;;..') for each of the four measures. These four measures are collated for each subject. 
dfC = pd.DataFrame()
for x in range(nRat):
        leftlev=['']
        rightlev=['']
        magentry=['']
        pellet=['']
        
        for i in range(stIX[x], edIX[x]):
            if ('DATA' != (headers.iloc[i]).values[0]):
                continue
            row=T.iloc[i]
        
            for j in range(len(row)):
                tempstr=row[j]
                if(tempstr=='EOD'):
                    break
                if(tempstr[0:15] == '2002;ON;8;L(0);'):
                    leftlev.extend([tempstr[15:-1]])
                elif(tempstr[0:15] == '2002;ON;8;L(1);'):
                    rightlev.extend([tempstr[15:-1]])
                elif(tempstr[0:15] == '2002;ON;8;S(0);'):
                    magentry.extend([tempstr[15:-1]])
                elif(tempstr[0:15] == '2006;DS;9;P(0);'):
                    pellet.extend([tempstr[15:-1]])
        
#Create dataframes out of these 4 lists
        df1 = pd.DataFrame(leftlev)
        df2 = pd.DataFrame(rightlev)
        df3 = pd.DataFrame(magentry)
        df4 = pd.DataFrame(pellet)
        dfX = pd.concat([df1,df2,df3, df4], axis=1)


#Insert new rows via negative index which contain subject info and add headers. Merge into main data table.       
        dfX.loc[0,:] = Drug[x]
        dfX.loc[-1,:] = DBGroup[x]
        dfX.loc[-2,:] = Date[x]
        dfX.loc[-3,:] = Subject[x]
        dfX.index = dfX.index+3        
        dfX = dfX.sort_index()
        dfX.columns=['Left Lev', 'Right Lev', 'Mag Entry', 'Pellet']
        dfC = pd.concat([dfC, dfX], axis=1)
        dfC = dfC.fillna('')
        
                    
#Write data to CSV using date as filename (arbitrary index, all the same). Output file goes into active directory (location of .py)
FileDate = Date[1]
dfC.to_csv(f'ActvLog_{FileDate}.csv', encoding='utf-8', index=False)
print(f"Output file created ActvLog_{FileDate}.csv")






#
#
#         __             _,-"~^"-.
#       _// )      _,-"~`         `.
#     ." ( /`"-,-"`                 ;
#    / 6            nik              ;
#   /           ,    woz      ,-"     ;
#  (,__.--.      \  ere      /        ;
#   //'   /`-.\   |  2022    |        `._________
#     _.-'_/`  )  )--...,,,___\     \-----------,)
#   ((("~` _.-'.-'           __`-.   )         //
#         ((("`             (((---~"`         //
#                                            ((________________
#                                            `----""""~~~~^^^```
#          
#