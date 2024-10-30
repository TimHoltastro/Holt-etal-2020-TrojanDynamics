#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:37:08 2018

Graphing Trojans


@author: tim
"""



import numpy as np
import pandas as pd
from datetime import datetime
import time
import sys
import subprocess
import glob
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from cycler import cycler

#parameters
psize = 0.5        #size of plot points
#limits
innerlimit = 0
limit = 3.5

#black style
plt.style.use('dark_background')
#plt.style.use('seaborn-colorblind')

plt.rcParams.update({'font.size': 22})

#Trojans
TJData = pd.read_csv('/home/tim/Google Drive/AstroWIP/PhD/Programs/JTMasterSim/HorizonsMatrix/SBDB20180417.7206.csv', low_memory=False)

#---Selecting some of the subgroups
#hildasselect = 
hildas = AsteroidsData[(AsteroidsData['a']>3.8) & (AsteroidsData['a']<4.1) ]
#trojans = AsteroidsData[AsteroidsData['pdes'].isin(TJData['pdes'])]
NEO = AsteroidsData[AsteroidsData['pdes'].isin(NEOData['pdes'])]
FamilyMembers = AsteroidsData[AsteroidsData['pdes'].isin(familiesDB['AST_NUMBER'])]

print('No: families', familiesDB.shape)
print('DB to families',FamilyMembers.shape)

'''
print(AsteroidsData['pdes'].dtype)
print(familiesDB['AST_NUMBER'].dtype)
print(FamilyMembers.shape)
'''



#------A vs I ------------

fig=plt.figure()

#Setup
#plt.title('Solar System')
plt.xlabel('Semi-major axis (au)')
plt.ylabel('Inc(Deg.).')
plt.xlim(left=innerlimit)
plt.xlim(right=limit)         #For outer
#plt.xlim(right=3.5)             #for inner
#plt.xlim(right=1000)
plt.ylim(top=50)


#trojans
trojans = AsteroidsData[AsteroidsData['class']=='TJN']
TJx = trojans['a']
TJy = trojans['i']

plt.scatter(TJx, TJy, marker='.', color = TrojanColor, s=psize, label = 'Trojans') 

#----planets----
planetx = planets['a']
planety = planets['I']
plt.scatter(planetx, planety, marker='.', color = PlanetColor, s=100, label = 'Planet') 
'''
for index, i in planets.iterrows():
    plt.annotate(s=i['Planet'], xy=(i['a'], i['I']))
'''

#sun
plt.scatter(0,0, marker='.', color='yellow')

#plt.legend()

plt.show()


#----------A vs E --------------------------------------

fig=plt.figure()

#Setup
#plt.title('Solar System')
plt.xlabel('Semi-major axis (au)')
plt.ylabel('Ecc.')
#plt.xlim(left=innerlimit)
plt.xlim(right=limit)         #For outer
#plt.ylim(bottom=0)
#plt.xlim(right=3.5)             #for inner
#plt.xlim(right=1000)
plt.ylim(top=0.60)


#trojans

TJy = trojans['e']

plt.scatter(TJx, TJy, marker='.', color = TrojanColor, s=psize, label = 'Trojans') 

#----planets----

planety = planets['e']
plt.scatter(planetx, planety, marker='.', color = PlanetColor, s=100, label = 'Planet') 
'''
for index, i in planets.iterrows():
    plt.annotate(s=i['Planet'], xy=(i['a'], i['I']))
'''

#sun
plt.scatter(0,0, marker='.', color='yellow')



#plt.legend()


plt.show()

#--------------------------------XY------------------------------------

#fig=plt.figure(facecolor='black')
#fig=plt.figure(dpi=600)
fig=plt.figure(1)

axes.set_xlim([-limit,limit])
axes.set_ylim([-limit,limit])
axes.set_aspect('equal')

#plt.title('Inner Solar system')
plt.xlabel('au')
plt.ylabel('au')

#trojans
TJx = trojans['x']
TJy = trojans['y']

plt.scatter(TJx, TJy, marker='.', color = TrojanColor, s=psize, label = 'Trojans') 

#-------=Sun and Planets--------=

#sun
plt.scatter(0,0, marker='.', color='yellow')

#planets
planets = pd.read_csv('/home/tim/Google Drive/AstroWIP/PhD/Programs/JTMasterSim/SSEnphemerates2000101.csv')

Jang = -math.atan2(planets.loc[4,'Y'], planets.loc[4,'X']) # angle offset for Jupiter
#print(Jang)
px = planets['X']
py = planets['Y']
#px = planets['X'] * math.cos(Jang) - planets['Y'] * math.sin(Jang)
#py = planets['X'] * math.sin(Jang) + planets['Y'] * math.cos(Jang)


plt.scatter(px, py, marker='.', color = PlanetColor, s=100, label = 'planet') 
#orbits
planets['a'] = (px**2 + py**2)**0.5  #Semi-major axis
for index, row in planets.iterrows():
    orbits = plt.Circle((0,0), radius=row['a'], fill=False)
    ax = fig.add_subplot(1, 1, 1)
    ax.add_patch(orbits)



#plt.legend(loc='lower right')
plt.show()


#--------------------------------YZ-----------------------------------

fig=plt.figure(2)
#fig=plt.figure(dpi=600)

axes = plt.gca()
axes.set_xlim([-limit,limit])
axes.set_ylim([-limit,limit])
axes.set_aspect('equal')

plt.xlabel('au')
plt.ylabel('au')

#trojans
TJz = trojans['z']
plt.scatter(TJx, TJz, marker='.', color = TrojanColor, s=psize, label = 'Trojans') 

#-------=Sun and Planets--------=

#sun
plt.scatter(0,0, marker='.', color='yellow')

#pzy = planets['Y']
#py = planets['X'] * math.sin(Jang) + planets['Y'] * math.cos(Jang)
pzz = planets['Z']

plt.scatter(py, pzz, marker='.', color = PlanetColor, s=100, label = None) 

#Neptune orbit
npy = planets.loc[7,'Y']
npz = planets.loc[7,'Z']


npx1, npy1 = [-npy, 0], [0, 0]
npx2, npy2 = [npy, 0], [0, 0]
#print(planets.loc[4,'Y'])
plt.plot(npx1, npy1,npx2, npy2, color='black')


#plt.legend()
plt.show()