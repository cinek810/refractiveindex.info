#!/usr/bin/python

import numpy as np
import sys
from getData import *
import matplotlib.pylab as plt


def effEpsilon(epsv1,epsv2,f):

	epsw1=[]
	epsw2=[]
	for eps1,eps2 in zip(epsv1,epsv2):
		epsw1.append(  f * eps1 + (1-f) * eps2)
		epsw2.append( 1./(f/eps1 + (1-f)/eps2))
	return (epsw1,epsw2)


if len(sys.argv)!=3:
	sys.stderr.write("You have to give exactly 2 arguments, yaml files with material descriptioni\n")
	sys.exit(1)
file1=sys.argv[1]
file2=sys.argv[2]

matFile1=open(file1,'r')
matFile2=open(file2,'r')



matRange1=getRange(file1)
matRange2=getRange(file2)
sys.stderr.write("matRange1="+str( matRange1))
sys.stderr.write("matRange2="+str( matRange2))

comRange=np.empty(shape=(2,1))
comRange[0]=matRange1[0] if matRange1[0]>matRange2[0] else matRange2[0]
comRange[1]=matRange1[1] if matRange1[1]<matRange2[1] else matRange2[1]

sys.stderr.write("comRange="+str(comRange))

#Sampling definition:
lambdas=np.linspace(comRange[0],comRange[1],100)

matData1=getData(file1,lambdas)
matData2=getData(file2,lambdas)

R1=np.empty(shape=(0,len(lambdas)))
I1=np.empty(shape=(0,len(lambdas)))

R2=np.empty(shape=(0,len(lambdas)))
I2=np.empty(shape=(0,len(lambdas)))

for f in np.linspace(0,1,100):
	(efw1,efw2)=effEpsilon(matData1,matData2,f)

	r1 = [x.real for x in efw1]
	i1 = [x.imag for x in efw1]

	r2 = [x.real for x in efw2]
	i2 = [x.imag for x in efw2]

	R1=np.vstack((R1,r1))
	I1=np.vstack((I1,i1))

	R2=np.vstack((R2,r2))
	I2=np.vstack((I2,i2))
	




plt.figure()
plt.subplot(211)
plt.plot(lambdas,matData1,'r-',label="Real(material1)")
plt.plot(lambdas,matData2,'b--',label="Real(material2)")
plt.legend()

plt.subplot(212)
plt.plot(lambdas,[ x.imag for x in matData1],'r-',label="Real(material1)")
plt.plot(lambdas,[ x.imag for x in matData2],'b--',label="Real(material2)")
plt.legend()

#number of ticks
TN=5
#formated list of wavelengths to be displayed
lambTicks=[]
for lamb in np.linspace(min(lambdas),max(lambdas),TN):
	lambTicks.append("%0.1f"%lamb)

fTicks=np.linspace(0,1,TN)
	
plt.figure()
plt.subplot(2,2,1)
plt.imshow(R1)
plt.ylabel("f")
plt.title(r'Re{$\epsilon_1$}')


#START:generic settings for all plots
plt.colorbar()
plt.xticks(np.linspace(0,R1.shape[0],TN),lambTicks)
plt.yticks(np.linspace(0,R1.shape[1],TN),fTicks)
#END:generic settings for all plots

#We can choose contour position with changing this line:
plt.contour(R1,[1.])




plt.subplot(2,2,2)
plt.imshow(R2)
plt.title(r'Re{$\epsilon_2$}')

#START:generic settings for all plots
plt.colorbar()
plt.xticks(np.linspace(0,R1.shape[0],TN),lambTicks)
plt.yticks(np.linspace(0,R1.shape[1],TN),fTicks)
#END:generic settings for all plots



#We can choose contour position with changing this line:
plt.contour(R2,[1.])

plt.subplot(2,2,3)
plt.imshow(I1)
plt.xlabel("Wavelength [um]")
plt.ylabel("f")
plt.title(r'Im{$\epsilon_1$}')

#START:generic settings for all plots
plt.colorbar()
plt.xticks(np.linspace(0,R1.shape[0],TN),lambTicks)
plt.yticks(np.linspace(0,R1.shape[1],TN),fTicks)
#END:generic settings for all plots

#We can choose contour position with changing this line:
plt.contour(I1,[0.])

plt.subplot(2,2,4)
plt.imshow(I2)
plt.xlabel("Wavelength [um]")
plt.title(r'Im{$\epsilon_2$}')


#START:generic settings for all plots
plt.colorbar()
plt.xticks(np.linspace(0,R1.shape[0],TN),lambTicks)
plt.yticks(np.linspace(0,R1.shape[1],TN),fTicks)
#END:generic settings for all plots

#We can choose contour position with changing this line:
plt.contour(I2,[0.])

plt.suptitle("f=1 means that everything is "+file1+",f=0 means everything"+file2)

plt.show()
