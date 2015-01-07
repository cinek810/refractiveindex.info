#!/usr/bin/python

import sys

if len(sys.argv)!=3:
	sys.stderr.write("You have to specify exactly 2 arguments, Lambda min and Lambda max")

xmin=float(sys.argv[1])
xmax=float(sys.argv[2])


import pickle

f=open("temporary-range-res.sav",'r');
resrange=pickle.load(f);
f.close


f=open("temporary-names-res.sav",'r');
resnames=pickle.load(f);
f.close

f=open("temporary-lims-res.sav",'r');
epsLimits=pickle.load(f);
f.close




import matplotlib.pyplot as plt

import matplotlib.colors as col

#Preparing colour list:
colourNames=[]
for name,hexCode in col.cnames.iteritems():
	colourNames.append(name);





fig, ax = plt.subplots()

ax.set_xlim(xmin,xmax)
count=1
#Incrementation is before usage, so start with -1:
iterator=-1;
yyyticks=[]
resnamesFounded=[]
for resr in resrange:
	#If it happens that specified material wasn't found in  
	#the region of interes skip it
	inRanges=[]
	for rangeTuple in resr:
		if( rangeTuple[0]> xmin and rangeTuple[0]<xmax) or (rangeTuple[1]<xmax and rangeTuple[1]>xmin):
			inRanges.append((rangeTuple[0],rangeTuple[1]-rangeTuple[0]))
	
	#Increase iterator	
	iterator+=1
	
	#Add plot if in range
	if inRanges==[]:

		continue;

	print iterator

	print inRanges
	print resnames[iterator]

	ax.broken_barh(inRanges,(count, 9), facecolors=colourNames[iterator])
	resnamesFounded.append(resnames[iterator])
	yyyticks.append(count+5)
	count+=10

ax.set_yticklabels(resnamesFounded)
print len(resnamesFounded)
print len(yyyticks)
ax.set_title("Materials with epsilon in <"+str(epsLimits[0])+","+str(epsLimits[1])+">")
ax.set_yticks(yyyticks)
ax.set_ylim(0,count+1)
ax.grid(True)
ax.set_xlabel("wavelength [um]")


plt.show()
