#!/usr/bin/python


from scipy.interpolate import interp1d
import sys
from parse import *
import yaml
import numpy as np
import cmath



#This function is designed to return refractive index for specified lambda
#for file in "tabluated nk " format
def getDataNK(yamlFile,lamb):
	yamlStream=open(yamlFile,'r')
	allData=yaml.load(yamlStream);	

	materialData=allData["DATA"][0]


	assert materialData["type"]=="tabulated nk"

	matLambda=[]
	matN=[]
	matK=[]
	#in this type of material read data line by line
	for line in materialData["data"].split('\n'):
		parsed=parse("{l:g} {n:g} {k:g}",line)
		try:
			n=parsed["n"]+1j*parsed["k"]
			matLambda.append(parsed["l"]);
			matN.append(parsed["n"])
			matK.append(parsed["k"])
		except TypeError as e:
			sys.stderr.write("TypeError occured:"+str(e)+"\n")

	matLambda=np.array(matLambda)
	matN=np.array(matN)
	matK=np.array(matK)

	interN=interp1d(matLambda,matN)
	interK=interp1d(matLambda,matK)
	
	return interN(lamb)+1j*interK(lamb)

def getRangeNK(yamlFile):
	yamlStream=open(yamlFile,'r')
	allData=yaml.load(yamlStream);	

	materialData=allData["DATA"][0]

	assert materialData["type"]=="tabulated nk"
	#in this type of material read data line by line
	matLambda=[]
	for line in materialData["data"].split('\n'):
		parsed=parse("{l:g} {n:g} {k:g}",line)
		try:
			matLambda.append(parsed["l"])
		except TypeError as e:
			sys.stderr.write("TypeError occured:"+str(e)+"\n")
	return (min(matLambda),max(matLambda))
		
		



##this function is desined to get data from files in formula3 format
def getDataF2(yamlFile,lamb):
	yamlStream=open(yamlFile,'r')
	allData=yaml.load(yamlStream);	

	materialData=allData["DATA"][0]

	assert materialData["type"]=="formula 2"

	dataRange=np.array(map(float,materialData["range"].split()));
	coeff=np.array(map(float,materialData["coefficients"].split()));

	n=0
	if min(lamb)>=dataRange[0] or max(lamb)<=dataRange[1]:
		for i in reversed(range(1,np.size(coeff),2)):
			n=n+((coeff[i]*lamb**2)/(lamb**2-coeff[i+1]))
		
	else:
		raise Exception("OutOfBands","No data for this material for this l")
	
	n=n+coeff[0]+1
	nres=[]
	for oneN in n:
		nres.append(cmath.sqrt(oneN))
	return nres


##this function is desined to get data from files in formula3 format
def getDataF3(yamlFile,lamb):
	yamlStream=open(yamlFile,'r')
	allData=yaml.load(yamlStream);	

	materialData=allData["DATA"][0]

	assert materialData["type"]=="formula 3"

	dataRange=np.array(map(float,materialData["range"].split()));
	coeff=np.array(map(float,materialData["coefficients"].split()));




	n=coeff[0]
	if min(lamb)>=dataRange[0] and max(lamb)<=dataRange[1]:
		for i in range(1,np.size(coeff),2):
			n=n+coeff[i]*lamb**coeff[i+1]
	else:
		raise Exception("OutOfBands","No data for this material for lambda="+str(l))
	
	nres=[]
	for oneN in n:
		nres.append(cmath.sqrt(oneN))
	return nres






def Error(BaseException):
	pass

###this is general function to check data type, and run appropriate actions
def getData(yamlFile,lamb):
	yamlStream=open(yamlFile,'r')
	allData=yaml.load(yamlStream)
	materialData=allData["DATA"][0]

	if materialData["type"]=="tabulated nk":
		return	getDataNK(yamlFile,lamb)
	elif materialData["type"]=="formula 2":
		return getDataF2(yamlFile,lamb)
	elif materialData["type"]=="formula 3":
		return getDataF3(yamlFile,lamb)
	else:
	#	raise Error("UnsupportedDataType:This data type is currnetly not supported");
		return np.zeros((1,0))

def getRange(yamlFile):
	yamlStream=open(yamlFile,'r')
	allData=yaml.load(yamlStream)
	materialData=allData["DATA"][0]

	if materialData["type"]=="tabulated nk":
		return	getRangeNK(yamlFile)
	elif materialData["type"]=="formula 2":
		return np.array(map(float,materialData["range"].split())) 
	elif materialData["type"]=="formula 3":
		return np.array(map(float,materialData["range"].split()))
	else:
	#	raise Error("UnsupportedDataType:This data type "+materialData["type"] +" is currnetly not supported");
		return (0,0)




if __name__ == "__main__":
	print "Direct tests:"
	print "MyData="+str(getDataNK("database/main/Ag/Rakic.yml",1))+" ,test ~  0.23 + 6.41j"
	print "MyData="+str(getDataF3("database/other/doped crystals/Mg-LiTaO3/Moutzouris-e.yml",np.array([0.7473])))+" test ~"
	print "MyData="+str(getDataF2("./database/main/CaCO3/Ghosh-o.yml",np.array([0.204])))+", test ~ 1.88"
	print "Tests through general getData function "
	print "MyData="+str(getData("database/main/Ag/Rakic.yml",1))
	print "MyData="+str(getData("database/other/doped crystals/Mg-LiTaO3/Moutzouris-e.yml",np.array([0.7473])))
	print "MyData="+str(getData("./database/main/CaCO3/Ghosh-o.yml",np.array([0.204])))
