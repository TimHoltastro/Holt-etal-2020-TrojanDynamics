#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 15:16:23 2018

@author: tim

--------Escape JT Ploting-------

Program to create plots for the Escaped Juptier Trojans
"""


import numpy as np
import pandas as pd
from scipy import stats
import scipy
from sklearn.metrics import r2_score
from datetime import datetime
import time
import sys
import subprocess
import glob
import matplotlib.pyplot as plt


#Bring in the CSV

filedata = pd.read_csv('JovTrojanEscapesDB-OrgescapeData-20190906-124940.csv')
#Putting in the SMA for clarity onto proper
filedata['da(AU)'] = filedata['da(AU)'] 

orig_stdout = sys.stdout

#making output text document.
textfile = 'EscapeRawData.txt'
sys.stdout = open(textfile, 'wt') 

L4data = filedata[filedata.L == 4]
L5data = filedata[filedata.L == 5]

#LibDB = pd.read_csv('JTLibrationDB-20180723-143803.csv', low_memory=False)
Astdys = pd.read_csv('/media/tim/Data/Trojan-Astdys-DataEnphems-20190828-134958.csv', low_memory=False)  #all data
#Putting in the SMA for clarity onto proper
Astdys['da(AU)'] = Astdys['da(AU)'] 

L4AstdysAll = Astdys[Astdys.L == 4]
L5AstdysAll = Astdys[Astdys.L == 5]

print('L4 escape shape: ', L4data.shape)
print('L4 shape: ', L4AstdysAll.shape)
print('L4 escape fraction: ', len(L4data.index) / len(L4AstdysAll.index))

print('L5 escape shape: ', L5data.shape)
print('L5 shape: ', L5AstdysAll.shape)
print('L5 escape fraction: ', len(L5data.index) / len(L5AstdysAll.index))

#selecting just the stable ones

L4Astdys = L4AstdysAll[~L4AstdysAll['Name'].isin(L4data['Name'])]
L5Astdys = L5AstdysAll[~L5AstdysAll['Name'].isin(L5data['Name'])]

#JTOrgData[~JTOrgData['JT'].isin(JTDiff['JT'])]


#----- Plot paramaters -----


cgrad = 'jet'  #Colormap for the gradients
#front size
plt.rcParams.update({'font.size': 20})
plt.rcParams.update({'figure.autolayout': True})

#L4 Scatter plots
#a vs e
plt.figure(4)
plt.title('L4 Escaped Trojans')
plt.xlabel('$\Delta a$ prop.')
plt.ylabel('e prop.')
#Astdyd data
L4jtaex = L4Astdys['da(AU)']
L4jtaey = L4Astdys['e_astdys']
plt.scatter(L4jtaex, L4jtaey, facecolor='none', edgecolor ='grey') #marker='.', c ='black'
#escape
L4jtaeEscx = L4data['da(AU)']
L4jtaeEscy = L4data['e_astdys']
plt.scatter(L4jtaeEscx, L4jtaeEscy, marker='x', c=L4data['EscapeTime'], cmap=cgrad)
plt.savefig('L4EscapesAE.png',bbox_inches='tight')
#Colorbar
#cbar = plt.colorbar(orientation="horizontal")
#cbar.set_label('Escape time (Gyr)', labelpad=15)
plt.show()

#a vs i
plt.figure(5)
plt.title('L4 Escaped Trojans')
plt.xlabel('$\Delta a$ prop.')
plt.ylabel('sinI')
#Astdyd data
L4jtaix = L4Astdys['da(AU)']
L4jtaiy = L4Astdys['sinI']
plt.scatter(L4jtaix, L4jtaiy,  facecolor='none', edgecolor ='grey')
#escape
L4jtaiEscx = L4data['da(AU)']
L4jtaiEscy = L4data['sinI']
plt.scatter(L4jtaiEscx, L4jtaiEscy, marker='x', c=L4data['EscapeTime'], cmap=cgrad)
plt.savefig('L4EscapesAI.png',bbox_inches='tight')
plt.show()

#L5 Scatter plots
#a vs e
plt.figure(6)
plt.title('L5 Escaped Trojans')
plt.xlabel('$\Delta a$ prop.')
plt.ylabel('e prop.')
#Astdyd data
L5jtaex = L5Astdys['da(AU)']
L5jtaey = L5Astdys['e_astdys']
plt.scatter(L5jtaex, L5jtaey,  facecolor='none', edgecolor ='grey')
#escape
L5jtaeEscx = L5data['da(AU)']
L5jtaeEscy = L5data['e_astdys']
plt.scatter(L5jtaeEscx, L5jtaeEscy, marker='x', c=L5data['EscapeTime'], cmap=cgrad)
plt.savefig('L5EscapesAE.png',bbox_inches='tight')
plt.show()

#a vs i
plt.figure(7)
plt.title('L5 Escaped Trojans')
plt.xlabel('$\Delta a$ prop.')
plt.ylabel('sinI')
#Astdyd data
L5jtaix = L5Astdys['da(AU)']
L5jtaiy = L5Astdys['sinI']
plt.scatter(L5jtaix, L5jtaiy,  facecolor='none', edgecolor ='grey')
#escape
L5jtaiEscx = L5data['da(AU)']
L5jtaiEscy = L5data['sinI']
plt.scatter(L5jtaiEscx, L5jtaiEscy, marker='x', c=L5data['EscapeTime'], cmap=cgrad)
plt.savefig('L5EscapesAI.png',bbox_inches='tight')
plt.show()



#closing the textfile
sys.stdout.close()
sys.stdout=orig_stdout  





