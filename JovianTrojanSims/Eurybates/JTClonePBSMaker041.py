#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 14:44:25 2018

---------Jovian Trojan Master--------

@author: Tim

This program is to loop though a list of enhemerates from the Jupiter trojans. It creates pbs files and submits them to the server.

"""


import numpy as np
import pandas as pd
import time
import sys
import os
import glob


#----------inputs-----------

#for the simulation
TimeStep = 0.3954                                    #The simulation timestep. Calculated for Jupiter

#number of outputs
intTime = 4.5e9                                  #integration Time in years Life of SS 4.5e9
sampleTime = 1e5
Clones = 2                             #Magnitude of clones eg, 4 = 4**3 =  64 clones, , 


#the matrix to loop though
Enferm = pd.read_csv('EurybatesEnphems-20190723-151820.csv')

#Pbs variables
cpus = len(Enferm.index)              #Number of CPUs to split it onto use len(Enferm.index) for all at once
Walltimehrs = 47       #the max number of hours

#---Generated-----

Enferm = Enferm.drop(columns=['date']) #dropping the times

clonenum = Clones**3

orig_stdout = sys.stdout
cwd = os.getcwd()               #current working directory

#-----------Creating the pbs files-------------
count=0
for g, df in Enferm.groupby(np.arange(len(Enferm)) // cpus):
    count = count+1
    outputfile = 'JTSim-{}-{}-clones-{}'.format(intTime, clonenum, count)

    
    #looping though each of the JTs - Creating a list.
    listfile = outputfile+'.list'
    sys.stdout = open(listfile, 'wt')
    for index, line in df.iterrows():
        linestring = line.tolist() #Converting to list
        linestring = ' '.join(str(e) for e in linestring) #joingin the list to a string
        linecommand = '{} {} {} {} {}'.format(TimeStep, intTime, sampleTime, Clones, linestring)
        print(linecommand)
    sys.stdout.close()
    
    #-The PDS files
    DatetimeNow = time.strftime("%Y%m%d-%H%M%S")
    pdsfile = outputfile+'.pbs'
    sys.stdout = open(pdsfile, 'wt')  
    
    #Writing the PBS script variables
    print('#!/bin/bash -l')
    print('#')
    print('## Created: {}'.format(DatetimeNow))
    print('#PBS -N JTsim-{}'.format(count))
    print('#PBS -q default')
    print('#PBS -l walltime={}:00:00'.format(Walltimehrs))
    print('#PBS -l select=1:ncpus=1:mem=8gb')
    #print('#PBS –l place=pack')                    #this put the jobs on similar nodes if possilbe. 
    print('#PBS -M timothy.holt@usq.edu.au')
    print('#PBS -m a')                      #mail if a - the job aborts b - the job begins e - the job ends
    print('')
    print('#PBS -P 0201-TRHOLT')                        #project code
    print('')  
    print('#PBS -V')                            # get system variables
    print('')
    print('#PBS -j oe')                         #merge output and error files. 
    print('')   
    print('#PBS -J 1-{}'.format(len(df)))           #The Job array 
    print('')
    print('cd {}'.format(cwd))                  # change to working directory  
    print('')
    print('### Specify the executable and modules')  
    print('')
    print('module load python/3.5.1-gnu')       #loading the python module
    print('')
    print('## Jovian Trojans')  
    print('')    
    print('parameters=`sed -n \"${{PBS_ARRAY_INDEX}} p\" {}.list`'.format(outputfile))  
    print('')
    print('python JTClonesim*.py ${parameters}')       

       
    #closing the textfile
    sys.stdout.close()
    sys.stdout=orig_stdout 
  
 
#------Creating a Submission file.     
#list of the pbs files
pbslist = sorted(glob.glob('JTSim*.pbs'))
#listlength = len(pbslist)

#The Start file. 
#startfile = 'Start-JTSim-{}-{}-clones.txt'.format(intTime, clonenum)
startfile = 'start.sh'.format(intTime, clonenum)
sys.stdout = open(startfile, 'wt') 

count =0
#print('#!/bin/bash')
for f in pbslist:
    count=count+1
    if count == 1:
        linecommand = 'sim1=$(qsub -h {})'.format(f)        #note this places the first job on hold. 
        #subprocess.run(linecommand, shell=True)
        print(linecommand)
        print('echo $sim1')
    else:
        simcount = 'sim{}'.format(count)
        prevcoutnname='sim{}'.format(count-1)
        linecommand = '{}=$(qsub -W depend=afterany:${} {})'.format(simcount,prevcoutnname,f)
        print(linecommand)
        print('echo ${}'.format(simcount))


#closing the textfile
sys.stdout.close()
sys.stdout=orig_stdout    













