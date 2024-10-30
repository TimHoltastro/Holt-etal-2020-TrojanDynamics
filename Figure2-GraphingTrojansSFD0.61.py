# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:20:53 2017

---------Graphing Trojan Data--------

@author: Tim


The purpose of this program is to visualise several parts of the Jovian Trojan data.

The data comes from the Small Solar system Body Database.
03 - update to new Trojan DB. Include SFD
04 - USing SFD to add in Fraction above 
05 - Correcting for probability in Paramater space volume - split to focus on SFD
0.61 - Updated for new analysis and larger font size. There is also some volume calculations. Added in the SF distribution curve from David
0.62 - removing all the subset information - as that was forked
"""

import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import math
import sys
import datetime
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import pickle
import matplotlib.ticker as ticker
import matplotlib
matplotlib.rcParams.update({'font.size': 30})


"""
Bringing in the data
"""

AllData = pd.read_csv('/media/tim/Data/Trojan-Astdys-DataEnphems-20190819-150408.csv', low_memory=False)

Cladfamsname = 'Trojan-Family-DispersalVelocity-20200220-115053-Sum'
CladFams = pd.read_csv('/home/tim/Google Drive/AstroWIP/PhD/Programs/JTCladisticsDispersalVelocities/{}.csv'.format(Cladfamsname), low_memory=False)



#Selecting for L4 and L5

#L4
AllDatal4 = AllData.loc[AllData.L == 4]
print('Alldata L4:', len(AllDatal4.index))



#L5
AllDatal5 = AllData.loc[AllData.L == 5]
print('Alldata L5:', len(AllDatal5.index))

figno=0

#Volume of the swarms in AEI space
l4diffa = np.ptp(AllDatal4['da(AU)'])
l4diffe = np.ptp(AllDatal4['e_astdys'])
l4diffi = np.ptp(AllDatal4['sinI'])
l4Vol = 0.5 * l4diffa * l4diffe * l4diffi
print('L4 V_Par: ', l4Vol)

l5diffa = np.ptp(AllDatal5['da(AU)'])
l5diffe = np.ptp(AllDatal5['e_astdys'])
l5diffi = np.ptp(AllDatal5['sinI'])
l5Vol = 0.5 * l5diffa * l5diffe * l5diffi
print('L5 V_Par: ', l5Vol)




"""
----------------Plots-------
"""
"""
#Size distribution
Size = AllData['diameter']

figno = figno+1
plt.figure(figno) 
#plt.grid()
plt.hist(Size[~np.isnan(Size)], cumulative=False, bins=30, log=True)
#plt.annotate((data['a'], data['e']), data['Satellite'])
plt.title('Jovian Trojan Size distribution')
plt.xlabel('Diameter (km)')
#plt.ylabel('Log cumulative no.')
#saveae = family+'.ae.pdf'
#plt.savefig(saveae)
plt.show()
"""


figno = figno+1
fig, ax = plt.subplots(figno)
#plt.grid()
plt.yscale('log')
plt.xscale('log')

'''
#Selecting only those greater than 10km
greaterthan = AllData[AllData['diameter']>15]
sorted_greaterthan = np.sort(greaterthan['diameter'])
plt.step(sorted_greaterthan[::-1], np.arange(sorted_greaterthan.size))
'''
#all sets
sorted_all = np.sort(AllData['diameter'])
sorted_L4 = np.sort(AllDatal4['diameter'])
sorted_L5 = np.sort(AllDatal5['diameter'])



#plt.step(sorted_all[::-1], np.arange(sorted_all.size))
binsize = 1000
#, density=True    for fraction
alln, allbins, allpatchs = plt.hist(AllData['diameter'],binsize, histtype='step', cumulative=-1, label='All', linestyle = '-', color = 'black', linewidth=1.5) 
allpatchs[0].set_xy(allpatchs[0].get_xy()[1:-1])
allbinsCenter = 0.5*(alln[1:]+ alln[:-1])   #Center of bins

L4n, L4bins, L4patchs = plt.hist(AllDatal4['diameter'],binsize, histtype='step', cumulative=-1, label='L4', linestyle = '--', color = 'black', linewidth=1.5) 
L4patchs[0].set_xy(L4patchs[0].get_xy()[1:-1])
L4lbinsCenter = 0.5*(L4bins[1:]+ L4bins[:-1])   #Center of bins

L5n, L5bins, L5patchs = plt.hist(AllDatal5['diameter'],binsize, histtype='step', cumulative=-1, label='L5', linestyle = ':', color = 'black', linewidth=1.5) 
L5patchs[0].set_xy(L5patchs[0].get_xy()[1:-1])
L5binsCenter = 0.5*(L5bins[1:]+ L5bins[:-1])   #Center of bins

plt.axvline(x=10, color = 'lightgray', linewidth=1, linestyle='dashed')

ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))


#SDF estimation from David N
#An estimation equation for the SDF from Davin N. 2018 review paper
#D = np.arange(AllData['diameter'].min(),AllData['diameter'].max(), 1)
D = np.arange(AllData['diameter'].min(),100, 1)
print(D)
NgtD = 25*(D/100)**-2.1          
plt.plot(D, NgtD, color= 'red', label = 'SFD estimation')
#the 'kink'
dd=np.arange(100,AllData['diameter'].max(), 1)
NgtD2 = 25*(dd/100)**-5 
plt.plot(dd, NgtD2, color= 'red')


#plt.annotate((data['a'], data['e']), data['Satellite'])
#plt.title('Jovian Trojan Size distribution')
plt.xlabel('D(km)')
plt.ylabel('N(>D)')
#plt.xlim(left=5)
#saveae = family+'.ae.pdf'
#plt.savefig(saveae)

plt.legend(loc='lower left')
plt.show()



















