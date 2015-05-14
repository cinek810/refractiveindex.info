#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import numpy as np
import pylab as plt
from getData import *


import matplotlib
matplotlib.rcParams.update({'font.size': 30})

range=(1,17)
lambdas=np.linspace(range[0],range[1],100)
ag=getData("database/main/GaAs/Skauli.yml",lambdas);

fig=plt.figure()
plt.plot(lambdas,[ (x*x).real for x in ag ],'r-',label=r'Real($\varepsilon_{GaAs}$)')

#plt.plot(lambdas,[ (x*x).imag for x in ag] ,'b-',label=r'Imag($\varepsilon_{Ag}$)')
#plt.plot(lambdasTiO2*1e3,[ (x*x).real for x in tio2],'g-',label=r'Real($\varepsilon_{TiO_{2}}$)')

c=299792458
lambdas=lambdas*10e-6
freq=c/lambdas
freq=freq/10e12

#plt.plot(freq,[ (x*x).real for x in ag ],'r-',label=r'Real($\varepsilon_{Ag}$)')

plt.legend()
#plt.title(r"Współczynnik przenikalnośći elektrycznej ($\varepsilon$)");
plt.ylabel('')
plt.xlabel('wavelength [um]')
plt.xlim([1,17])
plt.tight_layout()

#plt.ylim([-1.5,1.5])
plt.savefig("../phd/images/gaaseps.png")

plt.show()




