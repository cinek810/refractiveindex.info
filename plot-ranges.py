#!/usr/bin/python

import pickle

f=open("temporary-range-res.sav",'r');
resrange=pickle.load(f);
f.close


f=open("temporary-names-res.sav",'r');
resnames=pickle.load(f);
f.close


import matplotlib.pyplot as plt
fig, ax = plt.subplots()
count=1
yyyticks=[]
for resr in resrange:
	ax.broken_barh(resr,(count, 9), facecolors='blue')
	yyyticks.append(count+5)
	count+=10
ax.set_yticklabels(resnames)
print len(resnames)
print len(yyyticks)
ax.set_yticks(yyyticks)
ax.set_ylim(0,count+1)
ax.grid(True)

plt.show()
