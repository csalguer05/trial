"""
Spaghetti plot

To run:
>>> python3 chart_v3.py name.json

"""
import sys,os
import json
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

#def load_data(json_file):
json_file='%s' % sys.argv[1]
with open(json_file,'r') as indata:
	data = json.load(indata)

name, cmmt, para, Etot, type, hop, label=data

with open('second-batch-measurements.json','r') as indata:
        data2 = json.load(indata)

name2, cmmt2, para2, Etot2, type, hop2, label2=data2

def states(txt):
	#this function's purpose is to convert a txt file into a  list that will allow you to organize the different trajectories into their respective states
	
	#the following 2 lines create a dictionary, which is used to store the traj information in a more organized way and a counter which
	#allows you to create a key with the proper state
	dic={}
	q = 0
	st_i = list()	
	#the following in the loop opens the txt file that you have create.
	with open(txt, 'r') as infile:
		#the following lines allows you to concacatenate a letter 's' ,representated of 'state' + the number of the state to create the keys for the dictionaries.
		# after it break down txt file by line which allows you to place the traj into their respective keys (states)
		for line in infile:
			#the line below creates the keys
			st = "s"+str(q)
			#the line below splits the txt by line
			dic[st] = line.split()
			#the line below then raises the counter to make the different keys that are representative of their states
			q = q + 1

	#the following loops now breaks down the dictionary into a list which is then returned
	for i in dic: #this is where the loop enters the dictionary through is keys, i = keys, there for to obtaine the list for the specific states is dictionary[key]
		index= dic[i]
		#the following line is an abbreviated form a list, the topic is known as a list comprehension for python, and it allows for the list to be converted from
		#a str value types to int value types
		i = [int(s) for s in index]
		st_i.append(i)
	return st_i

def spaghetti_plt(st_i, cutoff,meas_1,meas_2):
	"""
	this function allows the user to take the list that is returned in the states() function and turn it into a plot
	"""

	#the following 3 lines are initializing the plots as a local variable rather than a global one. 
	x,y,x2,y2=[],[],[],[]
	fig = plt.figure()
	ax = fig.add_subplot(111)
	for i in st_i: 
		for j in i: 
			j = j - 1 
			ts = len(para[j])
			if ts <= cutoff:
				for k in range(ts):
					x.append(para[j][k][0][meas_1][0])
					y.append(para[j][k][0][meas_2][0])
				ax.plot(x,y,marker='o',markersize=0.,linewidth=0.5,alpha=0.3)
				x=list()
				y=list()
			else:
				continue

	"""
	Adds the hopping points from the ground state into the plot
	"""
	for i in st_i[0]:
		i = i - 1
		ts = len(para[i])
		if ts <= cutoff:
			ci = hop[i]
			if len(ci)>0: 
				ci = ci[-1] - 1 
				x2.append(para[i][ci][0][meas_1][0])
				y2.append(para[i][ci][0][meas_2][0])
			else:
				continue

		else:
			continue
	
	ax.scatter(x2,y2,color='black',marker='o',s=3,zorder=3)

	###THIS IS WHERE THE X AND Y LIMITS ARE PLACED###
	ax.set_xlim(1,3.5)
	ax.set_ylim(1,3.5)
	plt.savefig("spaghetti.png",dpi=1200)

def avg_sp(st_i, cutoff,avg_1,avg_2,meas_3):
	"""
	avgs two measurements and creates a spaghetti with a third measurement
	"""
	x,y,z,x2,y2,z2,l = [],[],[],[],[],[],[]	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	for i in st_i: 
		for j in i: 
			j = j - 1 
			ts = len(para[j])
			if ts <= cutoff:
				for k in range(ts):
					x.append(para[j][k][0][avg_1][0])
					y.append(para[j][k][0][avg_2][0])
					z.append(para[j][k][0][meas_3][0])
				
 				"""
				This section calculates the averages of the two measurements 
				"""
				lists = [x,y]
				a = [np.array(x) for x in lists]
				l = [np.mean(f) for f in zip(*a)]
				print(len(l))	
				ax.plot(l,z,marker='o',markersize=0.,linewidth=0.5,alpha=0.3)
				x=list()
				y=list()
				z=list()
				l=list()
				lists=list()
			else:
				continue


	"""
	Adds the hopping points from the ground state into the a list
	"""
	for i in st_i[0]:
		i = i - 1
		ts = len(para[i])
		if ts <= cutoff:
			ci = hop[i]
			if len(ci)>0:
				ci = ci[-1] - 1 
				x2.append(para[i][ci][0][avg_1][0])
				y2.append(para[i][ci][0][avg_2][0])
				z2.append(para[i][ci][0][meas_3][0])
			else:
				continue

		else:
			continue

	"""
	Adds the hopping points from the ground state into the plot correctly as they need to avg as well
	"""
	lists = [x2,y2]
	a = [np.array(x2) for x2 in lists]
	l = [np.mean(f) for f in zip(*a)]
	ax.scatter(l,z2,color='black',marker='o',s=3,zorder=3)
	
	###THIS IS WHERE THE X AND Y LIMITS ARE PLACED###
	ax.set_xlim(1.4,2)
	ax.set_ylim(90,120)
	plt.savefig("avg_sp.png",dpi=1200)

def filter(st_i,bond1,bond2):
	"""
	Creates a plot using the a distance cutoff
	"""

	x,y,z,x2,y2,z2,l = [],[],[],[],[],[],[]
	fig = plt.figure()
	ax = fig.add_subplot(111)
	print(para[464][-1][0][0][0])
	for i in st_i: 
		for j in i: 
			j = j - 1 
			print(j)
			b1 = para[j][-1][0][bond1][0]
			b2 = para[j][-1][0][bond2][0]
			if b1 > 3.3 or b2 > 3.3:
				for k in range(len(para[j])):
					x.append(para[j][k][0][bond1][0])
					y.append(para[j][k][0][bond2][0])
				ax.plot(x,y,marker='o',markersize=0.,linewidth=0.5,alpha=0.3)
				x=list()
				y=list()
			else:
				continue


	"""
	Adds the hopping points from the ground state into the plot
	"""
	for i in st_i[0]:
		i = i - 1
		b1 = para[i][-1][0][bond1][0]
		b2 = para[i][-1][0][bond2][0]
		if b1 > 3.3 or b2 > 3.3:
			ci = hop[i]
			if len(ci)>0:
				ci = ci[-1] - 1 
				x2.append(para[i][ci][0][bond1][0])
				y2.append(para[i][ci][0][bond2][0])
			else:
				continue

		else:
			continue
	ax.scatter(x2,y2,color='black',marker='o',s=3,zorder=3)
	###THIS IS WHERE THE X AND Y LIMITS ARE PLACED###
	ax.set_xlim(1.4,2)
	ax.set_ylim(90,120)
	plt.savefig("filtered.png",dpi=1200)


def longest_sp(st_i, cutoff,comp_1,comp_2,meas_3):
	"""
	This compares two measurements and descides which one is bigger
	"""
	x,y,z,x2,y2,z2,l = [],[],[],[],[],[],[]
	fig = plt.figure()
	ax = fig.add_subplot(111)
	for i in st_i: 
		for j in i: 
			j = j - 1 
			ts = len(para[j])
			if ts <= cutoff:
				for k in range(ts):
					x.append(para[j][k][0][comp_1][0])
					y.append(para[j][k][0][comp_2][0])
					z.append(para[j][k][0][meas_3][0])
				"""
				This compares the 2 intended measurements and plots them
				"""
				for i in range(len(x)):
					if x[i] > y[i]:
						l.append(x[i])
					else:
						l.append(y[i])
				ax.plot(l,z,marker='o',markersize=0.,linewidth=0.5,alpha=0.3)
				x=list()
				y=list()
				z=list()
				l=list()
			else:
				continue

	"""
	Adds the hopping points from the ground state into the plot correctly as they need to avg as well
	"""
	for i in st_i[0]:
		i = i - 1
		ts = len(para[i])
		if ts <= cutoff:
			ci = hop[i]
			if len(ci)>0:
				ci = ci[-1] - 1 
				x2.append(para[i][ci][0][comp_1][0])
				y2.append(para[i][ci][0][comp_2][0])
				z2.append(para[i][ci][0][meas_3][0])
			else:
				continue

		else:
			continue

	for i in range(len(x2)):
		if x2[i] > y2[i]:
			l.append(x2[i])
		else: 
			l.append(y2[i])
	ax.scatter(l,z2,color='black',marker='o',s=3,zorder=3)

	###THIS IS WHERE THE X AND Y LIMITS ARE PLACED###
	ax.set_xlim(1.4,2)
	ax.set_ylim(90,120)
	plt.savefig("longest_sp.png",dpi=1200)	
	
print(cmmt)
st_i = states('states.txt')
filter(st_i,0,1)
