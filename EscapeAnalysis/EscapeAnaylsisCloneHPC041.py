#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 14:05:03 2018

---------Sim Escape Data Analysis--------

@author: Tim

This program analyses data on Escaped Jovian Trojans. The program merges the escape database with a larger DB. 

HPC: Adjsuted to work on the USQ HPC
Clone: Merges the clone files
04: using a def and cleaned up.
041: get rid of Mean
042: add in the 'clone' to make it easier to Search

"""



import numpy as np
import pandas as pd
from datetime import datetime
import time
import sys
import subprocess
import glob
import matplotlib.pyplot as plt



#Files
JTOrgFile = 'JovTrojanEscapes-org-JT45e9_1e5_8clone-20200222-104301.csv'

#JTDatafile = '/home/u8007759/JTData/Trojan-Astdys-DataEnphems-20190828-134958.csv'  #HPC
JTDatafile = '/media/tim/Data/Trojan-Astdys-DataEnphems-20190828-134958.csv' #Local workstation


#generating
DatetimeNow = time.strftime("%Y%m%d-%H%M%S")
JTOrgData = pd.read_csv(JTOrgFile, low_memory=False)
#--FullData--
JTData = pd.read_csv(JTDatafile, low_memory=False)


#Joiing the clone DBs
Clonefiles = glob.glob('JovTrojanEscapes-clone-*.csv')
Clonefiles.sort()
JTEscapeDataPerJT = JTOrgData  #DF that has each JT with the escape of the relative clones
JTEscapeDataClone = JTOrgData #to merge in each of the clones as a seperate Trojan
JTEscapeDataClone['JT_Clone'] = JTEscapeDataClone['JT'] + '_org'
JTEscapeDataClone['Clone'] = 'org'
print('Original')
print('Original Shape:',JTEscapeDataPerJT.shape)
print('-----------')

for file in Clonefiles:
    escapedata = pd.read_csv(file, low_memory=False)
    filenamesplit = file.split('-')    #splitting the file name
    clonenumb = filenamesplit[2]
    CloneNumbLable = 'Clone_'+clonenumb
    print(CloneNumbLable)
    print('Clone Shape: ',escapedata.shape)
    #joining them to the original - Not that usefull
    JTEscapeDataPerJT = JTEscapeDataPerJT.merge(escapedata, how='outer', suffixes=('','_'+CloneNumbLable), on='JT')
    print(JTEscapeDataPerJT.shape)
    
    #Adding in new suffix
    escapedata['JT_Clone'] = escapedata['JT'] + '_' + CloneNumbLable
    escapedata['Clone'] = 'clone-'+clonenumb
    JTEscapeDataClone = JTEscapeDataClone.append(escapedata)
    print(JTEscapeDataClone.shape)
    
    print('-----------')

print(JTEscapeDataClone.dtypes)    
''''    
#Number of escapes
JTEscapeData['N_escape'] = 9-(round(JTEscapeData.isnull().sum(axis=1)/3))
#print(JTEscapeData['N_escape'])  

EscapeCount = JTEscapeData['N_escape'].value_counts(ascending=True, sort = False)
EscapecountDB = pd.DataFrame(EscapeCount.sort_index())
EscapecountDB['N_cum'] = EscapecountDB['N_escape'].cumsum()
'''

#---DB output-----
#Only those with 9 escapes
JTEscapeDataPerJTAllclone = JTEscapeDataPerJT.dropna()
JTEscapeDataPerJTAllclone.to_csv('JovTrojanEscapes-All9Clone-JT45e9_1e5_8clone-{}.csv'.format(DatetimeNow), index=False) 

#BD with each clone as an idividual
JTEscapeDataClone.to_csv('JovTrojanEscapes-IndiClones-JT45e9_1e5_8clone-{}.csv'.format(DatetimeNow), index=False) 

#joinging the DB's to the larger DB

def Databasejoin(DB, DBname):
    DBcombined = DB.merge(JTData,how='inner', suffixes=('','_r'), left_on='JT', right_on='Name')
    DBcombined.to_csv(DBname, index=False)


Databasejoin(JTEscapeDataPerJTAllclone, 'JovTrojanEscapesDB-All9escapeData-{}.csv'.format(DatetimeNow))  #only those with all 9 clones escaping
Databasejoin(JTEscapeDataClone, 'JovTrojanEscapesDB-CloneescapeData-{}.csv'.format(DatetimeNow))         #Each clone treated seperatly
Databasejoin(JTOrgData, 'JovTrojanEscapesDB-OrgescapeData-{}.csv'.format(DatetimeNow))                   #The original enphemerise particles escape







