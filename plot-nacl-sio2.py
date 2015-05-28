#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import numpy as np
import pylab as plt
from getData import *

import matplotlib
matplotlib.rcParams.update({'font.size': 30,'font.weight':'bold'})

range=(7,10)
lambdas=np.linspace(range[0],range[1],100)
ag=getData("database/main/NaCl/Li.yml",lambdas);

fig=plt.figure()
plt.plot(lambdas,[ (x*x).real for x in ag ],'r-',label=r'Re',lw=4)

plt.plot(lambdas,[ (x*x).imag for x in ag] ,'b--',label=r'Im',lw=4)
#plt.plot(lambdasTiO2*1e3,[ (x*x).real for x in tio2],'g-',label=r'Real($\varepsilon_{TiO_{2}}$)')

c=299792458
lambdas=lambdas*10e-6
freq=c/lambdas
freq=freq/10e12

#plt.plot(freq,[ (x*x).real for x in ag ],'r-',label=r'Real($\varepsilon_{Ag}$)')

plt.legend(loc=1,borderpad=0,frameon=False)
#plt.title(r"Współczynnik przenikalnośći elektrycznej ($\varepsilon$)");
plt.xlabel(r'$\lambda$ [$\mu m$]')
plt.xlim([7,10])
plt.ylim([-4,8])
plt.tight_layout()

#plt.yscale('log')
plt.savefig("../phd/images/pml/nacl.png")





lambdas=np.linspace(range[0],range[1],100)
ag=getData("database/main/SiO2/Kischkat.yml",lambdas);
fig=plt.figure()
plt.plot(lambdas,[ (x*x).real for x in ag ],'r-',label=r'Re',lw=4)

plt.plot(lambdas,[ (x*x).imag for x in ag] ,'b--',label=r'Im',lw=4)
#plt.plot(lambdasTiO2*1e3,[ (x*x).real for x in tio2],'g-',label=r'Real($\varepsilon_{TiO_{2}}$)')

c=299792458
lambdas=lambdas*10e-6
freq=c/lambdas
freq=freq/10e12

#plt.plot(freq,[ (x*x).real for x in ag ],'r-',label=r'Real($\varepsilon_{Ag}$)')

plt.legend(loc=2,borderpad=0,frameon=False)
#plt.title(r"Współczynnik przenikalnośći elektrycznej ($\varepsilon$)");
plt.xlabel(r'$\lambda$ [$\mu m$]')
plt.xlim([7,10])
plt.ylim([-4,8])
plt.tight_layout()

#plt.yscale('log')
plt.savefig("../phd/images/pml/sio2.png")


plt.show()
