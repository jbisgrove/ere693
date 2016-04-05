# things to do
# add filename information to raster write line
# get rid of redunancy of print when running command line
fileAppendix='_JB3_10'
rain=False  #set to 0 for rain on cell not included, 1 to include
noEdge=False
runBmp=True
inRaster = 'flowDirectionVerySmall'
accumulationRaster = 'flowAccumVerySmall'
outRaster = 'flowAdjustmentVerySmallPy'
bmpRaster = 'BMP_Points_Raster_Very_Small2'
outRaster+=fileAppendix	
outRaster+='Bmp'
##the loop messages should all be written only to console and without new lines
##this limits the number of lines to one without cursor controls
##the command is such as
##sys.stdout.write('%s'%'something')
##sys.stdout.write('\r%s'%'else')
#john bisgrove
#ERE 693
#Lab 5
#23 Feb 2016
# Tansverse Walk without nonbranched retracings
# believed to be invention jb3 herein demonstrated

# import library packages

import arcpy, os, sys, numpy
from arcpy import env
from arcpy.sa import *
import d8
from d8 import printline,printError,Outlet,Source
#start conditions and time
start = datetime.datetime.now()
print 'program has started at ',start
#-----------------------------------------
print ("D8 Modification Routines Copyright (C) 2016  John Bisgrove" 
"This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'."
"This is free software, and you are welcome to redistribute it"
"under certain conditions; type `show c' for details.")

printline('Modified Flow Adjustment using flow control raster cells as stream walk initiation cells : Program Started')
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

printline('flow direction : '+inRaster+' bmp : '+bmpRaster+' flow accumulation '+outRaster)
# set environment
drive = 'J'
directory = ':/ESF/Classes/ERE693/Lab05/'
db = 'Lab05Geodatabase.gdb/'
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
bmps = arcpy.RasterToNumPyArray(bmpRaster,nodata_to_value=0)
	#print 'bmps rows, columns ',bmps.shape[0],bmps.shape[1]
flowDirection = arcpy.RasterToNumPyArray(inRaster)
flowAccumulation = arcpy.RasterToNumPyArray(accumulationRaster)
rows = flowDirection.shape[0]
columns = flowDirection.shape[1]
printline( 'flowDirection rows: '+str(rows) +' columns: '+str(columns) )

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
	
#different-------------------	
		#test to prohibit artificial entry into retrace : CONTINUE
		if bmps[row][column]==0:
			continue
			print 'never prints'
#----------------------------		
		rWalk = row
		cWalk = column
		newTrace = True
		flowAdj = 0
		bmp = bmps[row][column]
		
		print 'row column bmp = ',row,column,bmp
		stream = True
		while stream:
			r,c =Outlet(flowDirection[rWalk][cWalk])
			if (rWalk+r) < 0 or (rWalk+r) >= rows or (cWalk+c) < 0 or (cWalk+c) >= columns :
				stream = False
			if not stream:
				break
			if newTrace:
				flowAdj = ((flowAccumulation[rWalk][cWalk])+1) * bmp
				print 'rWalk cWalk flowAccumulation flowAdj = ',rWalk, cWalk, flowAccumulation[rWalk][cWalk] ,flowAdj
				newTrace=False
			
			flowAccumulation[rWalk+r][cWalk+c]-=flowAdj

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
