#!/usr/bin/python

import sys

prefix=""
if len(sys.argv)<3:
	sys.stderr.write("You have to specify at least 2 arguments, Lambda min and Lambda max\n")
	sys.exit(1)
elif len(sys.argv)>4:
	sys.stderr.write("max 3 arguments: lambda_min lambda_max prefix\n")	
elif len(sys.argv)==4:
	prefix=sys.argv[3]



xmin=float(sys.argv[1])
xmax=float(sys.argv[2])


import pickle

f=open(prefix+"temporary-range-res.sav",'r');
resrange=pickle.load(f);
f.close


#f=open("temporary-names-res.sav",'r');
#resnames=pickle.load(f);
#f.close

f=open("temporary-lims-res.sav",'r');
epsLimits=pickle.load(f);
f.close

#print len (resrange)
#print len(resnames)
#assert len(resrange)==len(resnames)



import matplotlib.pyplot as plt

import matplotlib.colors as col

#Preparing colour list:
colourNames=[]
for name,hexCode in col.cnames.iteritems():
	colourNames.append(name);





fig, ax = plt.subplots()

ax.set_xlim(xmin,xmax)
count=1
#Iterate colours, start -1 because of preincrementation
iterator=-1;
yyyticks=[]
resnamesFounded=[]

print resrange

for resDict in resrange:
	#If it happens that specified material wasn't found in  
	#the region of interes skip it
	for resname,resr in resDict.items():
		fullFile=resname
		resname=resname.split('/')
		material=resname[-2]
		resname=resname[-1]+"_"+resname[-2]
		inRanges=[]
		print resname
		for rangeTuple in resr:
			if( rangeTuple[0]> xmin and rangeTuple[0]<xmax) or (rangeTuple[1]>xmin and rangeTuple[1]<xmax  ):
				inRanges.append((rangeTuple[0],rangeTuple[1]-rangeTuple[0]))
		
		
		#Add plot if in range
		if inRanges==[]:
			continue;


		if iterator==-1 or material!=resnamesFounded[-1].split("_")[1]:
			iterator+=1

		ax.broken_barh(inRanges,(count, 9), facecolors=colourNames[iterator])
		print "RESNAMES:./effEpsilon.py "+fullFile
		resnamesFounded.append(resname)
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
