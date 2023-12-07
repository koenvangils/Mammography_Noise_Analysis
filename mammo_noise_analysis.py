import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd

def fitfunc(X,e,q,s):
	return (e/X)**2+q**2/X+s**2

def elec(X,e):
	return (e/X)**2

def quant(X,q):
	return q**2/X

def quantstruc(X,q,s):
	return q**2/X-s

df=pd.read_excel('measurement_values.xlsx')
entrancedose=df['Measured dose (uGy)'].to_numpy()
meanlist=df['Mean pixel value'].to_numpy()
sdlist=df['SD'].to_numpy()

detectordosefactor= (700/675)**2 #SID 700 mm, source to table 675 mm for Hologic 3Dimensions
detectordose=entrancedose/detectordosefactor #Entrance dose converted to detector dose

meanlistcorrected=meanlist-50 #Correct for pixel offset, 50 for Hologic 3Dimensions
fitlist=(sdlist/meanlistcorrected)**2

popt, pcov = curve_fit(fitfunc, detectordose, fitlist, bounds=(0,np.inf))
print('Fit parameters: \n popt: '+ str(popt) + '\n pcov: ' + str(pcov))
fitrange=np.linspace(1,10000,num=1000)

plt.scatter(detectordose,fitlist, label='Rel. noise')
plt.plot(fitrange,fitfunc(fitrange,*popt), label='Noise fit')
plt.plot(fitrange,elec(fitrange,popt[0]), label='Elec. noise')
plt.plot(fitrange,quant(fitrange,popt[1]), label='Quant. noise')
plt.plot([1,1e4],[popt[2]**2,popt[2]**2], label='Struc. noise')
plt.loglog()
plt.xlabel('Detector dose ($\mu$Gy)')
plt.ylabel('SD$^2$/PV$^2$')
plt.legend()
plt.text(popt[0]**2/popt[1]**2,elec(popt[0]**2/popt[1]**2,popt[0])/10,str(int(np.round(popt[0]**2/popt[1]**2))))
plt.text(popt[1]**2/popt[2]**2,popt[2]**2/10,str(int(np.round(popt[1]**2/popt[2]**2))))
plt.savefig('plot.png')
print('Intersect quantum noise and electronic noise: '+str(popt[0]**2/popt[1]**2)+' uGy')
print('Intersect quantum noise and structure noise: '+str(popt[1]**2/popt[2]**2)+ ' uGy')