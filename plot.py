#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import yaml
from parse import *
import sys
import cmath
import numpy as np

from getData import *


def NtoEps(matVec):
	matVec=np.array(matVec)
	lamb=matVec[:,0]
	n=matVec[:,1]
	k=matVec[:,2]

	N=n[:]+1j*k[:]
	eps=N[:]*N[:]


	matEps=[lamb,eps.real,eps.imag]
	return matEps




		
import matplotlib.pyplot as plt



#Plotting Ag
#hag=getData("database/main/Ag/Hagemann.yml");
range=(0.280,0.790)
lambdasAg=np.linspace(range[0],range[1],100)
ag=getData("database/main/Ag/Johnson.yml",lambdasAg);
#print ag
lambdasTiO2=np.linspace(0.280,0.790)
#tio2=getData("database/main/TiO2/Devore-o.yml",lambdasTiO2);
tio2=getData("database/main/SiO2/Malitson.yml",lambdasTiO2);



fig=plt.figure()
plt.plot(lambdasTiO2*1e3,[ x.real for x in tio2],'g-',label=r'Real($n_{SiO_{2}}$)')


plt.legend()
plt.title(r"Współczynnik załamania $SiO_2$ ($n$)");
plt.ylabel('')
plt.xlabel('wavelength [nm]')
plt.xlim([280,750])

plt.savefig("../phd/images/sio2n.png")


fig=plt.figure()
plt.plot(lambdasAg*1e3,[ x.real for x in ag ],'r-',label=r'Real($n_{Ag}$)')

plt.plot(lambdasAg*1e3,[ x.imag for x in ag] ,'b-',label=r'Imag($n_{Ag}$)')
#plt.plot(lambdasTiO2*1e3,[ x.real for x in tio2],'g-',label=r'Real($n_{TiO_{2}}$)')


plt.legend()
plt.title(r"Współczynnik załamania srebra ($n$)");
plt.ylabel('')
plt.xlabel('wavelength [nm]')
plt.xlim([280,750])
plt.ylim([0,3])

plt.savefig("../phd/images/agn.png")

fig=plt.figure()
plt.plot(lambdasAg*1e3,[ (x*x).real for x in ag ],'r-',label=r'Real($\varepsilon_{Ag}$)')

plt.plot(lambdasAg*1e3,[ (x*x).imag for x in ag] ,'b-',label=r'Imag($\varepsilon_{Ag}$)')
#plt.plot(lambdasTiO2*1e3,[ (x*x).real for x in tio2],'g-',label=r'Real($\varepsilon_{TiO_{2}}$)')


plt.legend()
plt.title(r"Współczynnik przenikalnośći elektrycznej ($\varepsilon$)");
plt.ylabel('')
plt.xlabel('wavelength [nm]')
plt.xlim([380,750])
#plt.ylim([-1.5,1.5])
plt.savefig("../phd/images/agtio2eps.png")

########
#GaAs do rozdzialu o THz

plt.show()
