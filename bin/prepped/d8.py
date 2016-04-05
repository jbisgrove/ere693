#####-------Copy Right-------------------------------------
	# D8 Modification, begins stream traces only at sources
    # Copyright (C) 2016  John Bisgrove

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see http://www.gnu.org/licenses/gpl-3.0.html.


## output of this code has been compared with output from arcGIS Flow Accumulation Tool, 
## run on the same Flow Direction Rasters. 
## Raster Calculator was then used in each instance to demonstrate that the two Flow Accumulation Rasters have a differenece of zero for each cell.

def printline(message):
	try:
		arcpy.AddMessage(message)
	except Exception:
		print message
	

def printError(message):
	try:
		arcpy.AddError(message)	
	except Exception:
		print message
	
def Outlet(value): 
	outlet = value
	#outlet == 1 #good
	r=0
	c=1
	if outlet==2: #good
		r=1
		c=1
	elif outlet==4: #good
		r=1
		c=0
	elif outlet==8: #good
		r=1
		c=-1
	elif outlet==16: #good
		r=0
		c=-1
	elif outlet==32: #good
		r=-1
		c=-1
	elif outlet==64: #good
		r=-1
		c=0
	elif outlet==128: #good
		r=-1
		c=1
	return r,c	
		
def Source(flowDirection,row,column,rows,columns):
	source=True
	for r in [-1, 0, 1]:
		if not source:
			break
		for c in [-1, 0, 1]:
			if r==0 and c==0:
				continue
			if (row+r) >= 0 and (row+r) < rows and (column+c) >= 0 and (column+c) < columns: 
				outlet = flowDirection[row+r][column+c]
				# (1,1) rejected in if statement above
				if outlet == 1 and r==0 and c==-1 : #good
					source=False
					break
				elif outlet==2 and r==-1 and c==-1 : #good
					source=False
					break
				elif outlet==4 and r==-1 and c==0 : #good
					source=False
					break
				elif outlet==8 and r==-1 and c==1 : #good
					source=False
					break
				elif outlet==16 and r==0 and c==1 : #good
					source=False
					break
				elif outlet==32 and r==1 and c==1 : #good
					source=False
					break
				elif outlet==64 and r==1 and c==0 : #good
					source=False
					break
				elif outlet==128 and r==1 and c==-1 : #good
					source=False
	return source