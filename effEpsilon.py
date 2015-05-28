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


#Change refractive index to epsilon
matData1=getData(file1,lambdas)
for i in range(0,len(matData1)):
	matData1[i]=matData1[i]*matData1[i]

matData2=getData(file2,lambdas)
for i in range(0,len(matData2)):
	matData2[i]=matData2[i]*matData2[i]

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
	




plt.figure("Materials:"+file1+" "+file2)
plt.subplot(211)
plt.plot(1000*lambdas,matData1,'r-',label="Real("+file1+")")
plt.plot(1000*lambdas,matData2,'b--',label="Real("+file2+")")
plt.xlabel(r"$\lambda$  [nm]")
#plt.ylim(0,2)
plt.legend()

plt.subplot(212)
plt.plot(1000*lambdas,[ x.imag for x in matData1],'r-',label="Imag("+file1+")")
plt.plot(1000*lambdas,[ x.imag for x in matData2],'b--',label="Imag("+file2+")")
plt.xlabel(r"$\lambda$ [nm]")
plt.legend()

#number of ticks
TN=5
#formated list of wavelengths to be displayed
lambTicks=[]
for lamb in np.linspace(min(lambdas),max(lambdas),TN):
	lambTicks.append("%0.1f"%lamb)

fTicks=np.linspace(0,1,TN)




VMIN=-10#min(np.min(R1),np.min(R2))
VMAX=30#max(np.max(R1),np.max(R2))

	
plt.figure("Effective:"+file1+" "+file2)
plt.subplot(2,2,1)
plt.imshow(R1,vmin=VMIN,vmax=VMAX)
plt.ylabel("f")
plt.title(r'Re{$\epsilon_x$}')


#START:generic settings for all plots
#plt.xticks(np.linspace(0,R1.shape[0],TN),lambTicks)
plt.xticks([])
plt.yticks(np.linspace(0,R1.shape[1],TN),fTicks)
#END:generic settings for all plots

#We can choose contour position with changing this line:
plt.contour(R1,[0.],colors="k")




plt.subplot(2,2,2)
plt.imshow(R2,vmin=VMIN,vmax=VMAX)
plt.title(r'Re{$\epsilon_z$}')

#START:generic settings for all plots
plt.colorbar()
plt.xticks([])
plt.yticks([])
#END:generic settings for all plots



VMIN=min(np.min(I1),np.min(I2))
VMAX=10#max(np.max(I1),np.max(I2))
#We can choose contour position with changing this line:
plt.contour(R2,[100.],colours="w")

plt.subplot(2,2,3)
plt.imshow(I1,vmin=VMIN,vmax=VMAX)
plt.xlabel(r"$\lambda$ [nm]")
plt.ylabel("f")
plt.title(r'Im{$\epsilon_x$}')

#START:generic settings for all plots
plt.xticks(np.linspace(0,R1.shape[0],TN),1000*lambTicks)
plt.yticks(np.linspace(0,R1.shape[1],TN),fTicks)
#END:generic settings for all plots

#We can choose contour position with changing this line:
#plt.contour(I1,[1.])




plt.subplot(2,2,4)
plt.imshow(I2,vmin=VMIN,vmax=VMAX)
plt.xlabel(r"$\lambda$ [nm]")
plt.title(r'Im{$\epsilon_z$}')


#START:generic settings for all plots
plt.colorbar()
plt.xticks(np.linspace(0,R1.shape[0],TN),1000*lambTicks)
plt.yticks([])
#END:generic settings for all plots

#We can choose contour position with changing this line:
#plt.contour(I2,[1.])




plt.subplots_adjust(left=0.01, bottom=0.1, right=0.99, top=0.9, wspace=0, hspace=0.15)
plt.suptitle("")



#plt.figure("eps1eps2:"+file1+" "+file2)
##C=np.empty(shape=R1.shape,dtype="complex")
#Cr=np.empty(shape=R1.shape)
#Ci=np.empty(shape=R1.shape)
#for i in range(0,R1.shape[1]):
#	for j in range(0,R1.shape[0]):
#		C=(R1[i][j]+1j*I1[i][j]) * (R2[i][j]+1j*I2[i][j])
#		Cr[i][j]=C.real
#		Ci[i][j]=C.imag
#
#
#plt.subplot(2,2,1)	
#plt.title(r"$\epsilon_1 \cdot \epsilon_2$",size=20)
#plt.imshow(abs(1-Cr),vmin=-50,vmax=50)
#plt.title("Real")
#plt.colorbar(fraction=0.046, pad=0.04)
#plt.xticks(np.linspace(0,R1.shape[0],TN),lambTicks)
#plt.yticks(np.linspace(0,R1.shape[1],TN),fTicks)
#plt.contour(Cr,[1],colors="w")
#
#plt.subplot(2,2,2)
#plt.title("Imag")
#plt.imshow(abs(Ci),vmin=-50,vmax=50)
#plt.colorbar(fraction=0.046, pad=0.04)
#plt.xticks(np.linspace(0,R1.shape[0],TN),lambTicks)
#plt.yticks(np.linspace(0,R1.shape[1],TN),fTicks)
#plt.contour(Ci,[0],colors="w")
#
#plt.subplot(2,2,3)
#
#plt.contour(Cr,[1],colors="b")
#plt.contour(Ci,[0],colors="r")
#plt.xticks(np.linspace(0,R1.shape[0],TN),lambTicks)
#plt.yticks(np.linspace(0,R1.shape[1],TN),fTicks)
#
#plt.subplot(2,2,4)
##Calculated R for normal incidence
#Refle=np.empty(shape=R1.shape)
#n=np.empty(shape=R1.shape,dtype="complex")
#for i in range(0,R1.shape[1]):
#	for j in range(0,R1.shape[0]):
#		n=cmath.sqrt(R1[i][j]+1j*I1[i][j])
#		Refle[i][j]=abs((n-1)/(n+1))*abs((n-1)/(n+1))
#
#plt.imshow(Refle,vmin=0,vmax=1)	
#plt.colorbar(fraction=0.046, pad=0.04)
#plt.title("Reflection for normal incidence")
#plt.xticks(np.linspace(0,R1.shape[0],TN),lambTicks)
#plt.yticks(np.linspace(0,R1.shape[1],TN),fTicks)
#
#minRef=np.average(Refle,axis=1)
#print minRef

#if np.any(minRef<0.1):
plt.show()


