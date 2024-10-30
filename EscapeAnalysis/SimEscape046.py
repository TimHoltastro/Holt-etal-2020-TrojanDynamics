#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Mar 26 14:44:25 2018

---------Sim Escape Data--------

@author: Tim

This program is to get infromation from the REBOUND sims and itterate over multipul files. The aim is to find the Trojans that escape the Cloud.

04 - Updated to accept the extension as a input

"""



import numpy as np
import pandas as pd
from datetime import datetime
import time
import sys
import subprocess
import glob
import matplotlib.pyplot as plt
import math

#extenstion = 'clone-1'                #org is the original, clone-1 to 8 is the clones number

#using Argparse as inputs
import argparse
parser = argparse.ArgumentParser(prefix_chars='@')
parser.add_argument("CloneName", help="Clone name: org is the original, clone-1 to 8 is the clones number") 

args = parser.parse_args()
extenstion = args.CloneName

outlimit = 5.5
inlimit = 4.6

#on hpsc or Workstation
#loc = '/media/tim/Data'  #local on the workstation
loc = '/home/u8007759'    #for on the hpc

#Directory
direc = 'JT45e9_1e5_8clone'       #usually 'JT45e9_1e5_8clone'

# Make a list of all the CSV filenames
csvfiles = glob.glob('{}/{}/*Sim*-{}.csv'.format(loc,direc,extenstion))


#Creating a text file.
DatetimeNow = time.strftime("%Y%m%d-%H%M%S")
orig_stdout = sys.stdout
outputtext = 'Escaped-Trojans-{}-{}-{}.txt'.format(extenstion, direc, DatetimeNow)
sys.stdout = open(outputtext, 'wt')

#Creating a DB
escapedTJColum = ['JT', 'Escape', 'EscapeTime', 'Ejection']
escaptedJT = pd.DataFrame([], columns = escapedTJColum)


print('--------- List of Escaped Trojans----------')
#number of escapted 
escapeout = 0
escapein = 0
start = datetime.now()        #start time

print('Total Trojans Analysed: ', len(csvfiles))
print('Escape out limit: ', outlimit)
print('Escape in limit: ', inlimit)

for file in csvfiles:
    filedata = pd.read_csv(file)
    namesplit = file.split('-')
    name = namesplit[1]
    JTtime = datetime.now() - start
    print(name, file=sys.stderr)
    #indiDatetimeNow = time.strftime("%Y%m%d-%H%M%S")
    print(JTtime, file=sys.stderr)
    #max and min
    MaxA = filedata['a'].max()
    MaxData = filedata.loc[filedata['a'].idxmax()]
    MaxTime=MaxData['Time']
    MinA = filedata['a'].min()
    MinData = filedata.loc[filedata['a'].idxmin()]
    MinTime=MinData['Time']
    #Calculating distance
    for index, row in filedata.iterrows():
        dist = math.sqrt(row['x']**2 + row['y']**2 + row['z']**2)
        filedata.at[index,'SSdist'] = dist
    
    #Escaping out
    if (filedata['a'] > outlimit).any():
        escapeout = escapeout+1
        escapeTJ = filedata.loc[filedata['a'] > outlimit, 'Time'].iloc[0]  #Get the time when it escapes the cloud
        try:
            ejectionTJ = filedata.loc[filedata['SSdist'] > 1000, 'Time'].iloc[0]  #Get the time when it is ejected
            indiTJ = pd.DataFrame([[name, 'out', escapeTJ, ejectionTJ]], columns = escapedTJColum)
        except:
            indiTJ = pd.DataFrame([[name, 'out', escapeTJ, np.nan]], columns = escapedTJColum)
        escaptedJT = escaptedJT.append(indiTJ,ignore_index=True)
        print('{} escaped out at {}'.format(name, escapeTJ))

    #Escaping in
    elif (filedata['a'] < inlimit).any():
            escapein = escapein+1
            escapeTJ = filedata.loc[filedata['a'] < inlimit, 'Time'].iloc[0]  #Get the time when it escapes the cloud
            try:
                ejectionTJ = filedata.loc[filedata['SSdist'] > 1000, 'Time'].iloc[0]  #Get the time when it is ejected if it is
                indiTJ = pd.DataFrame([[name, 'in', escapeTJ, ejectionTJ]], columns = escapedTJColum)
            except:
                indiTJ = pd.DataFrame([[name, 'in', escapeTJ, np.nan]], columns = escapedTJColum)
            escaptedJT = escaptedJT.append(indiTJ,ignore_index=True)
            print('{} escaped in at {}'.format(name,escapeTJ))


#output to CSV
DatetimeNow = time.strftime("%Y%m%d-%H%M%S")
escaptedJT.to_csv('JovTrojanEscapes-{}-{}-{}.csv'.format(extenstion,direc,DatetimeNow), index=False)            
              
            
print('Total escaped out:{}'.format(escapeout))
print('Total escaped in:{}'.format(escapein))
totalescape = escapeout+escapein
print('Total escaped:{}'.format(totalescape))

sys.stdout.close()
sys.stdout=orig_stdout 

