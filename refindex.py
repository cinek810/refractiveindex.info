#!/usr/bin/python

import yaml
from parse import *
from string import split
import sys
import numpy as np
import cmath 

#import refFunctions


def formula_2(coeff,da_range,l):
	n=1+coeff[0]
	print n
	if l>=da_range[0] and l<=da_range[1]:
		for i in range(1,np.size(coeff),2):
			print "---"
			print coeff[i]
			print coeff[i+1]
			print  l
			print  l**2
			print ((coeff[i]*l**2)/(l**2-coeff[i+1]**2))
		
			n=n+((coeff[i]*l**2)/(l**2-coeff[i+1]**2))
			print "n="+str(cmath.sqrt(n))	
	else:
		raise Exception("OutOfBands","No data for this material for this l")
	
	return cmath.sqrt(n)

def formula_3(coeff,da_range,l):
	n=coeff[0]
	if l>=da_range[0] and l<=da_range[1]:
		for i in range(1,np.size(coeff),2):
			n=n+coeff[i]*l**coeff[i+1]
	else:
		raise Exception("OutOfBands","No data for this material for this l")
	
	return cmath.sqrt(n)




def searchMaterial(yamlFile,bookName,nmin,nmax):

	#Function used only internally to display material parameters values	
	def printParams(paramsArray,paramList,comment):
		for param in paramList:
			sys.stdout.write(str(paramsArray[-1][param])+" ");
		sys.stdout.write(comment+"\n");


	#Just some boolen, if the firs element is OK it may not be shown
	#it's defined only for first material for the rest it's undefined at the begining
	print_in_my_range=False;


	#This parameter decides additional output about parameters inside range have been met
	my_range=False;
	
	yamlStream=open(yamlFile,'r')
	allData=yaml.load(yamlStream);

	materialData=allData["DATA"][0]

	if materialData["type"]=="tabulated nk":
		lines=materialData["data"].split('\n')
		params=[]
		for line in lines:
			params.append(parse("{l:g} {n:g} {k:g}",line));
		
			try:
				if (params[-1]["n"]>nmin and params[-1]["n"]<nmax) :
					if my_range == False:
						printParams(params,["l","n","k"],bookName+" start_range")
					if print_in_my_range:
						printParams(params,["l","n","k"],bookName+" inner_range tabulated nk")
					my_range=True
				else:
					if my_range == True:
						printParams(params,["l","n","k"],bookName+" end")
					my_range=False
			except TypeError:
				#Do nothink, it's ok
				sys.stderr.write( "TypeError in ("+yamlFile+"):"+str(params[-1])+". Line was:'"+line+"'\n")
		
	elif materialData["type"]=="tabulated n":
		lines=materialData["data"].split('\n')
		params=[]
		for line in lines:
			params.append(parse("{l:g} {n:g}",line));
		
			try:
				if (params[-1]["n"]>nmin and params[-1]["n"]<nmax) :
					if my_range == False:
						printParams(params,["l","n"],bookName+" start_range")
					if print_in_my_range:
						printParams(params,["l","n"],bookName+" inner_range tabulated n")
					my_range=True
				else:
					if my_range == True:
						printParams(params,["l","n"],bookName+" end_range")
					my_range=False
			except TypeError:
				#Do nothink, it's ok
				sys.stderr.write( "TypeError in ("+yamlFile+"):"+str(params[-1])+". Line was:'"+line+"'\n")

####### elif materialData["type"]=="formula 2":
####### 	data_range=np.array(map(float,materialData["range"].split()));
####### 	data_coeff=np.array(map(float64,materialData["coefficients"].split()));

####### 	params=[]
####### 	for lamb in np.linspace(data_range[0],data_range[1],100):
####### 		complex_n=formula_2(data_coeff,data_range,lamb);
####### 		params.append(dict([('l',lamb),('n',complex_n.real),('k',complex_n.imag)]));
####### 		try:
####### 			if (params[-1]["n"]>nmin and params[-1]["n"]<nmax) :
####### 				if my_range == False:
####### 					printParams(params,["l","n","k"],bookName+" start_range")
####### 				if print_in_my_range:
####### 					printParams(params,["l","n","k"],bookName+" inner_range formula_2")
####### 				my_range=True
####### 			else:
####### 				if my_range == True:
####### 					printParams(params,["l","n","k"],bookName+" end_range")
####### 				my_range=False
####### 		except TypeError:
####### 			#Do nothink, it's ok
####### 			sys.stderr.write( "TypeError in ("+yamlFile+"):"+str(params[-1])+". Line formula_3\n")


	elif materialData["type"]=="formula 3":
		data_range=np.array(map(float,materialData["range"].split()));
		data_coeff=np.array(map(float,materialData["coefficients"].split()));

		params=[]
		for lamb in np.linspace(data_range[0],data_range[1],100):
			complex_n=formula_3(data_coeff,data_range,lamb);
			params.append(dict([('l',lamb),('n',complex_n.real),('k',complex_n.imag)]));
			try:
				if (params[-1]["n"]>nmin and params[-1]["n"]<nmax) :
					if my_range == False:
						printParams(params,["l","n","k"],bookName+" start_range")
					if print_in_my_range:
						printParams(params,["l","n","k"],bookName+" inner_range formula_3")
					my_range=True
				else:
					if my_range == True:
						printParams(params,["l","n","k"],bookName+" end_range")
					my_range=False
			except TypeError:
				#Do nothink, it's ok
				sys.stderr.write( "TypeError in ("+yamlFile+"):"+str(params[-1])+". Line formula_3\n")


			

prefix="database/"
lib=yaml.load(open(prefix+"library.yml",'r'))



for schelf in lib:
#	print schelf[0]
#	print schelf
	bookName="NoBookSet"
	for materials in schelf["content"]:
		for k,v in materials.iteritems():
			if k=="BOOK":
				bookName=v

			if k=="content":
				matName=bookName
				fileName=prefix+v[0]["path"]

				searchMaterial(fileName,matName,0,1)	

#		for material in materials["content"]:
#			print material
	print "\n\n"

