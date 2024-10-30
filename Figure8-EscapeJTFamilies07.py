#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 10:24:54 2018

---------Sim Escape Data Analysis--------

@author: Tim

This program is to find family members among the escaped trojans. 

05  -split off the Eurybates family specific
06 - updated for 9 clones rather than mean
07 - accounting for clones

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


#Files
JTFamfile = 'JTFamiles.csv'
#JTFamfile = 'BrozFamilyDBupdatedastdys.csv'
#JTFile = 'JovTrojanEscapesDB-OrgescapeData-20190906-124940.csv'  #change clone number to 1
JTFile = 'JovTrojanEscapesDB-CloneescapeData-20200224-103656.csv' #change clone number to 9
#JTFile = 'JovTrojanEscapesDB-All9escapeData-20190906-124940.csv' #change clone number to 1
Alldata = pd.read_csv('/media/tim/Data/Trojan-Astdys-DataEnphems-20190828-134958.csv', low_memory=False)

#number of clones
clonenum=9

PropEle = pd.read_csv('ASTDy-Trojan.syn', delim_whitespace=True)

def percent(frac,whole):
    return round(frac / whole * 100, 2)

pd.set_option('display.max_rows', None)     #no truncation of pandas dataframes
pd.set_option('display.max_columns', None)    

#generating
DatetimeNow = time.strftime("%Y%m%d-%H%M%S")
JTEscapeData = pd.read_csv(JTFile, low_memory=False)
JTfamData = pd.read_csv(JTFamfile)

BinNo = 100
binsize = JTEscapeData.EscapeTime.max() / BinNo
print(binsize)

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

#L5
L5FamEleAll = FamEle[FamEle.L==5]                                                #all L5
L5AstdysStab = L5FamEleAll[~L5FamEleAll['Name'].isin(JTEscapeData['Name']) & L5FamEleAll.FAMILY_NAME.isna()]    #L5 stable non families
L5AstdysEsc = L5FamEleAll[L5FamEleAll['Name'].isin(JTEscapeData['Name']) & L5FamEleAll.FAMILY_NAME.isna()]      #L5 Escaped non families
L5Fam = justFamProp[justFamProp.L==5]                    #L5 family members
L5FamStab = L5Fam[~L5Fam['Name'].isin(JTEscapeData['Name'])]   #L5 stable family members
L5FamEscape = famEscape[famEscape.L==5]   #L5 Escaped family members

'''
L5FamEleAll = FamEle[FamEle.L==5]
L5AstdysStab = L5AstdysAll[~L5AstdysAll['Name'].isin(JTEscapeData['JT'])]
'''
FamVolfrac = famEscape['vol_km3'].sum()/(FamDataAll['vol_km3'].sum()*clonenum)
#checks
#print(('Prop Ele:', PropEle.shape))
print('Family with Prop Ele:', len(FamEle)*clonenum)
print('------')
print('Just Family with Prop Ele:', len(justFamProp)*clonenum)
print('------')
print('Fam. Members that escape:', len(famEscape))
print('------')
print('Vol fraction of Fam. Members that escape:', FamVolfrac)
print('------')
print('Escaped total: ', len(JTEscapeData))
print('L4 all: ', len(L4FamEleAll)*clonenum)
print('L4stable:', len(L4AstdysStab)*clonenum)
print('L4escaped:', len(L4AstdysEsc))
print('------')
print('L5 all: ', len(L5FamEleAll)*clonenum)
print('L5stable:', len(L5AstdysStab))
print('L5escaped:', len(L5AstdysEsc)*clonenum)
print('------')
#print(famEscape.dtypes)

#Plotsetups
linew = 3
#Plot paramaters

plt.rcParams.update({'font.size': 20})
plt.rcParams.update({'figure.autolayout': True})

cgrad = 'jet'  #Colormap for the gradients


#------------------------------------------L4 Scatter plots---------------------------
#-------------------a vs e---------------------
figno = figno+1
plt.figure(figno)
plt.title('L4 Trojan Families')
plt.xlabel('$\Delta a$ prop.')
plt.ylabel('e prop.')
#Stable Trojans 
L4jtaex = L4AstdysStab['da_prop']
L4jtaey = L4AstdysStab['e_prop']
plt.scatter(L4jtaex, L4jtaey, facecolor='none', edgecolor ='grey') #marker='.', c ='black'
#escaped Trojans
L4jtaeEscx = L4AstdysEsc['da_prop']
L4jtaeEscy = L4AstdysEsc['e_prop']
plt.scatter(L4jtaeEscx, L4jtaeEscy, marker='x', c='grey')

#---------families
#--Eurybates
EurybatesAll = FamDataAll[FamDataAll['FAMILY_NAME'] == ' 3548 Eurybates']
EurybateStable = L4FamStab[L4FamStab['FAMILY_NAME'] == ' 3548 Eurybates']
EurybateEscape = L4FamEscape[L4FamEscape['FAMILY_NAME'] == ' 3548 Eurybates']

#stable
L4jtFam1aex = EurybateStable['da_prop']
L4jtFam1aey = EurybateStable['e_prop']
plt.scatter(L4jtFam1aex, L4jtFam1aey, marker='$1$', c='black')

#Escaped
L4jtaeFam1Escx = EurybateEscape['da_prop']
L4jtaeFam1Escy = EurybateEscape['e_prop']
plt.scatter(L4jtaeFam1Escx, L4jtaeFam1Escy, marker='$1$', c=EurybateEscape['EscapeTime'], cmap=cgrad)

print(' 3548 Eurybates family')
print('Total number: ', len(EurybatesAll)*clonenum)
print('Total Volume: ', EurybatesAll['vol_km3'].sum()*clonenum)
print('Escaped: ', len(EurybateEscape))
print('Escape fraction: ', len(EurybateEscape)/(len(EurybatesAll)*clonenum))
print('Escape fraction (Volume): ', EurybateEscape['vol_km3'].sum()/(EurybatesAll['vol_km3'].sum()*clonenum))
print('------')

#cbar = plt.colorbar()
#cbar.set_label('Escape time (yrs)', rotation=270, labelpad=15)

#Hektor
HektorAll = FamDataAll[FamDataAll['FAMILY_NAME'] == ' 624 Hector']
HektorStable = L4FamStab[L4FamStab['FAMILY_NAME'] == ' 624 Hector']
HektorEscape = L4FamEscape[L4FamEscape['FAMILY_NAME'] == ' 624 Hector']
#stable
L4jtFam1aex = HektorStable['da_prop']
L4jtFam1aey = HektorStable['e_prop']
plt.scatter(L4jtFam1aex, L4jtFam1aey, marker='$2$', c='black')

#Escaped
L4jtaeFam1Escx = HektorEscape['da_prop']
L4jtaeFam1Escy = HektorEscape['e_prop']
plt.scatter(L4jtaeFam1Escx, L4jtaeFam1Escy, marker='$2$', c=HektorEscape['EscapeTime'], cmap=cgrad)

print(' 624 Hector family')
print('Total number: ', len(HektorAll)*clonenum)
print('Total Volume: ', HektorAll['vol_km3'].sum()*clonenum)
print('Escaped: ', len(HektorEscape))
print('Escape fraction: ', len(HektorEscape)/(len(HektorAll)*clonenum))
print('Escape fraction (Volume): ', HektorEscape['vol_km3'].sum()/(HektorAll['vol_km3'].sum()*clonenum))
print('------')

#1996 RJ
f1996RJAll = FamDataAll[FamDataAll['FAMILY_NAME'] == ' 9799 1996 RJ']
f1996RJStable = L4FamStab[L4FamStab['FAMILY_NAME'] == ' 9799 1996 RJ']
f1996RJEscape = L4FamEscape[L4FamEscape['FAMILY_NAME'] == ' 9799 1996 RJ']
#stable
L4jtFam1aex = f1996RJStable['da_prop']
L4jtFam1aey = f1996RJStable['e_prop']
plt.scatter(L4jtFam1aex, L4jtFam1aey, marker='$3$', c='black')

#Escaped
L4jtaeFam1Escx = f1996RJEscape['da_prop']
L4jtaeFam1Escy = f1996RJEscape['e_prop']
plt.scatter(L4jtaeFam1Escx, L4jtaeFam1Escy, marker='$3$', c=f1996RJEscape['EscapeTime'], cmap=cgrad)

print(' 9799 1996RJ family')
print('Total number: ', len(f1996RJAll)*clonenum)
print('Total Volume: ', f1996RJAll['vol_km3'].sum()*clonenum)
print('Escaped: ', len(f1996RJEscape))
print('Escape fraction: ', len(f1996RJEscape)/(len(f1996RJAll)*clonenum))
print('Escape fraction (Volume): ', f1996RJEscape['vol_km3'].sum()/(f1996RJAll['vol_km3'].sum()*clonenum))
#print(f1996RJEscape[['full_name','JT_Clone','radius_km']])
print('------')


#Arkesilaos
ArkesilaosAll = FamDataAll[FamDataAll['FAMILY_NAME'] == ' 20961 Arkesilaos']
ArkesilaosStable = L4FamStab[L4FamStab['FAMILY_NAME'] == ' 20961 Arkesilaos']
ArkesilaosEscape = L4FamEscape[L4FamEscape['FAMILY_NAME'] == ' 20961 Arkesilaos']
#stable
L4jtFam1aex = ArkesilaosStable['da_prop']
L4jtFam1aey = ArkesilaosStable['e_prop']
plt.scatter(L4jtFam1aex, L4jtFam1aey, marker='$4$', c='black')

#Escaped
L4jtaeFam1Escx = ArkesilaosEscape['da_prop']
L4jtaeFam1Escy = ArkesilaosEscape['e_prop']
plt.scatter(L4jtaeFam1Escx, L4jtaeFam1Escy, marker='$4$', c=ArkesilaosEscape['EscapeTime'], cmap=cgrad)

print(' 20961 Arkesilaos family')
print('Total number: ', len(ArkesilaosAll)*clonenum)
print('Total Volume: ', ArkesilaosAll['vol_km3'].sum()*clonenum)
print('Escaped: ', len(ArkesilaosEscape))
print('Escape fraction: ', len(ArkesilaosEscape)/(len(ArkesilaosAll)*clonenum))
print('Escape fraction (Volume): ', ArkesilaosEscape['vol_km3'].sum()/(ArkesilaosAll['vol_km3'].sum()*clonenum))
print(ArkesilaosEscape[['full_name','JT_Clone','radius_km']])
print('------')

'''
#-Stable families
L4jtFamaex = L4FamStab['da_prop']
L4jtFamaey = L4FamStab['e_prop']
plt.scatter(L4jtFamaex, L4jtFamaey, marker='$1$', c ='red')
#Escape Families

L4jtaeFamEscx = L4FamEscape['da_prop']
L4jtaeFamEscy = L4FamEscape['e_prop']
plt.scatter(L4jtaeFamEscx, L4jtaeFamEscy, marker='$1$', c=L4FamEscape['EscapeTime'], cmap=cgrad)
'''
plt.savefig('L4FamEscapesAE.png',bbox_inches='tight')
plt.show()

#-------------------a vs i---------------------
figno = figno+1
plt.figure(figno)
plt.title('L4 Trojan Families')
plt.xlabel('$\Delta a$ prop.')
plt.ylabel('sinI prop.')
#Stable Trojans 
L4jtaex = L4AstdysStab['da_prop']
L4jtaey = L4AstdysStab['sinI_prop']
plt.scatter(L4jtaex, L4jtaey, facecolor='none', edgecolor ='grey') #marker='.', c ='black'
#escaped Trojans
L4jtaeEscx = L4AstdysEsc['da_prop']
L4jtaeEscy = L4AstdysEsc['sinI_prop']
plt.scatter(L4jtaeEscx, L4jtaeEscy, marker='x', c='grey')

#---------families
#--Eurybates
#stable
L4jtFam1aex = L4FamStab.da_prop[L4FamStab['FAMILY_NAME'] == ' 3548 Eurybates']
L4jtFam1aey = L4FamStab.sinI_prop[L4FamStab['FAMILY_NAME'] == ' 3548 Eurybates']
plt.scatter(L4jtFam1aex, L4jtFam1aey, marker='$1$', c='black')
#Escaped
L4jtaeFam1Escx = L4FamEscape.da_prop[L4FamEscape['FAMILY_NAME'] == ' 3548 Eurybates']
L4jtaeFam1Escy = L4FamEscape.sinI_prop[L4FamEscape['FAMILY_NAME'] == ' 3548 Eurybates']
plt.scatter(L4jtaeFam1Escx, L4jtaeFam1Escy, marker='$1$', c=L4FamEscape.EscapeTime[L4FamEscape['FAMILY_NAME'] == ' 3548 Eurybates'], cmap=cgrad)


#cbar = plt.colorbar()
#cbar.set_label('Escape time (yrs)', rotation=270, labelpad=15)

#Hektor
#stable
L4jtFam2aex = L4FamStab.da_prop[L4FamStab['FAMILY_NAME'] == ' 624 Hector']
L4jtFam2aey = L4FamStab.sinI_prop[L4FamStab['FAMILY_NAME'] == ' 624 Hector']
plt.scatter(L4jtFam2aex, L4jtFam2aey, marker='$2$', c='black')
#Escaped
L4jtaeFam2Escx = L4FamEscape.da_prop[L4FamEscape['FAMILY_NAME'] == ' 624 Hector']
L4jtaeFam2Escy = L4FamEscape.sinI_prop[L4FamEscape['FAMILY_NAME'] == ' 624 Hector']
plt.scatter(L4jtaeFam2Escx, L4jtaeFam2Escy, marker='$2$', c=L4FamEscape.EscapeTime[L4FamEscape['FAMILY_NAME'] == ' 624 Hector'], cmap=cgrad)

#1996 RJ
#stable
L4jtFam3aex = L4FamStab.da_prop[L4FamStab['FAMILY_NAME'] == ' 9799 1996 RJ']
L4jtFam3aey = L4FamStab.sinI_prop[L4FamStab['FAMILY_NAME'] == ' 9799 1996 RJ']
plt.scatter(L4jtFam3aex, L4jtFam3aey, marker='$3$', c='black')
#Escaped
L4jtaeFam3Escx = L4FamEscape.da_prop[L4FamEscape['FAMILY_NAME'] == ' 9799 1996 RJ']
L4jtaeFam3Escy = L4FamEscape.sinI_prop[L4FamEscape['FAMILY_NAME'] == ' 9799 1996 RJ']
plt.scatter(L4jtaeFam3Escx, L4jtaeFam3Escy, marker='$3$', c=L4FamEscape.EscapeTime[L4FamEscape['FAMILY_NAME'] == ' 9799 1996 RJ'], cmap=cgrad)

#Arkesilaos
#stable
L4jtFam4aex = L4FamStab.da_prop[L4FamStab['FAMILY_NAME'] == ' 20961 Arkesilaos']
L4jtFam4aey = L4FamStab.sinI_prop[L4FamStab['FAMILY_NAME'] == ' 20961 Arkesilaos']
plt.scatter(L4jtFam4aex, L4jtFam4aey, marker='$4$', c='black')
#Escaped
L4jtaeFam4Escx = L4FamEscape.da_prop[L4FamEscape['FAMILY_NAME'] == ' 20961 Arkesilaos']
L4jtaeFam4Escy = L4FamEscape.sinI_prop[L4FamEscape['FAMILY_NAME'] == ' 20961 Arkesilaos']
plt.scatter(L4jtaeFam4Escx, L4jtaeFam4Escy, marker='$4$', c=L4FamEscape.EscapeTime[L4FamEscape['FAMILY_NAME'] == ' 20961 Arkesilaos'], cmap=cgrad)

plt.savefig('L4FamEscapesAI.png',bbox_inches='tight')
plt.show()





#------------------------------------------L5 Scatter plots---------------------------
#-------------------a vs e---------------------
figno = figno+1
plt.figure(figno)
plt.title('L5 Trojan Families')
plt.xlabel('$\Delta a$ prop.')
plt.ylabel('e prop.')
#Stable Trojans 
L5jtaex = L5AstdysStab['da_prop']
L5jtaey = L5AstdysStab['e_prop']
plt.scatter(L5jtaex, L5jtaey, facecolor='none', edgecolor ='grey') #marker='.', c ='black'
#escaped Trojans
L5jtaeEscx = L5AstdysEsc['da_prop']
L5jtaeEscy = L5AstdysEsc['e_prop']
plt.scatter(L5jtaeEscx, L5jtaeEscy, marker='x', c='grey')

#---------families
#-- 4709 Ennomos
EnnomosAll = FamDataAll[FamDataAll['FAMILY_NAME'] == ' 4709 Ennomos']
EnnomosStable = L5FamStab[L5FamStab['FAMILY_NAME'] == ' 4709 Ennomos']
EnnomosEscape = L5FamEscape[L5FamEscape['FAMILY_NAME'] == ' 4709 Ennomos']
#stable
L5jtFam1aex = EnnomosStable['da_prop']
L5jtFam1aey = EnnomosStable['e_prop']
plt.scatter(L5jtFam1aex, L5jtFam1aey, marker='$1$', c='black')

#Escaped
L5jtaeFam1Escx = EnnomosEscape['da_prop']
L5jtaeFam1Escy = EnnomosEscape['e_prop']
plt.scatter(L5jtaeFam1Escx, L5jtaeFam1Escy, marker='$5$', c=EnnomosEscape['EscapeTime'], cmap=cgrad)

print(' 20961 Ennomos family')
print('Total number: ', len(EnnomosAll)*clonenum)
print('Total Volume: ', EnnomosAll['vol_km3'].sum()*clonenum)
print('Escaped: ', len(EnnomosEscape))
print('Escape fraction: ', len(EnnomosEscape)/(len(EnnomosAll)*clonenum))
print('Escape fraction (Volume): ', EnnomosEscape['vol_km3'].sum()/(EnnomosAll['vol_km3'].sum()*clonenum))
#print(EnnomosEscape[['full_name','JT_Clone','radius_km']])
print('------')

#cbar = plt.colorbar()
#cbar.set_label('Escape time (yrs)', rotation=270, labelpad=15)

#247341 2001 UV209
f2001UV209All = FamDataAll[FamDataAll['FAMILY_NAME'] == ' 247341 2001 UV209']
f2001UV209Stable = L5FamStab[L5FamStab['FAMILY_NAME'] == ' 247341 2001 UV209']
f2001UV209Escape = L5FamEscape[L5FamEscape['FAMILY_NAME'] == ' 247341 2001 UV209']
#stable
L4jtFam1aex = f2001UV209Stable['da_prop']
L4jtFam1aey = f2001UV209Stable['e_prop']
plt.scatter(L5jtFam1aex, L5jtFam1aey, marker='$6$', c='black')

#Escaped
L5jtaeFam1Escx = f2001UV209Escape['da_prop']
L5jtaeFam1Escy = f2001UV209Escape['e_prop']
plt.scatter(L5jtaeFam1Escx, L5jtaeFam1Escy, marker='$1$', c=f2001UV209Escape['EscapeTime'], cmap=cgrad)

print('  247341 2001 UV209 family')
print('Total number: ', len(f2001UV209All)*clonenum)
print('Total Volume: ', f2001UV209All['vol_km3'].sum()*clonenum)
print('Escaped: ', len(f2001UV209Escape))
print('Escape fraction: ', len(f2001UV209Escape)/(len(f2001UV209All)*clonenum))
print('Escape fraction (Volume): ', f2001UV209Escape['vol_km3'].sum()/(f2001UV209All['vol_km3'].sum()*clonenum))
print(f2001UV209Escape[['full_name','JT_Clone','radius_km']])
print('------')


'''
#-Stable families
L5jtFamaex = L5FamStab['da_prop']
L5jtFamaey = L5FamStab['e_prop']
plt.scatter(L5jtFamaex, L5jtFamaey, marker='$1$', c ='red')
#Escape Families

L5jtaeFamEscx = L5FamEscape['da_prop']
L5jtaeFamEscy = L5FamEscape['e_prop']
plt.scatter(L5jtaeFamEscx, L5jtaeFamEscy, marker='$1$', c=L5FamEscape['EscapeTime'], cmap=cgrad)
'''
plt.savefig('L5FamEscapesAE.png',bbox_inches='tight')
plt.show()

#-------------------a vs i---------------------
figno = figno+1
plt.figure(figno)
plt.title('L5 Trojan Families')
plt.xlabel('$\Delta a$ prop.')
plt.ylabel('sinI prop.')
#Stable Trojans 
L5jtaex = L5AstdysStab['da_prop']
L5jtaey = L5AstdysStab['sinI_prop']
plt.scatter(L5jtaex, L5jtaey, facecolor='none', edgecolor ='grey') #marker='.', c ='black'
#escaped Trojans
L5jtaeEscx = L5AstdysEsc['da_prop']
L5jtaeEscy = L5AstdysEsc['sinI_prop']
plt.scatter(L5jtaeEscx, L5jtaeEscy, marker='x', c='grey')

#---------families
#--Eurybates
#stable
L5jtFam1aex = L5FamStab.da_prop[L5FamStab['FAMILY_NAME'] == ' 4709 Ennomos']
L5jtFam1aey = L5FamStab.sinI_prop[L5FamStab['FAMILY_NAME'] == ' 4709 Ennomos']
plt.scatter(L5jtFam1aex, L5jtFam1aey, marker='$5$', c='black')
#Escaped
L5jtaeFam1Escx = L5FamEscape.da_prop[L5FamEscape['FAMILY_NAME'] == ' 4709 Ennomos']
L5jtaeFam1Escy = L5FamEscape.sinI_prop[L5FamEscape['FAMILY_NAME'] == ' 4709 Ennomos']
plt.scatter(L5jtaeFam1Escx, L5jtaeFam1Escy, marker='$5$', c=L5FamEscape.EscapeTime[L5FamEscape['FAMILY_NAME'] == ' 4709 Ennomos'], cmap=cgrad)

#cbar = plt.colorbar()
#cbar.set_label('Escape time (yrs)', rotation=270, labelpad=15)

#Hektor
#stable
L5jtFam2aex = L5FamStab.da_prop[L5FamStab['FAMILY_NAME'] == ' 247341 2001 UV209']
L5jtFam2aey = L5FamStab.sinI_prop[L5FamStab['FAMILY_NAME'] == ' 247341 2001 UV209']
plt.scatter(L5jtFam2aex, L5jtFam2aey, marker='$6$', c='black')
#Escaped
L5jtaeFam2Escx = L5FamEscape.da_prop[L5FamEscape['FAMILY_NAME'] == ' 247341 2001 UV209']
L5jtaeFam2Escy = L5FamEscape.sinI_prop[L5FamEscape['FAMILY_NAME'] == ' 247341 2001 UV209']
plt.scatter(L5jtaeFam2Escx, L5jtaeFam2Escy, marker='$6$', c=L5FamEscape.EscapeTime[L5FamEscape['FAMILY_NAME'] == ' 247341 2001 UV209'], cmap=cgrad)

plt.savefig('L5FamEscapesAI.png',bbox_inches='tight')
plt.show()

