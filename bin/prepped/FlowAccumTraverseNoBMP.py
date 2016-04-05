#john bisgrove
#ERE 693
#Lab 5
#23 Feb 2016
# Tansverse Walk
# to be compared to the Transverse Walk without non-source origins.
#####-------Copy Right-------------------------------------
	# D8 Modifications, begins stream traces only at sources
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
	
#user set variables
noEdge=False
fileAppendix='_8'
inRaster = 'flowDirectionSmall2'
outRaster = 'flowAccumulationSmallPy'
outRaster+=fileAppendix	

# set environment variables
drive = 'J'
directory = ':/ESF/Classes/ERE693/Lab05/'
db = 'Lab05Geodatabase.gdb/'
# import library packages

import arcpy, os, sys, numpy
from arcpy import env
from arcpy.sa import *
import d8
from d8 import printline,printError,Outlet

#start conditions and time
start = datetime.datetime.now()
print 'program has started at ',start
#-----------------------------------------


printline('D8 Flow Accumulation : Program Started')
print ("D8 and Modifications Copyright (C) 2016  John Bisgrove"
    "This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'."
    "This is free software, and you are welcome to redistribute it"
    "under certain conditions; type `show c' for details.")
printline(os.path)
numpy.set_printoptions(threshold=numpy.nan)
if arcpy.CheckExtension("Spatial") == "Available":
    printline("Checking out Spatial")
    arcpy.CheckOutExtension("Spatial")
else:
    printError("Unable to get spatial analyst extension")
    printline(arcpy.GetMessages(0))
    sys.exit(0)
# get parameters (input and output datasets, filenames, etc)
##inputData = arcpy.GetParameter()
##outputData = arcpy.GetParameter()

printline('flow direction : '+inRaster+' flow accumulation '+outRaster)
# set environment
workspace = drive+directory+db
env.workspace = workspace
dsc=arcpy.Describe(workspace+inRaster)
arcpy.env.extent=dsc.Extent
printline ( arcpy.env.extent )
env.outputCoordinateSystem=dsc.SpatialReference
spatial_ref=dsc.SpatialReference
xCellSize = dsc.children[0].meanCellWidth
yCellSize = dsc.children[0].meanCellHeight
corner = arcpy.Point(dsc.extent.XMin, dsc.extent.YMin)
env.overwriteOutput = True
# Set Snap Raster environment
env.snapRaster = inRaster
# create variables to hold input and output datasets
flowDirection = arcpy.RasterToNumPyArray(inRaster)
rows = flowDirection.shape[0]
columns = flowDirection.shape[1]
printline( 'flowDirection rows: '+str(rows) +' columns: '+str(columns) )
flowAccumulation = numpy.zeros([rows,columns],dtype='float64')

# process (loop through) datasets

print 'entering traversal section'
for row in range(rows):
	sys.stdout.flush()
	print '\r',
	print row,
	#test if edge cell : CONTINUE
	if noEdge and (row == 0 or row == row-1):
		continue
	for column in range(columns):
		#test if edge cell : CONTINUE
		if noEdge and (column == 0 or column == columns-1):
			continue
			
		rWalk = row
		cWalk = column
		
		flowTrace = 1
		stream = True
		while stream:
			r,c =Outlet(flowDirection[rWalk][cWalk])
			if (rWalk+r) < 0 or (rWalk+r) >= rows or (cWalk+c) < 0 or (cWalk+c) >= columns :
				stream = False
			if not stream:
				break
			
			
			flowTrace = 1
			flowAccumulation[rWalk+r][cWalk+c]+=flowTrace 
			#####stream loop maintenence#############
			rWalk+=r
			cWalk+=c
			##################################
print 'finished traversal'
#convert to raster
new_raster = arcpy.NumPyArrayToRaster(flowAccumulation,corner,xCellSize,yCellSize)
print 'Raster of classes created'
# Setting output raster spatial reference and save it
arcpy.DefineProjection_management(new_raster, spatial_ref)
print 'Projection Defined'
new_raster.save(workspace+outRaster)
print 'Raster saved to workspace'
arcpy.CheckInExtension("Spatial")
print 'Spatial Checked In.'	
print 'program run done. Discarded resources destroyed.'		
stop = datetime.datetime.now()
dt = (stop - start)/3600
print 'program was started at '+str(start.strftime('%Y-%m-%d %H:%M:%S'))
#stop conditions,time and delta time
print 'program ending at '+str(stop.strftime('%Y-%m-%d %H:%M:%S'))
print 'run time (hours) is '+str(dt)+' hours'
