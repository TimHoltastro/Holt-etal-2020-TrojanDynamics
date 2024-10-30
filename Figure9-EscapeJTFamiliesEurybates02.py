#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 17:12:02 2019

-------Escape aanlysis for the Eurybates family-------


@author: tim

02 - updated to use the 

"""

import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.metrics import r2_score
import time
import sys
import subprocess
import glob
import matplotlib.pyplot as plt
import sympy
import scipy
import matplotlib.ticker as ticker
import matplotlib
matplotlib.rcParams.update({'font.size': 22})
#matplotlib.use('Agg')

#Files
JTFamfile = 'JTFamiles.csv'
#JTFile = 'JovTrojanEscapesDB-OrgescapeData-20190906-124940.csv'
JTFile = 'JovTrojanEscapesDB-CloneescapeData-20190906-124940.csv'
Alldata = pd.read_csv('/media/tim/Data/Trojan-Astdys-DataEnphems-20190828-134958.csv', low_memory=False)

clonenum = 9

PropEle = pd.read_csv('ASTDy-Trojan.syn', delim_whitespace=True)

#generating
DatetimeNow = time.strftime("%Y%m%d-%H%M%S")
JTEscapeData = pd.read_csv(JTFile, low_memory=False)
JTfamData = pd.read_csv(JTFamfile)

BinNo = 10
binsize = JTEscapeData.EscapeTime.max() / BinNo
print(binsize)
linew = 3

cgrad = 'jet'  #Colormap for the gradients

#merg family set with proper
#JTfamData['FAMILY_NUMBER'] = JTfamData['FAMILY_NUMBER'].astype(int)

JTfamData['Ast.No'] = JTfamData['Ast.No'].astype(np.str)
JTfamData = JTfamData.rename(columns = {'Ast.No':'Name'})
JTfamData = JTfamData.rename(columns = {'da(AU)':'da_prop'})

#PropEleIndexed = PropEle.set_index('Name', drop=False)
#JTfamDataIndexed = JTfamData.set_index('Name', drop=False)


#FamEle = PropEleIndexed.join(JTfamDataIndexed, lsuffix='', rsuffix='_y')
FamEle = pd.merge(PropEle, JTfamData, how='outer', on='Name')
FamEle = FamEle.rename(columns = {'da(AU)':'da_prop'})
FamEle = FamEle.rename(columns = {'e_astdys':'e_prop'})
FamEle = FamEle.rename(columns = {'sinI':'sinI_prop'})

#Justfamily
FamDataAll = pd.merge(Alldata, JTfamData, how='inner', on='Name')


#Getting just the family members
justFamProp = FamEle.dropna()



#family members that escape
famEscape = pd.merge(justFamProp, JTEscapeData, how='inner', on='Name', suffixes=('', '_y'))
#cleaning up the duplicate columns
def drop_y(df):
    # list comprehension of the cols that end with '_y'
    to_drop = [x for x in df if x.endswith('_y')]
    df.drop(to_drop, axis=1, inplace=True)
drop_y(famEscape)




#print(famEscape)

#output to csv
#famEscape.to_csv('JovTrojanEscapes-OrgFamilymembers-{}.csv'.format(DatetimeNow), index=False)


#--------Plots-------


#selecting the individual sets
figno=1
#L4
L4FamEleAll = FamEle[FamEle.L==4]                                                #all L4
L4AstdysStab = L4FamEleAll[~L4FamEleAll['Name'].isin(JTEscapeData['Name']) & L4FamEleAll.FAMILY_NAME.isna()]    #L4 stable non families
L4AstdysEsc = L4FamEleAll[L4FamEleAll['Name'].isin(JTEscapeData['Name']) & L4FamEleAll.FAMILY_NAME.isna()]      #L4 Escaped non families
L4Fam = justFamProp[justFamProp.L==4]                    #L4 family members
L4FamStab = L4Fam[~L4Fam['Name'].isin(JTEscapeData['Name'])]   #L4 stable family members
L4FamEscape = famEscape[famEscape.L==4]   #L4 Escaped family members



#-----------------------------Eurybates family-------------------------------------------

print('---Eurybates family-----')
EuryStable = L4FamStab[L4FamStab['FAMILY_NAME'] == ' 3548 Eurybates']
EuryEscape = L4FamEscape[L4FamEscape['FAMILY_NAME'] == ' 3548 Eurybates']
Eurydata = EuryEscape
EuryNum = len(Eurydata.index)*clonenum
#-------------------a vs e---------------------
figno = figno+1
plt.figure(figno)
plt.title('Eurybates family')
plt.xlabel('$\Delta a$ prop.')
plt.ylabel('e prop.')
plt.xlim(right=0.125, left = 0.04)
plt.ylim(top=0.075, bottom=0.03)
'''
#Stable Trojans 
L4jtaex = L4AstdysStab['da_prop']
L4jtaey = L4AstdysStab['e_prop']
plt.scatter(L4jtaex, L4jtaey, facecolor='none', edgecolor ='grey') #marker='.', c ='black'
#escaped Trojans
L4jtaeEscx = L4AstdysEsc['da_prop']
L4jtaeEscy = L4AstdysEsc['e_prop']
plt.scatter(L4jtaeEscx, L4jtaeEscy, marker='x', c='grey')
'''
#---------families
#--Eurybates
#stable
L4jtFam1aex = EuryStable.da_prop
L4jtFam1aey = EuryStable.e_prop
plt.scatter(L4jtFam1aex, L4jtFam1aey, facecolor='none', edgecolor ='grey') #marker='$1$',  c='black'

#Escaped
L4jtaeFam1Escx = EuryEscape.da_prop
L4jtaeFam1Escy = EuryEscape.e_prop
plt.scatter(L4jtaeFam1Escx, L4jtaeFam1Escy, marker='x', c=EuryEscape.EscapeTime, cmap=cgrad)

plt.savefig('EurybatesAE.png',bbox_inches='tight')
#plt.show()

#-------------------a vs i---------------------
figno = figno+1
plt.figure(figno)
plt.title('Eurybates family')
plt.xlabel('$\Delta a$ prop.')
plt.ylabel('sinI prop.')
plt.xlim(right=0.125, left = 0.04)
plt.ylim(top=0.14, bottom=0.12)
'''
#Stable Trojans 
L4jtaex = L4AstdysStab['da_prop']
L4jtaey = L4AstdysStab['sinI_prop']
plt.scatter(L4jtaex, L4jtaey, facecolor='none', edgecolor ='grey') #marker='.', c ='black'
#escaped Trojans
L4jtaeEscx = L4AstdysEsc['da_prop']
L4jtaeEscy = L4AstdysEsc['sinI_prop']
plt.scatter(L4jtaeEscx, L4jtaeEscy, marker='x', c='grey')
'''

#--Eurybates

#stable
L4jtFam1aex = EuryStable.da_prop
L4jtFam1aey = EuryStable.sinI_prop
plt.scatter(L4jtFam1aex, L4jtFam1aey,  facecolor='none', edgecolor ='grey') #marker='$1$', c='black'
#Escaped
L4jtaeFam1Escx = EuryEscape.da_prop
L4jtaeFam1Escy = EuryEscape.sinI_prop
plt.scatter(L4jtaeFam1Escx, L4jtaeFam1Escy, marker='x', c=EuryEscape.EscapeTime, cmap=cgrad)


#cbar = plt.colorbar()
#cbar.set_label('Escape time (yrs)', rotation=270, labelpad=15)

plt.savefig('EurybatesAI.png',bbox_inches='tight')
##plt.show()


#-------------------------------Regression escape analysis----------------------------------------------------------
print('-----Eurybates-------')
#Histogram of escape time
figno = figno+1
fig, ax = plt.subplots(num=figno)
plt.title('Eurybates Escapes')
plt.xlabel('Time (Gyr)')
plt.ylabel('No. Escaped')
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1,))  #Y axis as percentiles from decimals
Eurynum, Eurybin, Eurybar = plt.hist(Eurydata['EscapeTime'], cumulative=True, bins=BinNo, weights=np.zeros_like(Eurydata['EscapeTime']) + 1. / EuryNum, color='gray') #histogram

#plt.hist(L5data['EscapeTime'], cumulative=False, bins=100, stacked=True)

Eurycenters = 0.5*(Eurybin[1:]+ Eurybin[:-1])   #Center of bins

#plt.scatter(Eurycenters,Eurynum)

#make into array
Euryescapearay = pd.DataFrame(data = {'EscapeYear': Eurycenters, 'Counts': Eurynum})


#------regression------

print('--Cumulative Poly 2 fit')
Eurypoly2coef = np.polyfit(Euryescapearay['EscapeYear'], Euryescapearay['Counts'], 2)
print(Eurypoly2coef)
#Eurypoly2equ = Eurypoly2coef[0]*Euryescapearay['EscapeYear']**2 + Eurypoly2coef[1]*Euryescapearay['EscapeYear'] + Eurypoly2coef[2]
Eurypoly2equ = np.poly1d(Eurypoly2coef)       #the Equation
print(Eurypoly2equ)
Eurypoly2r2 = r2_score(Euryescapearay['Counts'], Eurypoly2equ(Euryescapearay['EscapeYear']))        #R^2 value
print(Eurypoly2r2)

plt.plot(Euryescapearay['EscapeYear'], Eurypoly2equ(Euryescapearay['EscapeYear']), label = '2nd poly: {}'.format(round(Eurypoly2r2,3)), color = 'black', linestyle='dashed', linewidth=linew)

print('--Cumulative Poly 3 fit')
Eurypoly3coef = np.polyfit(Euryescapearay['EscapeYear'], Euryescapearay['Counts'], 3)
print(Eurypoly3coef)
#Eurypoly3equ = Eurypoly3coef[0]*Euryescapearay['EscapeYear']**3 + Eurypoly3coef[1]*Euryescapearay['EscapeYear']**2 + Eurypoly3coef[2]*Euryescapearay['EscapeYear'] + Eurypoly3coef[3]
Eurypoly3equ = np.poly1d(Eurypoly3coef)       #the Equation
print(Eurypoly3equ)
Eurypoly3r2 = r2_score(Euryescapearay['Counts'], Eurypoly3equ(Euryescapearay['EscapeYear']))        #R^2 value
print(Eurypoly3r2)    

plt.plot(Euryescapearay['EscapeYear'], Eurypoly3equ(Euryescapearay['EscapeYear']), label ='3rd poly: {}'.format(round(Eurypoly3r2,3)), color = 'black', linewidth=linew)

plt.legend()
#plt.show()


#--noncumulative
#Graph
figno = figno+1
fig, ax = plt.subplots(num=figno)
plt.title('Eurybates family Escapes')
plt.xlabel('Time (Gyr)')
plt.ylabel('Escape perc.')
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1,))  #Y axis as percentiles from decimals

Euryncnum, Euryncbin, Euryncbar = plt.hist(Eurydata['EscapeTime'], cumulative=False, bins=BinNo, weights=np.zeros_like(Eurydata['EscapeTime']) + 1. / EuryNum, color='gray')  #histogram

Eurynccenters = 0.5*(Euryncbin[1:]+ Euryncbin[:-1])   #Center of bins

#plt.scatter(Eurycenters,Eurynum)

#make into array
Euryncescapearay = pd.DataFrame(data = {'EscapeYear': Eurynccenters, 'Counts': Euryncnum})

#Linear 
print('--Linear fit')
EuryncLincoef = np.polyfit(Euryncescapearay['EscapeYear'], Euryncescapearay['Counts'], 1)
print(EuryncLincoef)
EuryncLinequ = np.poly1d(EuryncLincoef)       #the Equation
print(EuryncLinequ)
EuryncLinequbin = EuryncLinequ * binsize
EuryncLinr2 = r2_score(Euryncescapearay['Counts'], EuryncLinequ(Euryncescapearay['EscapeYear']))        #R^2 value
print(EuryncLinr2)
plt.plot(Euryncescapearay['EscapeYear'], EuryncLinequ(Euryncescapearay['EscapeYear']),label = 'Linear:{}'.format(round(EuryncLinr2,2)), color = 'black', linewidth=linew)

#2nd order
print('--2nd order poly fit')
Eurync2ndcoef = np.polyfit(Euryncescapearay['EscapeYear'], Euryncescapearay['Counts'], 2)
print(Eurync2ndcoef)
Eurync2ndequ = np.poly1d(Eurync2ndcoef)       #the Equation
print(Eurync2ndequ)
Eurync2ndequbin = Eurync2ndequ * binsize
Eurync2ndr2 = r2_score(Euryncescapearay['Counts'], Eurync2ndequ(Euryncescapearay['EscapeYear']))        #R^2 value
print(Eurync2ndr2)
plt.plot(Euryncescapearay['EscapeYear'], Eurync2ndequ(Euryncescapearay['EscapeYear']),label = '2nd order poly:{}'.format(round(EuryncLinr2,2)), color = 'black', linestyle='dashed', linewidth=linew)



#Regression analysis.

#figno = figno+1
#plt.figure(figno)
#plt.title('Jovian Trojan Escapees')
#plt.xlabel('Time (Gyr)')
#plt.ylabel('EscapeRate')


#2d regression
print('--2d regression')
#poly2dregequ = np.polyint(Eurypoly2equ, k=Euryncescapearay['EscapeYear'].max())
Eurypoly2dregequ = np.polyder(Eurypoly2equ)
Eurypoly2dregequbin = Eurypoly2dregequ * binsize  #accounting for bin size 
print(Eurypoly2dregequ)
Eurypoly2dregequr2 = r2_score(Euryncescapearay['Counts'], Eurypoly2dregequbin(Euryncescapearay['EscapeYear']))    #R^2 value with bins
print(Eurypoly2dregequr2)
Euryescapearay['Poly2'] = Eurypoly2dregequ(Euryescapearay['EscapeYear'])

plt.plot(Euryescapearay['EscapeYear'], Eurypoly2dregequbin(Euryescapearay['EscapeYear']),label = 'Linear (2nd poly reg):{}'.format(round(Eurypoly2dregequr2,2)), color = 'black', linestyle='dashdot', linewidth=linew)

#plt.plot(Euryescapearay['EscapeYear'], poly2dregequ(Euryescapearay['EscapeYear']), label = '2nd order poly reg: {}'.format(round(poly2dregequr2,3)))


#3d regression
print('--3d regression')

Eurypoly3dregequ = np.polyder(Eurypoly3equ)
Eurypoly3dregequbin = Eurypoly3dregequ * binsize
print(Eurypoly3dregequ)
Euryescapearay['Poly3'] = Eurypoly3dregequ(Euryescapearay['EscapeYear'])

Eurypoly3dregequr2 = r2_score(Euryncescapearay['Counts'], Eurypoly3dregequbin(Euryncescapearay['EscapeYear']))    #R^2 value
print(Eurypoly3dregequr2)

plt.plot(Euryescapearay['EscapeYear'], Eurypoly3dregequbin(Euryescapearay['EscapeYear']), label = '2nd order (3rd poly reg):{}'.format(round(Eurypoly3dregequr2,2)), color = 'black', linestyle='dotted', linewidth=linew)
#print(Euryncescapearay)

#4d regression
plt.tight_layout()
plt.legend()
#plt.show()


#------------- Escape equations---------
figno = figno+1
plt.figure(figno)
plt.title('Jovian Trojan escape equations')
plt.xlabel('Time (Gyr)')
plt.ylabel('No. Escape')

escapearrayyear = np.linspace(-Euryescapearay['EscapeYear'].max(), Euryescapearay['EscapeYear'].max(), num=2*BinNo) #creating a linear set of numbers.

plt.plot(escapearrayyear, Eurypoly3dregequ(escapearrayyear), label = 'Both:{}'.format(round(Eurypoly3dregequr2,2)), color = 'black', linewidth=linew)


#plt.legend()
#plt.show()

#Some interesting things

EuryZeroescape =  np.roots(EuryncLinequ)       #point at which y=0
print('Roots (When y=0): ',EuryZeroescape)


#---integrals---

#L4 - just negative
#pastescapeEury = scipy.integrate.quad(Eurypoly3dregequ, -4.5e9, 0)
pastescapeEury = scipy.integrate.quad(EuryncLinequ, EuryZeroescape[0], 0)
print('Past escape number', pastescapeEury)
EuryTotalnum = len(EuryStable.index) + len(EuryEscape.index)
EuryOriginal = pastescapeEury[0] + EuryTotalnum
print('Eurybates Present Number: ', EuryTotalnum)
print('Eurybates Original Number: ', EuryOriginal)
#L4integ = -np.polyint(l4poly3dregequ) + len(L4AstdysAll.index) #bins
Euryinteg = -np.polyint(Eurypoly3dregequ) + EuryTotalnum
print(Euryinteg)


figno = figno+1
plt.figure(figno)
plt.title('Total numbers')
plt.xlabel('Time (Gyr)')
plt.ylabel('Total number')
#L4
plt.plot(escapearrayyear, Euryinteg(escapearrayyear), label = 'L4', color = 'black', linewidth=linew)

plt.show()