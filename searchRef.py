#!/usr/bin/python

import numpy as np
import yaml
from  getData import *

#TODO this function is generally dirty, but works so...
#it will wait infinite time to be changed
def searchRef(yamlFile,bookName,nmin,nmax):

	#List for result
	result=[]

	#Function used only internally to display material parameters values	
	#ATTENTION!!! comment is not only a comment is like command for this function (yes, it's dirty ;))
#	def printParams(paramsArray,paramList,comment):
#		for param in paramList:
#			sys.stdout.write(str(paramsArray[-1][param])+" ");
#		sys.stdout.write(comment+"\n");
#		if comment.find("start_range")!=-1:
	#		printParams.lastStart=paramsArray[-1]["l"]
	#	elif comment.find("end_range")!=-1:
	#		result.append((printParams.lastStart,paramsArray[-1]["l"]))
	#printParams.lastStart=0;

	#Just some boolen, if the firs element is OK it may not be shown
	#it's defined only for first material for the rest it's undefined at the begining
	print_in_my_range=False;


	#This parameter decides additional output about parameters inside range have been met
	my_range=False;
	
	yamlStream=open(yamlFile,'r')
	allData=yaml.load(yamlStream);

	materialData=allData["DATA"][0]

	#dataRange - where we can check the data
	dataRange=getRange(yamlFile)
	if dataRange[0]==0:
		return []

	#wavelengths to check for this material:
	#HERE WE DEFINE THE SAMPLING
	lambdas=np.linspace(dataRange[0],dataRange[1],100)

	#refractive indx
	nList=np.empty((1,0))
#	try:
	nList=getData(yamlFile,lambdas[:])
	if len(nList) == 1:
		return []
	eps=np.zeros(len(nList),dtype="complex")

	for i in range(0,len(nList)):
		eps[i]=nList[i]*nList[i]
#	except UnsupportedDataType as e:
#		sys.stderr.write(e)

	if len(nList)<100:
		return result
	inRange=False
	rangeStart=0
	
	for i in range(0,len(lambdas)):
		if eps[i].real>nmin and eps[i].real<nmax:
			if inRange==False:
				inRange=True
				rangeStart=lambdas[i]
		
		elif inRange:
			result.append((rangeStart,lambdas[i]))
			inRange=False
			

	return result
		
		

	

		





		
if __name__ == "__main__":
	import sys

	if len( sys.argv )!=3:
		sys.stderr.write("You have to give exactly two arguments- eps_min and eps_max\n")
		sys.exit(1)

	prefix="database/"
	lib=yaml.load(open(prefix+"library.yml",'r'))


	#List for resulted ranges
	resrange=[]
	#List for material names
	resnames=[]


	for schelf in lib:
		for materials in schelf["content"]:
			bookName="NoBookSet"
			if(materials.keys()[0]=="content"):
				bookName=materials["BOOK"]
				smallRes=dict()
				for myFileIsIn in materials["content"]:
					fileName=prefix+myFileIsIn["path"]
#					if bookName=="NoBookSet":
#						raise Exception("NoBookSet");
					result=searchRef(fileName,bookName,float(sys.argv[1]),float(sys.argv[2]))	
					if len(result)>0:
						for oneTuple in result:
							try:
								smallRes[fileName].append(oneTuple)
							except KeyError:
								smallRes[fileName]=[]
								smallRes[fileName].append(oneTuple)
				
				if len(smallRes)>0:
					resrange.append(smallRes)



	import pickle
	f=open("temporary-range-res.sav",'w')
	pickle.dump(resrange,f);
	f.close();

#	f=open("temporary-names-res.sav",'w')
#	pickle.dump(resnames,f);
#	f.close();


	f=open("temporary-lims-res.sav",'w')
	pickle.dump((float(sys.argv[1]),float(sys.argv[2])),f);
	f.close();


	print ("You can now call plot-ranges.py")
