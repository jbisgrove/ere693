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



#user assigned variables
inRaster = 'flowDirectionVerySmall'
accumulationRaster = 'flowAccumVerySmall'
outRaster = 'BMP_Points_Raster_Very_Small2'
# set environment variables
drive = 'J'
directory = ':/ESF/Classes/ERE693/Lab05/'
db = 'Lab05Geodatabase.gdb/'
# to set locations and loss fractions please see line ~60 below.
# bmps[row][column]=loss fraction

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


printline('build bmp')
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

	#print 'bmps rows, columns ',bmps.shape[0],bmps.shape[1]
flowDirection = arcpy.RasterToNumPyArray(inRaster)
rows = flowDirection.shape[0]
columns = flowDirection.shape[1]
bmps = numpy.zeros([rows,columns],dtype='float32')
printline( 'flowDirection rows: '+str(rows) +' columns: '+str(columns) )
bmps[10][23]=0.05
bmps[17][38]=0.10
# process (loop through) datasets

#convert to raster
new_raster = arcpy.NumPyArrayToRaster(bmps,corner,xCellSize,yCellSize)
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
