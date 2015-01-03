#!/usr/bin/python

import pickle

f=open("temporary-range-res.sav",'r');
resrange=pickle.load(f);
f.close


f=open("temporary-names-res.sav",'r');
resnames=pickle.load(f);
f.close


import matplotlib.pyplot as plt

import matplotlib.colors as col

#Preparing colour list:
colourNames=[]
for name,hexCode in col.cnames.iteritems():
	colourNames.append(name);


#Use limiting if you need
xmin=0.3
xmax=1.4



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
	inRanges=False;
	for rangeTuple in resr:
		if( rangeTuple[0]> xmin and rangeTuple[0]<xmax) or (rangeTuple[1]<xmax and rangeTuple[1]>xmin):
			inRanges=True
	
	#Increase iterator	
	iterator+=1
	
	#Add plot if in range
	if inRanges==False:
		continue;

	ax.broken_barh(resr,(count, 9), facecolors=colourNames[iterator])
	resnamesFounded.append(resnames[iterator])
	yyyticks.append(count+5)
	count+=10

ax.set_yticklabels(resnamesFounded)
print len(resnamesFounded)
print len(yyyticks)
ax.set_yticks(yyyticks)
ax.set_ylim(0,count+1)
ax.grid(True)
ax.set_xlabel("wavelength [um]")


plt.show()
