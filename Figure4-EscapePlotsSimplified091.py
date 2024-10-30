#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 15:16:23 2018

@author: tim

--------Escape JT Ploting-------

Program to create plots for the Escaped Juptier Trojans

07- updated for new databasefile that includes the Astdys data
08 - using fractions rather than absolute
09 - Pool adition.
Simplified - removal of the cumulative plots, simplified to just linear fit. 
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
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
matplotlib.rcParams.update({'font.size': 40})
#import matplotlib.axes as ax


#Bring in the CSV

Escapedata = pd.read_csv('JovTrojanEscapesDB-CloneescapeData-20200310-161455GT10km.csv', low_memory=False) #All clones
#Escapedata = pd.read_csv('JovTrojanEscapesDB-All9escapeData-20191025-161833.csv', low_memory=False) #Just those where all 9 clones escape
#Escapedata = pd.read_csv('JovTrojanEscapesDB-OrgescapeData-20191025-161833.csv', low_memory=False) #Reference particle (reemmber to change clone number to 1)
Alldata = pd.read_csv('Trojan-Astdys-DataEnphems-Family-Colours-20200309-171439GT10km.csv', low_memory=False)

#Number of clones
clonenum=9

#Size of the Histogram bins
BinNo=100

#--Calculations-- 

L4escapedata = Escapedata[Escapedata['L'] == 4]
L5escapedata = Escapedata[Escapedata['L'] == 5]

L4Alldata = Alldata[Alldata['L'] == 4]
L5Alldata = Alldata[Alldata['L'] == 5]

#Sizes

TotalNum = len(Alldata.index)*clonenum
L4Num = len(L4Alldata.index)*clonenum
L5Num = len(L5Alldata.index)*clonenum

#Volumes 
Totalvol = Alldata['vol_km3'].sum()*clonenum
L4vol = L4Alldata['vol_km3'].sum()*clonenum
L5vol = L5Alldata['vol_km3'].sum()*clonenum

TotalescapeVol = Escapedata['vol_km3'].sum()
L4escapeVol = L4escapedata['vol_km3'].sum()
l5escapeVol = L5escapedata['vol_km3'].sum()

#'large' escapes
largesize = 100             #what consitutes a 'large' asteroid
L4LargeAllData = L4Alldata[L4Alldata['diameter'] > largesize]
L4LargeAllDatasize = len(L4LargeAllData)*clonenum
l4LargeEscapeData = L4escapedata[L4escapedata['diameter'] > largesize]
L4LargeescapeVol = l4LargeEscapeData['vol_km3'].sum()

L5LargeAllData = L5Alldata[L5Alldata['diameter'] > largesize]
L5LargeAllDatasize = len(L5LargeAllData)*clonenum
l5LargeEscapeData = L5escapedata[L5escapedata['diameter'] > largesize]
L5LargeescapeVol = l5LargeEscapeData['vol_km3'].sum()


print('L4/L5 Volume ratio: ', L4vol/L5vol)
print('L4/L5 number ratio: ',L4Num/L5Num)
print()
print('Total size: ', TotalNum)
print('Total escape numbers: ', len(Escapedata.index))
print('Total escape number fraction: ', len(Escapedata.index) / TotalNum)
print('Total escape volume fraction: ', TotalescapeVol/Totalvol)
print()
print('L4 numbers: ', L4Num)
print('L4 number > {} km: {}'.format(largesize, L4LargeAllDatasize))
print('L4 escape numbers: ', len(L4escapedata.index))
print('L4 escape number > {} km: {}'.format(largesize, len(l4LargeEscapeData)))
print('L4 escape number fraction: ', len(L4escapedata.index)/ L4Num)
print('L4 escape volume fraction: ', L4escapeVol/L4vol)
print('L4 escape large as fraction of volume: ', L4LargeescapeVol/L4escapeVol)
print()
print('L5 numbers: ', L5Num)
print('L5 number > {} km: {}'.format(largesize, L5LargeAllDatasize))
print('L5 escape numbers: ', len(L5escapedata.index))
print('L5 escape number > {} km: {}'.format(largesize, len(l5LargeEscapeData)))
print('L5 escape number fraction: ', len(L5escapedata.index)/ (L5Num) )
print('L5 escape volume fraction: ', l5escapeVol/L5vol)
print('L5 escape large as fraction of volume: ', L5LargeescapeVol/l5escapeVol)



#selecting just the stable ones

L4Stable = L4Alldata[~L4Alldata['Name'].isin(L4escapedata['Name'])]
L5Stable = L5Alldata[~L5Alldata['Name'].isin(L5escapedata['Name'])]

#JTOrgData[~JTOrgData['JT'].isin(JTDiff['JT'])]
print()
print('---Anlaysis---')
#L4/L5 data Historgrams

binsize = Escapedata.EscapeTime.max() / BinNo
print('Binsize:', binsize)

#Plotsetups
linew = 3



#-----Both-------
print('-----Both-------')

figno=1                                 #just a way to make cululative figures

#------noncumulative----------
#Graph
figno = figno+1
#fig = plt.figure(figno)
fig, ax = plt.subplots(num=figno)
plt.title('Jovian Trojan Escapees')
plt.xlabel('Time (Gyr)')
plt.ylabel('Escape perc.')
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1,))  #Y axis as percentiles from decimals

popncnum, popncbin, popncbar = plt.hist(Escapedata['EscapeTime'], cumulative=False, bins=BinNo, weights=np.zeros_like(Escapedata['EscapeTime']) + 1. / TotalNum, color='gray')  #histogram

popnccenters = 0.5*(popncbin[1:]+ popncbin[:-1])   #Center of bins

#plt.scatter(popcenters,popnum)

#make into array
popncescapearay = pd.DataFrame(data = {'EscapeYear': popnccenters, 'Counts': popncnum})

#Linear 
print('--Linear fit')
popLincoef = np.polyfit(popncescapearay['EscapeYear'], popncescapearay['Counts'], 1)
print(popLincoef)
popLinequ = np.poly1d(popLincoef)       #the Equation
print(popLinequ)
popLinequbin = popLinequ * binsize
popLinr2 = r2_score(popncescapearay['Counts'], popLinequ(popncescapearay['EscapeYear']))        #R^2 value
print(popLinr2)
plt.plot(popncescapearay['EscapeYear'], popLinequ(popncescapearay['EscapeYear']),label = 'Linear:{}'.format(round(popLinr2,2)), color = 'black', linewidth=linew)

plt.legend()
plt.show()




#-------------------------------L4----------------------------------------------------------
print('-----L4-------')

#--noncumulative
#Graph
figno = figno+1
#plt.figure(figno)
fig, ax = plt.subplots(num=figno)
plt.title('Jovian Trojan L4 Escapees')
plt.xlabel('Time (Gyr)')
plt.ylabel('Frac. Escape')

l4ncnum, l4ncbin, l4ncbar = plt.hist(L4escapedata['EscapeTime'], cumulative=False, bins=BinNo, weights=np.zeros_like(L4escapedata['EscapeTime']) + 1. / L4Num, color='gray')  #histogram

l4nccenters = 0.5*(l4ncbin[1:]+ l4ncbin[:-1])   #Center of bins

#plt.scatter(l4centers,l4num)

#make into array
l4ncescapearay = pd.DataFrame(data = {'EscapeYear': l4nccenters, 'Counts': l4ncnum})

#Linear 
print('--Linear fit')
l4Lincoef = np.polyfit(l4ncescapearay['EscapeYear'], l4ncescapearay['Counts'], 1)
#print(l4Lincoef)
l4Linequ = np.poly1d(l4Lincoef)       #the Equation
print(l4Linequ)
l4Linequbin = l4Linequ * binsize
l4Linr2 = r2_score(l4ncescapearay['Counts'], l4Linequ(l4ncescapearay['EscapeYear']))        #R^2 value
print(l4Linr2)
plt.plot(l4ncescapearay['EscapeYear'], l4Linequ(l4ncescapearay['EscapeYear']),label = 'Linear:{}'.format(round(l4Linr2,2)), color = 'black', linewidth=linew)


plt.legend()
plt.show()


#-------------------------------L5----------------------------------------------------------
print('-----L5-------')

#--noncumulative
#Graph
figno = figno+1
#plt.figure(figno)
fig, ax = plt.subplots(num=figno)
plt.title('Jovian Trojan l5 Escapees')
plt.xlabel('Time (Gyr)')
plt.ylabel('Frac. Escape')

l5ncnum, l5ncbin, l5ncbar = plt.hist(L5escapedata['EscapeTime'], cumulative=False, bins=BinNo, weights=np.zeros_like(L5escapedata['EscapeTime']) + 1. / L5Num, color='gray')  #histogram

l5nccenters = 0.5*(l5ncbin[1:]+ l5ncbin[:-1])   #Center of bins

#plt.scatter(l5centers,l5num)

#make into array
l5ncescapearay = pd.DataFrame(data = {'EscapeYear': l5nccenters, 'Counts': l5ncnum})

#Linear 
print('--Linear fit')
l5Lincoef = np.polyfit(l5ncescapearay['EscapeYear'], l5ncescapearay['Counts'], 1)
print(l5Lincoef)
l5Linequ = np.poly1d(l5Lincoef)       #the Equation
print(l5Linequ)
l5Linequbin = l5Linequ * binsize
l5Linr2 = r2_score(l5ncescapearay['Counts'], l5Linequ(l5ncescapearay['EscapeYear']))        #R^2 value
print(l5Linr2)
plt.plot(l5ncescapearay['EscapeYear'], l5Linequ(l5ncescapearay['EscapeYear']),label = 'Linear:{}'.format(round(l5Linr2,2)), color = 'black', linewidth=linew)


plt.legend()
plt.show()

#----- Larger supplots
figno = figno+1
fig, (popplt, l4plt, l5plt) = plt.subplots(1,3, num=figno, sharey=True, squeeze=True)
popplt.set_ylabel('Escape perc.')


#Population
popplt.set_title('Population Escapees')
popplt.set_xlabel('Time (Gyr)')
popplt.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1,))  #Y axis as percentiles from decimals

popplt.hist(Escapedata['EscapeTime'], cumulative=False, bins=BinNo, weights=np.zeros_like(Escapedata['EscapeTime']) + 1. / TotalNum, color='gray')  #histogram
popplt.plot(popncescapearay['EscapeYear'], popLinequ(popncescapearay['EscapeYear']),label = 'Linear:{}'.format(round(popLinr2,2)), color = 'black', linewidth=linew)
popplt.legend()

#L4
l4plt.set_title('L4 Swarm Escapees')
l4plt.set_xlabel('Time (Gyr)')
l4plt.hist(L4escapedata['EscapeTime'], cumulative=False, bins=BinNo, weights=np.zeros_like(L4escapedata['EscapeTime']) + 1. / L4Num, color='gray')  #histogram

l4plt.plot(l4ncescapearay['EscapeYear'], l4Linequ(l4ncescapearay['EscapeYear']),label = 'Linear:{}'.format(round(l4Linr2,2)), color = 'black', linewidth=linew)

l4plt.legend()

#l5
l5plt.set_title('L5 Swarm Escapees')
l5plt.set_xlabel('Time (Gyr)')
l5plt.hist(L5escapedata['EscapeTime'], cumulative=False, bins=BinNo, weights=np.zeros_like(L5escapedata['EscapeTime']) + 1. / L5Num, color='gray')  #histogram
l5plt.plot(l5ncescapearay['EscapeYear'], l5Linequ(l5ncescapearay['EscapeYear']),label = 'Linear:{}'.format(round(l5Linr2,2)), color = 'black', linewidth=linew)

l5plt.legend()

plt.show()


#------------- Escape equations---------

figno = figno+1
#plt.figure(figno)
fig, ax = plt.subplots(num=figno)
plt.title('Jovian Trojan escape equations')
plt.xlabel('Time (Gyr)')
plt.ylabel('Perc. Escape')
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1,))  #Y axis as percentiles from decimals
escapearrayyearPos = popncescapearay['EscapeYear']
escapearrayyearneg = np.negative(escapearrayyearPos)

escapearrayyear = np.linspace(-popncescapearay['EscapeYear'].max(), popncescapearay['EscapeYear'].max(), num=2*BinNo) #creating a linear set of numbers.


'''
#ratio of L4 to L5
ratioL4L5 = l4poly3dregequ(escapearrayyear) / l5poly3dregequ(escapearrayyear)
plt.plot(escapearrayyear, ratioL4L5, color = 'black', linewidth=linew)
'''

#both
plt.plot(escapearrayyear, popLinequ(escapearrayyear), label = 'Both:{}'.format(round(popLinr2,2)), color = 'black', linewidth=linew)
#L4
plt.plot(escapearrayyear, l4Linequ(escapearrayyear), label = 'L4:{}'.format(round(l4Linr2,2)), color = 'black', linewidth=linew, linestyle='dashed')
#L5
plt.plot(escapearrayyear, l5Linequ(escapearrayyear), label = 'L5:{}'.format(round(l5Linr2,2)), color = 'black', linewidth=linew, linestyle='dotted')
#vertilce line
plt.axvline(x=0, color = 'lightgray', linewidth=linew, linestyle='dashed')

plt.legend()
plt.show()


#------------L4 vs L5------------------
#---integrals---


#Both 
#clones
pastescapeboth = scipy.integrate.quad(popLinequ, -4.5e9/binsize, 0)
Furuteescapeboth = scipy.integrate.quad(popLinequ, 0, 4.5e9/binsize)
pastescapenumberclone = pastescapeboth[0]*TotalNum + TotalNum
Futureescapesclone = Furuteescapeboth[0]*TotalNum 
FuturePopunumberclone = TotalNum - Futureescapesclone
#divided by clone num
currentnumberboth = L4Num/clonenum + L5Num/clonenum
pastescapenumber = pastescapenumberclone/clonenum


#L4 
#Clones
pastescapeL4 = scipy.integrate.quad(l4Linequ, -4.5e9/binsize, 0)
FuruteescapeL4 = scipy.integrate.quad(l4Linequ, 0, 4.5e9/binsize)
pastescapenumbercloneL4 = pastescapeL4[0]*L4Num + L4Num
FutureescapescloneL4 = FuruteescapeL4[0]*L4Num 
FuturePopunumbercloneL4 = L4Num - FutureescapescloneL4

#divided by clone num
L4currenttotal = L4Num/clonenum


#L5
#clones
pastescapeL5 = scipy.integrate.quad(l5Linequ, -4.5e9/binsize, 0)
FuruteescapeL5 = scipy.integrate.quad(l5Linequ, 0, 4.5e9/binsize)
pastescapenumbercloneL5 = pastescapeL5[0]*L5Num + L5Num
FutureescapescloneL5 = FuruteescapeL5[0]*L5Num 
FuturePopunumbercloneL5 = L5Num - FutureescapescloneL5
#divided by clone num
L5currenttotal = L5Num/clonenum


#Print info
print('---Past population---')
print('-Population-')
print('Clone past number:',pastescapenumberclone)
print('Clone past fraction:', pastescapenumberclone/TotalNum)
print('Clone Future number:',FuturePopunumberclone)
print('Clone Future fraction:', FuturePopunumberclone/TotalNum)
print('predicted vs Future Escapes : ', Futureescapesclone/len(Escapedata.index))
print('Acct. past number:', pastescapenumberclone/clonenum)
print('')
print('-L4-')
print('Clone past number:',pastescapenumbercloneL4)
print('Clone past fraction:', pastescapenumbercloneL4/L4Num)
print('Clone Future number:',FuturePopunumbercloneL4)
print('Clone Future fraction:', FuturePopunumbercloneL4/L4Num)
print('Future Escapes vs predicted: ', FutureescapescloneL4/len(L4escapedata.index))
print('Acct. past number:', pastescapenumbercloneL4/clonenum)
print('')
print('-L5-')
print('Clone past number:',pastescapenumbercloneL5)
print('Clone past fraction:', pastescapenumbercloneL5/L5Num)
print('Clone Future number:',FuturePopunumbercloneL5)
print('Clone Future fraction:', FuturePopunumbercloneL5/L5Num)
print('Future Escapes vs predicted: ', FutureescapescloneL5/len(L5escapedata.index))
print('Acct. past number:', pastescapenumbercloneL5/clonenum)
print('')
print('-Ratio-')
print('Past ratio: ', pastescapenumbercloneL4/pastescapenumbercloneL5)

BinNo
binsize

#population dataframe
popDatabase = pd.DataFrame(columns = ['escapeyear', 'bothClone', 'L4Clone', 'L5Clone', 'both', 'L4', 'L5', 'bothpc', 'L4pc', 'L5pc'])
popDatabase['escapeyear'] = escapearrayyear

for index, row in popDatabase.iterrows():
    if row['escapeyear'] < 0:
        Clonesizeboth = scipy.integrate.quad(popLinequ, row['escapeyear']/binsize, 0) 
        popDatabase.at[index, 'bothClone'] = Clonesizeboth[0]*TotalNum + TotalNum 
        ClonesizeL4 = scipy.integrate.quad(l4Linequ, row['escapeyear']/binsize, 0)
        popDatabase.at[index, 'L4Clone'] = ClonesizeL4[0]*L4Num + L4Num 
        ClonesizeL5 = scipy.integrate.quad(l5Linequ, row['escapeyear']/binsize, 0)
        popDatabase.at[index, 'L5Clone'] = ClonesizeL5[0]*L5Num + L5Num 
    elif row['escapeyear'] == 0:
        popDatabase.at[index, 'bothClone'] = TotalNum 
        popDatabase.at[index, 'L4Clone'] = L4Num  
        popDatabase.at[index, 'L5Clone'] =  L5Num
    elif row['escapeyear'] > 0:
        Clonesizeboth = scipy.integrate.quad(popLinequ, 0, row['escapeyear']/binsize)
        popDatabase.at[index, 'bothClone'] = TotalNum - Clonesizeboth[0]*TotalNum
        ClonesizeL4 = scipy.integrate.quad(l4Linequ, 0, row['escapeyear']/binsize)
        popDatabase.at[index, 'L4Clone'] = L4Num - ClonesizeL4[0]*L4Num
        ClonesizeL5 = scipy.integrate.quad(l5Linequ, 0, row['escapeyear']/binsize) 
        popDatabase.at[index, 'L5Clone'] = L5Num - ClonesizeL5[0]*L5Num


popDatabase['both'] = popDatabase['bothClone']/clonenum
popDatabase['L4'] = popDatabase['L4Clone']/clonenum
popDatabase['L5'] = popDatabase['L5Clone']/clonenum
popDatabase['Ratio'] = popDatabase['L4Clone']/popDatabase['L5Clone']

popDatabase['bothpc'] = popDatabase['bothClone']/TotalNum
popDatabase['L4pc'] = popDatabase['L4Clone']/L4Num
popDatabase['L5pc'] = popDatabase['L5Clone']/L5Num

figno = figno+1
#plt.figure(figno)
fig, ax = plt.subplots(num=figno)
#plt.title('Total number in Jovian Trojan Swarm')
plt.xlabel('Time (Gyr)')
plt.ylabel('Total Numbers')


#both
plt.plot(popDatabase['escapeyear'], popDatabase['both'], label = 'All'.format(), color = 'black', linewidth=linew)
#L4
plt.plot(popDatabase['escapeyear'], popDatabase['L4'], label = 'L4'.format(), color = 'black', linewidth=linew, linestyle='dashed')
#L5
plt.plot(popDatabase['escapeyear'], popDatabase['L5'], label = 'L5'.format(), color = 'black', linewidth=linew, linestyle='dotted')

plt.legend(loc=9, ncol=3)
#ratio
ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
ax2.plot(popDatabase['escapeyear'], popDatabase['Ratio'], color = 'gray', linewidth=linew, label='L4/L5 ratio')
ax2.tick_params(axis='y', labelcolor='gray')
ax2.set_ylabel('L4/L5 ratio', color='gray')

#vertilce line
plt.axvline(x=0, color = 'lightgray', linewidth=linew/2, linestyle='dashed')

plt.show()


figno = figno+1
#plt.figure(figno)
fig, ax = plt.subplots(num=figno)
plt.title('Total numbers')
plt.xlabel('Time (Gyr)')
plt.ylabel('Total Percentages')

ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1,)) 


#both
plt.plot(popDatabase['escapeyear'], popDatabase['bothpc'], label = 'Both:'.format(), color = 'black', linewidth=linew)
#L4
plt.plot(popDatabase['escapeyear'], popDatabase['L4pc'], label = 'L4'.format(), color = 'black', linewidth=linew, linestyle='dashed')
#L5
plt.plot(popDatabase['escapeyear'], popDatabase['L5pc'], label = 'L5'.format(), color = 'black', linewidth=linew, linestyle='dotted')


#vertilce line
plt.axvline(x=0, color = 'lightgray', linewidth=linew, linestyle='dashed')

plt.legend()
fig.tight_layout()
plt.show()




#Ratio
figno = figno+1
#plt.figure(figno)
fig, ax = plt.subplots(num=figno)
plt.title('L4/L5 total number ratio')
plt.xlabel('Time (Gyr)')
plt.ylabel('Ratio')

#Escaperatio = L4integ(-escapearrayyear/binsize) / L5integ(-escapearrayyear/binsize)
#Escaperatio = L4integ(escapearrayyear/clonenum) / L5integ(escapearrayyear/clonenum)
plt.plot(popDatabase['escapeyear'], popDatabase['Ratio'], color = 'black', linewidth=linew)
#vertilce line
plt.axvline(x=0, color = 'lightgray', linewidth=linew, linestyle='dashed')

plt.show()

















