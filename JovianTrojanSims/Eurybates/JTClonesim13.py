#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 14:06:09 2018

---------Jovian Trojan Simulation--------

@author: Tim

This program runs the bulk work simulating individual objects using REBOUND. 
It simulates a Jupiter Trojan as a particle in the presence of the 4 giant planets and the sun.

Version Notes:
9 - Used to run the main 4.5e9 Trojans.
10 - Updated to inculde ex/ey and ix/iy for short run proper elements
Backwards - changed to reverse integration
11 - Updated to include vectors and backwards possibility.
12 - put in the proper day to year conversion
13 - fixing the time samples
"""


import rebound
import numpy as np
import pandas as pd
from datetime import datetime
import time
import sys
import math

#Dependancies
#4planets.bin

#----------inputs-----------
#loading from the master

#The simulation timestep. Calculated for Jupiter
#Timestep
#TimeStep = 0.3954									#The simulation timestep. Calculated for Jupiter

#number of outputs
#intTime = 4.5e9   								#integration Time in years Life of SS 4.5e9
#sampleTime = 1e7   						#Sampleing time in years



#-----Creating the command line rguments-----

#using Argparse as inputs
import argparse
parser = argparse.ArgumentParser(prefix_chars='@')
#Simulation inputs from master
parser.add_argument("TimeStep", help="Time Step (AU)", type=float) #name argument normally  
parser.add_argument("intTime", help="Integration Time (Years)", type=float) #length of the run
parser.add_argument("sampleTime", help="Sample time output (Years)", type=float) #name argument 2010LZ21 
parser.add_argument("clones", help="Number of clones", type=int) #name argument 2010LZ21 

# 
parser.add_argument("name", help="name") #name argument 2010LZ21 
parser.add_argument("vx", help="vx", type=float) #name argument 0.0051502437 
parser.add_argument("vx_s", help="vx_s", type=float) #name argument 1.85481982 
parser.add_argument("vy", help="vy", type=float) #name argument -0.008625115 
parser.add_argument("vy_s", help="vy_s", type=float) #name argument 1.41892673 
parser.add_argument("vz", help="vz", type=float) #name argument -4.55660589067072e-05 
parser.add_argument("vz_s", help="vz_s", type=float) #name argument 0.727192046 
parser.add_argument("x", help="x", type=float) #name argument -2.7473173925 
parser.add_argument("x_s", help="x_s", type=float) #name argument 570.206812 
parser.add_argument("y", help="y", type=float) #name argument -2.2151841235 
parser.add_argument("y_s", help="y_s", type=float) #name argument 955.5624050000001 
parser.add_argument("z", help="z", type=float) #name argument -1.0719581095 
parser.add_argument("z_s", help="z_s", type=float) #name argument  2.81271383


#---Generateed---
args = parser.parse_args()
TimeStep = args.TimeStep									#The simulation timestep. Calculated for Jupiter
#number of outputs
intTime = args.intTime 
sampleTime = args.sampleTime 

start = datetime.now()		#start time
DatetimeNow = time.strftime("%Y%m%d-%H%M%S")


#----------------------------
#Simulations
#Using a pregenerated file for orbits
sim = rebound.Simulation.from_file("4planets.bin")
year = 1 # One year in units where G=1


#forwards
sim.dt = TimeStep  #forwards
Noutputs = int(intTime//sampleTime)
timeline = np.arange(0.0,intTime, sampleTime) 		#Number of simulations

'''
#For backwards - comment out for forwards
sim.dt = -TimeStep 
intTime = -intTime   								#integration Time in years Life of SS 4.5e9 -if backwards
Noutputs = int((-intTime)//sampleTime)
time = np.linspace(0.,intTime, Noutputs) 		#Number of simulations
'''

#Jovian Trojans
sim.add(m=0,x=args.x,y=args.y,z=args.z,vx=args.vx*365.25,vy=args.vy*365.25,vz=args.vz*365.25)  # original particle[5]

#Clones
clones = args.clones            #magnitude of clones
clonenum = clones**3            #number of clones
clonenumlist = list(range(6, 6+clonenum))   #list of integers to be itterated over
   

#print(clonenumlist)

#---creating the clones----

#x
xmin = args.x - args.x_s
xmax = args.x + args.x_s
xclones = np.linspace(xmin, xmax, num = clones)
#y
ymin = args.y - args.y_s
ymax = args.y + args.y_s
yclones = np.linspace(ymin, ymax, num = clones)
#z
zmin = args.z - args.z_s
zmax = args.z + args.z_s
zclones = np.linspace(zmin, zmax, num = clones)

for x in xclones:
    for y in yclones:
        for z in zclones:
            sim.add(m=0,x=x,y=y,z=z,vx=args.vx*365.25,vy=args.vy*365.25,vz=args.vz*365.25) 

#Text Overview file
outputfile = 'JTSim-{}-{}-{}-clones'.format(args.name, intTime, clonenum)
#outputfile = '{}-Sim-{}-clones'.format(args.name, clonenum)
orig_stdout = sys.stdout
outputtext = outputfile+'-Sum.txt'
sys.stdout = open(outputtext, 'wt')
print("-----------{}-------------".format(args.name))
print("")
print("Run:{}".format(DatetimeNow))

print('Starting parameters')
print('Integration')
print("Timestep: {} years".format(sim.dt))
print("Integraion time: {} years".format(intTime))
print("Sample time: {} years".format(sampleTime))

print('Number of clones: ', clonenum)
print('X clone range: ', xclones)
print('Y clone range: ', yclones)
print('Z clone range: ', zclones)

print('Starting parameters')
sim.status()


#------Integration--------
print('Integration')

print("Timestep: {} years".format(sim.dt))
print("Integraion time: {} years".format(intTime))
print("Sample time: {} years".format(sampleTime))



#integration
'''
#sim.initSimulationArchive("{}.bin".format(outputfile), interval=sampleTime)		#Archive
'''

#sim.integrator = "ias15" # IAS15 is the default integrator, so we actually don't need this line
#sim.integrator = "whfast" #whfast is already in the start file. 
sim.move_to_com()        # We always move to the center of momentum frame before an integration

#----DBs---
JTorgdb = pd.DataFrame([], columns=['Time', 'a', 'e', 'i', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'Libration', 'jtx', 'jty', 'ex', 'ey', 'ix', 'iy'])
#creating a DB for each clone
JTclonedb = {x: pd.DataFrame([], columns=['Time', 'a', 'e', 'i', 'x', 'y', 'z', 'vx', 'vy', 'vz','Libration', 'jtx', 'jty']) for x in clonenumlist}



# This stores the data and integrates through each timestep
for i,t in enumerate(timeline):
	sim.integrate(t, exact_finish_time=0)
	#--for the original particle--
	#Amplitude of Libration
	AmpLibDeg = math.degrees(sim.particles[5].orbit.l) - math.degrees(sim.particles[1].orbit.l)        #Amplitude of libration  = Trojan - Jupiter
	AmpLib = AmpLibDeg % 360      #normalising to 360
	#with a static Jupiter
	Jang = -math.atan2(sim.particles[1].y, sim.particles[1].x)        #Angle of Jupiter
	jtx = sim.particles[5].x * math.cos(Jang) - sim.particles[5].y * math.sin(Jang)
	jty = sim.particles[5].x * math.sin(Jang) + sim.particles[5].y * math.cos(Jang)
	ex = sim.particles[5].orbit.e * np.cos(sim.particles[5].orbit.omega)
	ey = sim.particles[5].orbit.e * np.sin(sim.particles[5].orbit.omega)
	ix = sim.particles[5].orbit.inc * np.cos(sim.particles[5].orbit.Omega)
	iy = sim.particles[5].orbit.inc * np.sin(sim.particles[5].orbit.Omega)
	#update the pandas dataframe
	JovTrojanTS = pd.DataFrame([[(sim.t), (sim.particles[5].orbit.a), (sim.particles[5].orbit.e), (sim.particles[5].orbit.inc), (sim.particles[5].x), (sim.particles[5].y), (sim.particles[5].z), (sim.particles[5].vx), (sim.particles[5].vy), (sim.particles[5].vz), AmpLib, jtx, jty, ex, ey, ix, iy]], columns=['Time', 'a', 'e', 'i','x', 'y', 'z', 'vx', 'vy', 'vz','Libration', 'jtx', 'jty', 'ex', 'ey', 'ix', 'iy'])
	JTorgdb = JTorgdb.append(JovTrojanTS,ignore_index=True)

	#for each clone calculation in the dataframe
	for line in clonenumlist:
		partno = line                         #setting the particle clone number, to take into account for the planetsts. Remember starts at 0
		#Amplitude of Libration
		AmpLibDeg = math.degrees(sim.particles[partno].orbit.l) - math.degrees(sim.particles[1].orbit.l)        #Amplitude of libration  = Trojan - Jupiter
		AmpLib = AmpLibDeg % 360      #normalising to 360
		#with a static Jupiter
		jtx = sim.particles[partno].x * math.cos(Jang) - sim.particles[partno].y * math.sin(Jang)
		jty = sim.particles[partno].x * math.sin(Jang) + sim.particles[partno].y * math.cos(Jang)
		ex = sim.particles[partno].orbit.e * np.cos(sim.particles[partno].orbit.omega)
		ey = sim.particles[partno].orbit.e * np.sin(sim.particles[partno].orbit.omega)
		ix = sim.particles[partno].orbit.inc * np.cos(sim.particles[partno].orbit.Omega)
		iy = sim.particles[partno].orbit.inc * np.sin(sim.particles[partno].orbit.Omega)

		#update the pandas dataframe
		JovTrojanTS = pd.DataFrame([[(sim.t), (sim.particles[partno].orbit.a), (sim.particles[partno].orbit.e), (sim.particles[partno].orbit.inc), (sim.particles[partno].x), (sim.particles[partno].y), (sim.particles[partno].z),  (sim.particles[partno].vx), (sim.particles[partno].vy), (sim.particles[partno].vz), AmpLib, jtx, jty, ex, ey, ix, iy]], columns=['Time', 'a', 'e', 'i','x', 'y', 'z', 'vx', 'vy', 'vz','Libration', 'jtx', 'jty', 'ex', 'ey', 'ix', 'iy'])
		JTclonedb[line] = JTclonedb[line].append(JovTrojanTS,ignore_index=True)				


#-----Mean Database
JTCloneConcat = pd.concat(JTclonedb.values())
byrowindex = JTCloneConcat.groupby(JTCloneConcat.index)
JTMeandf = byrowindex.mean()
#outputfile
JTmeanoutfile = 'JTSim-{}-{}-mean.csv'.format(args.name, intTime)
JTMeandf.to_csv(JTmeanoutfile, index=False)
	

#------Data manipulation of each of the particles
#for the original particle
JTorgoutfile = 'JTSim-{}-{}-org.csv'.format(args.name, intTime)
JTorgdb.to_csv(JTorgoutfile, index=False)

print('-----statistics for {}-------'.format(args.name))    
print('Maximum SMA:')
print(JTorgdb.loc[JTorgdb['a'].idxmax()])
print('----')
print('Minimum SMA:')
print(JTorgdb.loc[JTorgdb['a'].idxmin()])
print('----')
meanLib = JTorgdb['Libration'].mean()
print('Mean Libration Angle: {} \u00b0'.format(meanLib))
print('----')
rangeLib = JTorgdb['Libration'].max() - JTorgdb['Libration'].min()
print('Libration angle range: {}'.format(rangeLib))
print('-----------------------------------------------------------')

#the clones
for JTname, JT in JTclonedb.items():
    #output to csv.
    clonename = 'clone-{}'.format(JTname-5)
    JTindioutfile = 'JTSim-{}-{}-{}.csv'.format(args.name, intTime, clonename)
    JT.to_csv(JTindioutfile, index=False)

    #-----Some statistics-------
    print('-----statistics for {}-------'.format(clonename))    
    print('Maximum SMA:')
    print(JT.loc[JT['a'].idxmax()])
    print('----')
    print('Minimum SMA:')
    print(JT.loc[JT['a'].idxmin()])
    print('----')
    meanLib = JT['Libration'].mean()
    print('Mean Libration Angle: {} \u00b0'.format(meanLib))
    print('----')
    rangeLib = JT['Libration'].max() - JT['Libration'].min()
    print('Libration angle range: {}'.format(rangeLib))
    print('-----------------------------------------------------------')

	
print('-----statistics for Mean-------')    
print('Maximum SMA:')
print(JTMeandf.loc[JTMeandf['a'].idxmax()])
print('----')
print('Minimum SMA:')
print(JTMeandf.loc[JTMeandf['a'].idxmin()])
print('----')
meanLib = JTMeandf['Libration'].mean()
print('Mean Libration Angle: {} \u00b0'.format(meanLib))
print('----')
rangeLib = JTMeandf['Libration'].max() - JTMeandf['Libration'].min()
print('Libration angle range: {}'.format(rangeLib))
print('-----------------------------------------------------------')	

#stop time
end = datetime.now()
print("Run Time:", end - start)	
#closing the textfile
sys.stdout.close()
sys.stdout=orig_stdout 

