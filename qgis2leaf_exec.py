# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgis2leaf
                                 A QGIS plugin
 QGIS to Leaflet creation programm
                             -------------------
        begin                : 2014-04-29
        copyright            : (C) 2013 by Riccardo Klinger
        email                : riccardo.klinger@geolicious.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import QFileInfo
import osgeo.ogr, osgeo.osr #we will need some packages
from osgeo import ogr
from osgeo import gdal
import processing
import shutil
from qgis.core import *
import qgis.utils
import os #for file writing/folder actions
import shutil #for reverse removing directories
import urllib # to get files from the web
import time
import tempfile
import re
import fileinput
import webbrowser #to open the made map directly in your browser
import sys #to use another print command without annoying newline characters 


def layerstyle_single(layer):
	return color_code

def qgis2leaf_exec(outputProjectFileName, basemapName, basemapMeta, basemapAddress, width, height, extent, full, layer_list, visible, opacity_raster, encode2JSON, cluster_set, webpage_name, webmap_head,webmap_subhead, legend, locate, address):
	# supply path to where is your qgis installed
	#QgsApplication.setPrefixPath("/path/to/qgis/installation", True)

	pluginDir = os.path.dirname(os.path.realpath(__file__))
	
	cluster_num = 1
	# load providers
	QgsApplication.initQgis()
	# let's determine the current work folder of qgis:
	print os.getcwd()		
	print layer_list
	# let's create the overall folder structure:
	outputProjectFileName = os.path.join(outputProjectFileName, 'export_' + str(time.strftime("%Y_%m_%d")) + '_' + str(time.strftime("%I_%M_%S")))
	jsStore = os.path.join(os.getcwd(),outputProjectFileName, 'js')
	os.makedirs(jsStore)
	shutil.copyfile(pluginDir + os.sep + 'js' + os.sep + 'Autolinker.min.js', jsStore + os.sep + 'Autolinker.min.js')
	shutil.copyfile(pluginDir + os.sep + 'js' + os.sep + 'leaflet.markercluster.js', jsStore + os.sep + 'leaflet.markercluster.js')
	dataStore = os.path.join(os.getcwd(),outputProjectFileName, 'data')
	os.makedirs(dataStore)
	cssStore = os.path.join(os.getcwd(),outputProjectFileName, 'css')
	os.makedirs(cssStore)
	shutil.copyfile(pluginDir + os.sep + 'css' + os.sep + 'MarkerCluster.css', cssStore + os.sep + 'MarkerCluster.css')
	shutil.copyfile(pluginDir + os.sep + 'css' + os.sep + 'MarkerCluster.Default.css', cssStore + os.sep + 'MarkerCluster.Default.css')
	picturesStore = os.path.join(os.getcwd(),outputProjectFileName, 'pictures')
	os.makedirs(picturesStore)
	miscStore = os.path.join(os.getcwd(),outputProjectFileName, 'misc')
	os.makedirs(miscStore)
	#lets create a css file for own css:
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'css' + os.sep + 'own_style.css', 'w') as f_css:
		if full == 1:
			text = """
<style>
	body {
		padding: 0;
		margin: 0;
	}
	html, body, #map {
		height: 100%;
		width: 100%;
		padding: 0;
		margin: 0;
	}
	th {
		text-align: left;
		vertical-align: top;
	}
"""
		elif full == 0:
			text = """
<style>
	body {
		padding: 0;
		margin: 0;
	}
	html, body, #map {
		height: """+str(height)+"""px;
		width: """+str(width)+"""px;
	}
	th {
		text-align: left;
		vertical-align: top;
	}
"""
		if opacity_raster == True and full == 1:
			text += """
	html, body, #slide {
		width: 100%;
		padding: 0;
		margin: 0;
	}
"""
		elif opacity_raster == True and full== 0:
			text += """	
		html, body, #slide {
		width: """+str(width)+"""px;
		padding: 0;
		margin: 0;
	}

"""
		elif opacity_raster == False:
			text += """
		"""
		text += """
		.info {
    padding: 6px 8px;
    font: 14px/16px Arial, Helvetica, sans-serif;
    background: white;
    background: rgba(255,255,255,0.8);
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    border-radius: 5px;
        }
    .info h2 {
    margin: 0 0 5px;
    color: #777;
}
</style>"""
		f_css.write(text)
		f_css.close()
	
	#the index file has an easy beginning. we will store it right away:
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'w') as f_html:
		base = """
<!DOCTYPE html>
<html>
<head> """
		if webpage_name == "":
			base +="""
	<title>QGIS2leaf webmap</title>
	"""
		else:
			base +="""
	<title>""" + (webpage_name).encode('utf-8') + """</title>
	"""
		base += """
	<meta charset="utf-8" />
	<link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.2/leaflet.css" /> <!-- we will us e this as the styling script for our webmap-->
	<link rel="stylesheet" href="css/MarkerCluster.css" />
	<link rel="stylesheet" href="css/MarkerCluster.Default.css" />
	<link rel="stylesheet" type="text/css" href="css/own_style.css">"""
		if address == True:
			base += """
        <link rel="stylesheet" href="http://k4r573n.github.io/leaflet-control-osm-geocoder/Control.OSMGeocoder.css" />	"""
		base +="""
	<script src="http://code.jquery.com/jquery-1.11.1.min.js"></script> <!-- this is the javascript file that does the magic-->
	<script src="js/Autolinker.min.js"></script>"""
		if full == 1:
			base +="""
	<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />"""
		base += """
</head>
<body>
	<div id="map"></div> <!-- this is the initial look of the map. in most cases it is done externally using something like a map.css stylesheet were you can specify the look of map elements, like background color tables and so on.-->
	<script src="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.2/leaflet.js"></script> <!-- this is the javascript file that does the magic-->"""
		if address == True:
			
			base +="""
	<script src="http://k4r573n.github.io/leaflet-control-osm-geocoder/Control.OSMGeocoder.js"></script>"""
		base +="""
	<script src="js/leaflet.markercluster.js"></script>
	"""
		if opacity_raster == True:
			base += """<input id="slide" type="range" min="0" max="1" step="0.1" value="1" onchange="updateOpacity(this.value)">"""
  		f_html.write(base)
		f_html.close()
	# let's create the js files in the data folder of input vector files:
	canvas = qgis.utils.iface.mapCanvas()
	allLayers = canvas.layers()
	exp_crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
	for i in allLayers: 
		for j in layer_list:
			if re.sub('[\W_]+', '', i.name()) == re.sub('[\W_]+', '', j):
				if i.providerType() != 'WFS' or encode2JSON == True and i:
					if i.type() ==0:
						qgis.core.QgsVectorFileWriter.writeAsVectorFormat(i,dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js', 'utf-8', exp_crs, 'GeoJson')
						#now change the data structure to work with leaflet:

						with open(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js', "r+") as f2:
							old = f2.read() # read everything in the file
							f2.seek(0) # rewind
							f2.write("var exp_" + str(re.sub('[\W_]+', '', i.name())) + " = " + old) # write the new line before
							f2.close
						#let's define style for the single marker points
						if i.rendererV2().dump()[0:6] == 'SINGLE' and i.geometryType() == 0:
							color_str = str(i.rendererV2().symbol().color().name())
							radius_str = str(i.rendererV2().symbol().size() * 2)
							transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
							transp_str2 = str(i.rendererV2().symbol().alpha())
							for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
								line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "color_qgis2leaf": '""" + color_str + """', "radius_qgis2leaf": """ + radius_str + """, "transp_qgis2leaf": """ + transp_str + """, "transp_fill_qgis2leaf": """ + transp_str2 + """, """ )
								sys.stdout.write(line)
						#let's define style for the single marker lines
						if i.rendererV2().dump()[0:6] == 'SINGLE' and i.geometryType() == 1:
							color_str = str(i.rendererV2().symbol().color().name())
							radius_str = str(i.rendererV2().symbol().width() * 5)
							transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
							transp_str2 = str(i.rendererV2().symbol().alpha())
							for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
								line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "color_qgis2leaf": '""" + color_str + """', "radius_qgis2leaf": """ + radius_str + """, "transp_qgis2leaf": """ + transp_str + """, "transp_fill_qgis2leaf": """ + transp_str2 + """, """ )
								sys.stdout.write(line)
						#let's define style for the single marker polygons
						if i.rendererV2().dump()[0:6] == 'SINGLE' and i.geometryType() == 2:
							if i.rendererV2().symbol().symbolLayer(0).layerType() == 'SimpleLine':
								color_str = 'none'
								borderColor_str = str(i.rendererV2().symbol().color().name())
								radius_str = str(i.rendererV2().symbol().symbolLayer(0).width() * 5)
							else:
								color_str = str(i.rendererV2().symbol().color().name())
								borderColor_str = str(i.rendererV2().symbol().symbolLayer(0).borderColor().name())
								radius_str = str(i.rendererV2().symbol().symbolLayer(0).borderWidth() * 5)
							transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
							transp_str2 = str(i.rendererV2().symbol().alpha())
							for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
								line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "color_qgis2leaf": '""" + color_str + """', "border_color_qgis2leaf": '""" + borderColor_str + """', "radius_qgis2leaf": """ + radius_str + """, "transp_qgis2leaf": """ + transp_str + """, "transp_fill_qgis2leaf": """ + transp_str2 + """, """ )
								sys.stdout.write(line)		
						#let's define style for categorized points
						if i.rendererV2().dump()[0:11] == 'CATEGORIZED' and i.geometryType() == 0:
							iter = i.getFeatures()
							provider = i.dataProvider()
							attrvalindex = provider.fieldNameIndex(i.rendererV2().classAttribute())
							categories = i.rendererV2().categories()
							color_str = []
							radius_str = []
							transp_str2 = []
							transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
							for feat in iter:
								fid = feat.id()
								attribute_map = feat.attributes()
								catindex = i.rendererV2().categoryIndexForValue(unicode(attribute_map[attrvalindex]))
								if catindex != -1: 
									color_str.append(str(categories[catindex].symbol().color().name()))
									radius_str.append(str(categories[catindex].symbol().size() * 2))
									transp_str2.append(str(categories[catindex].symbol().alpha()))
								else: 
									color_str.append('#FF00FF')
									radius_str.append('4')
									transp_str2.append('1')
							qgisLeafId = 0
							for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
								addOne = str(line).count(""""type": "Feature", "properties": { """)
								if qgisLeafId < len(color_str):
									line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "id_qgis2leaf": """ + str(qgisLeafId) + """, "color_qgis2leaf": '""" + str(color_str[qgisLeafId]) + """', "radius_qgis2leaf": """ + str(radius_str[qgisLeafId]) + """, "transp_qgis2leaf": """ + str(transp_str) + """, "transp_fill_qgis2leaf": """ + str(transp_str2[qgisLeafId]) + """, """ )
								else:
									line = line.replace(" "," ")
								sys.stdout.write(line)
								qgisLeafId = qgisLeafId+addOne
							
						#let's define style for categorized lines
						if i.rendererV2().dump()[0:11] == 'CATEGORIZED' and i.geometryType() == 1:
							iter = i.getFeatures()
							provider = i.dataProvider()
							attrvalindex = provider.fieldNameIndex(i.rendererV2().classAttribute())
							categories = i.rendererV2().categories()
							color_str = []
							radius_str = []
							transp_str2 = []
							transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
							for feat in iter:
								fid = feat.id()
								attribute_map = feat.attributes()
								catindex = i.rendererV2().categoryIndexForValue(unicode(attribute_map[attrvalindex]))
								if catindex != -1: 
									color_str.append(str(categories[catindex].symbol().color().name()))
									radius_str.append(str(categories[catindex].symbol().width() * 5))
									transp_str2.append(str(categories[catindex].symbol().alpha()))
								else: 
									color_str.append('#FF00FF')
									radius_str.append('4')
									transp_str2.append('1')
							qgisLeafId = 0
							for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
								addOne = str(line).count(""""type": "Feature", "properties": { """)
								if qgisLeafId < len(color_str):
									line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "id_qgis2leaf": """ + str(qgisLeafId) + """, "color_qgis2leaf": '""" + str(color_str[qgisLeafId]) + """', "radius_qgis2leaf": """ + str(radius_str[qgisLeafId]) + """, "transp_qgis2leaf": """ + str(transp_str) + """, "transp_fill_qgis2leaf": """ + str(transp_str2[qgisLeafId]) + """, """ )
								else:
									line = line.replace(" "," ")
								sys.stdout.write(line)
								qgisLeafId = qgisLeafId+addOne
						#let's define style for categorized polygons
						if i.rendererV2().dump()[0:11] == 'CATEGORIZED' and i.geometryType() == 2:
							iter = i.getFeatures()
							provider = i.dataProvider()
							attrvalindex = provider.fieldNameIndex(i.rendererV2().classAttribute())
							categories = i.rendererV2().categories()
							color_str = []
							radius_str = []
							transp_str2 = []
							transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
							for feat in iter:
								fid = feat.id()
								attribute_map = feat.attributes()
								catindex = i.rendererV2().categoryIndexForValue(unicode(attribute_map[attrvalindex]))
								if catindex != -1: 
									color_str.append(str(categories[catindex].symbol().color().name()))
									transp_str2.append(str(categories[catindex].symbol().alpha()))
								else: 
									color_str.append('#FF00FF')
									transp_str2.append('1')
							qgisLeafId = 0
							for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
								addOne = str(line).count(""""type": "Feature", "properties": { """)
								if qgisLeafId < len(color_str):
									line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "id_qgis2leaf": """ + str(qgisLeafId) + """, "color_qgis2leaf": '""" + str(color_str[qgisLeafId]) + """', "transp_qgis2leaf": """ + str(transp_str) + """, "transp_fill_qgis2leaf": """ + str(transp_str2[qgisLeafId]) + """, """ )
								else:
									line = line.replace(" "," ")
								sys.stdout.write(line)
								qgisLeafId = qgisLeafId+addOne	
						#let's define style for the graduaded marker points
						if i.rendererV2().dump()[0:9] == 'GRADUATED' and i.geometryType() == 0:
							# every json entry needs a unique id:
							iter = i.getFeatures()
							#what is the value based on:
							provider = i.dataProvider()
							attrvalindex = provider.fieldNameIndex(i.rendererV2().classAttribute())	
							transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
							color_str = []
							radius_str = []
							transp_str2 = []
							for feat in iter:
								if str(feat.attributes()[attrvalindex]) != 'NULL':
									value = feat.attributes()[attrvalindex]
								elif str(feat.attributes()[attrvalindex]) == 'NULL':
									value = None
								for r in i.rendererV2().ranges():
									if value >= r.lowerValue() and value <= r.upperValue() and value != None:
										color_str.append(str(r.symbol().color().name()))
										radius_str.append(str(r.symbol().size() * 2))
										transp_str2.append(str(r.symbol().alpha()))
										break
									elif value == None:
										color_str.append('#FF00FF')
										radius_str.append('4')
										transp_str2.append('1')
										break
							qgisLeafId = 0
							for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
								addOne = str(line).count(""""type": "Feature", "properties": { """)
								if qgisLeafId < len(color_str):
									line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "id_qgis2leaf": """ + str(qgisLeafId) + """, "color_qgis2leaf": '""" + str(color_str[qgisLeafId]) + """', "radius_qgis2leaf": """ + str(radius_str[qgisLeafId]) + """, "transp_qgis2leaf": """ + str(transp_str) + """, "transp_fill_qgis2leaf": """ + str(transp_str2[qgisLeafId]) + """, """ )
								else:
									line = line.replace(" "," ")
								sys.stdout.write(line)
								qgisLeafId = qgisLeafId+addOne
								
						#let's define style for the graduaded marker line
						if i.rendererV2().dump()[0:9] == 'GRADUATED' and i.geometryType() == 1:
							# every json entry needs a unique id:
							iter = i.getFeatures()
							#what is the value based on:
							provider = i.dataProvider()
							attrvalindex = provider.fieldNameIndex(i.rendererV2().classAttribute())	
							transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
							color_str = []
							radius_str = []
							transp_str2 = []
							for feat in iter:
								if str(feat.attributes()[attrvalindex]) != 'NULL':
									value = feat.attributes()[attrvalindex]
								elif str(feat.attributes()[attrvalindex]) == 'NULL':
									value = None
								for r in i.rendererV2().ranges():
									if value >= r.lowerValue() and value <= r.upperValue() and value != None:
										color_str.append(str(r.symbol().color().name()))
										radius_str.append(str(r.symbol().width() * 5))
										transp_str2.append(str(r.symbol().alpha()))
										break
									elif value == None:
										color_str.append('#FF00FF')
										radius_str.append('4')
										transp_str2.append('1')
										break
							qgisLeafId = 0
							for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
								addOne = str(line).count(""""type": "Feature", "properties": { """)
								if qgisLeafId < len(color_str):
									line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "id_qgis2leaf": """ + str(qgisLeafId) + """, "color_qgis2leaf": '""" + str(color_str[qgisLeafId]) + """', "radius_qgis2leaf": """ + str(radius_str[qgisLeafId]) + """, "transp_qgis2leaf": """ + str(transp_str) + """, "transp_fill_qgis2leaf": """ + str(transp_str2[qgisLeafId]) + """, """ )
								else:
									line = line.replace(" "," ")
								sys.stdout.write(line)
								qgisLeafId = qgisLeafId+addOne
						#let's define style for the graduaded marker polygon
						if i.rendererV2().dump()[0:9] == 'GRADUATED' and i.geometryType() == 2:
							# every json entry needs a unique id:
							iter = i.getFeatures()
							#what is the value based on:
							provider = i.dataProvider()
							attrvalindex = provider.fieldNameIndex(i.rendererV2().classAttribute())	
							transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
							color_str = []
							radius_str = []
							transp_str2 = []
							for feat in iter:
								if str(feat.attributes()[attrvalindex]) != 'NULL':
									value = feat.attributes()[attrvalindex]
								elif str(feat.attributes()[attrvalindex]) == 'NULL':
									value = None
								for r in i.rendererV2().ranges():
									if value >= r.lowerValue() and value <= r.upperValue() and value != None:
										color_str.append(str(r.symbol().color().name()))
										transp_str2.append(str(r.symbol().alpha()))
										break
									elif value == None:
										color_str.append('#FF00FF')
										transp_str2.append('1')
										break
							qgisLeafId = 0
							for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
								addOne = str(line).count(""""type": "Feature", "properties": { """)
								if qgisLeafId < len(color_str):
									line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "id_qgis2leaf": """ + str(qgisLeafId) + """, "color_qgis2leaf": '""" + str(color_str[qgisLeafId]) + """', "transp_qgis2leaf": """ + str(transp_str) + """, "transp_fill_qgis2leaf": """ + str(transp_str2[qgisLeafId]) + """, """ )
								else:
									line = line.replace(" "," ")
								sys.stdout.write(line)
								qgisLeafId = qgisLeafId+addOne						
							
						#now add the js files as data input for our map
						with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f3:
							new_src = """
				<script src='""" + 'data' + """/exp_""" + re.sub('[\W_]+', '', i.name()) + """.js' ></script>
				"""
							# store everything in the file
							f3.write(new_src)
							f3.close()
					#here comes the raster layers. you need an installed version of gdal
					elif i.type() == 1:
						in_raster = str(i.dataProvider().dataSourceUri())
						prov_raster = tempfile.gettempdir() + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + 'prov.tif'
						out_raster = dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.jpg'

						if str(i.dataProvider().metadata()[0:4]) == 'JPEG' and str(i.crs().authid()) == 'EPSG:4326':
							shutil.copyfile(in_raster+".aux.xml", out_raster + ".aux.xml")
							shutil.copyfile(in_raster, out_raster)
						else:
							processing.runalg("gdalogr:warpreproject",str(in_raster),str(i.crs().authid()),"EPSG:4326",0,1,"",prov_raster)
							format = "jpeg"
							driver = gdal.GetDriverByName( format )
							src_ds = gdal.Open(prov_raster)
							dst_ds = driver.CreateCopy( out_raster, src_ds, 0 ) 
							dst_ds = None #free the dataset	
							src_ds = None #free the dataset				
							#ret = subprocess.check_call(['gdal_translate -of jpeg -outsize 100% 100% -a_srs EPSG:4326 ' + filename_raster + " " +  out_raster_name], shell=True)
							#ret2 = subprocess.check_call(['cp ' + filename_raster + ".aux.xml " +  out_raster_name + ".aux.xml"], shell=True)

	#now determine the canvas bounding box
	#####now with viewcontrol
	if extent == 'canvas extent':
		pt0	= canvas.extent()
		crsSrc = qgis.utils.iface.mapCanvas().mapRenderer().destinationCrs()    # WGS 84
		crsDest = QgsCoordinateReferenceSystem(4326)  # WGS 84 / UTM zone 33N
		xform = QgsCoordinateTransform(crsSrc, crsDest)
		pt1 = xform.transform(pt0)
		bbox_canvas = [pt1.yMinimum(), pt1.yMaximum(),pt1.xMinimum(), pt1.xMaximum()]
		bounds = '[[' + str(pt1.yMinimum()) + ',' + str(pt1.xMinimum()) + '],[' + str(pt1.yMaximum()) + ',' + str(pt1.xMaximum()) +']]'
		middle = """
	<script>
		var map = L.map('map', { zoomControl:true }).fitBounds(""" + bounds + """);
		var additional_attrib = 'created w. <a href="https://github.com/geolicious/qgis2leaf" target ="_blank">qgis2leaf</a> by <a href="http://www.geolicious.de" target ="_blank">Geolicious</a> & contributors<br>';"""
	if extent == 'layer extent':
		middle = """
	<script>
		var map = L.map('map', { zoomControl:true });
		var additional_attrib = 'created with <a href="https://github.com/geolicious/qgis2leaf" target ="_blank">qgis2leaf</a> by <a href="http://www.geolicious.de" target ="_blank">Geolicious</a> & contributors<br>';"""
	# we will start with the clustergroup
	middle += """
	var feature_group = new L.featureGroup([]);

	var raster_group = new L.LayerGroup([]);
	"""
#here come the basemap (variants list thankfully provided by: "https://github.com/leaflet-extras/leaflet-providers") our geojsons will  looped after that
#basemap name	
	basemapText = """
	var basemap= L.tileLayer('""" + basemapAddress + """');"""
#attribution	
	basemapText += """
	map.attributionControl.addAttribution(additional_attrib + '""" + basemapMeta + """');"""
	basemapText += """	
	basemap.addTo(map);"""
	layerOrder = """	
	var layerOrder=new Array();"""
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f4:
			f4.write(middle)
			f4.write(basemapText)
			f4.write(layerOrder)
			f4.close()
	for i in reversed(allLayers): 
		for j in layer_list:
			if re.sub('[\W_]+', '', i.name()) == j:
				if i.type()==0:
					with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f5:
						#here comes the layer style
						#here comes the html popup content
						fields = i.pendingFields() 
						field_names = [field.name() for field in fields]
						html_prov = False
						icon_prov = False
						for field in field_names:
							if str(field) == 'html_exp':
								html_prov = True
								table = 'feature.properties.html_exp'
							if str(field) == 'icon_exp':
								icon_prov = True #we need this later on for icon creation
							if html_prov != True:
								tablestart = """'<table>"""
								row = ""
								for field in field_names:
									if str(field) == "icon_exp":
										row += ""
									else: 
										if i.editType(fields.indexFromName(field)) != QgsVectorLayer.Hidden:
											row += """<tr><th scope="row">""" + i.attributeDisplayName(fields.indexFromName(str(field))) + """</th><td>' + Autolinker.link(String(feature.properties.""" + str(field) + """)) + '</td></tr>"""
								tableend = """</table>'"""
								table = tablestart + row +tableend
						popFuncs = """					var popupContent = """ + table + """;
					layer.bindPopup(popupContent);
"""
						new_pop = """
				function pop_""" + re.sub('[\W_]+', '', i.name()) + """(feature, layer) {
					"""+popFuncs+"""

				}
						"""
						#single marker points:
						 
						if i.rendererV2().dump()[0:6] == 'SINGLE' and i.geometryType() == 0 and icon_prov != True:
							layerName=re.sub('[\W_]+', '', i.name())
							if i.providerType() == 'WFS' and encode2JSON == False:
								color_str = str(i.rendererV2().symbol().color().name())
								radius_str = str(i.rendererV2().symbol().size() * 2)
								transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
								transp_str2 = str(i.rendererV2().symbol().alpha())
								stylestr="""
								pointToLayer: function (feature, latlng) {  
								return L.circleMarker(latlng, {
									radius: """+radius_str+""",
									fillColor: '"""+color_str+"""',
									color: '#000',
									weight: 1,
									opacity: """+transp_str+""",
									fillOpacity: """+transp_str2+"""
									})
								},
                                onEachFeature : function (feature, layer) {
                                """+popFuncs+"""
                                }
                                """
								new_obj="""
			var """+layerName+"""URL='"""+i.source()+"""&outputFormat=text%2Fjavascript&format_options=callback%3Aget"""+layerName+"""Json';
			"""+layerName+"""URL="""+layerName+"""URL.replace(/SRSNAME\=EPSG\:\d+/, 'SRSNAME=EPSG:4326');
			var exp_"""+layerName+"""JSON = L.geoJson(null, {"""+stylestr+"""});
			layerOrder[layerOrder.length] = exp_"""+layerName+"""JSON;
			var """+layerName+"""ajax = $.ajax({
					url : """+layerName+"""URL,
					dataType : 'jsonp',
					jsonpCallback : 'get"""+layerName+"""Json',
					contentType : 'application/json',
					success : function (response) {
						L.geoJson(response, {
								onEachFeature : function (feature, layer) {
									"""+popFuncs+"""
									exp_"""+layerName+"""JSON.addData(feature)
								}
							});
						for (index = 0; index < layerOrder.length; index++) {
							feature_group.removeLayer(layerOrder[index]);feature_group.addLayer(layerOrder[index]);
						}
					}
				});
			
								"""
							else:
								new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					pointToLayer: function (feature, latlng) {  
						return L.circleMarker(latlng, {
							radius: feature.properties.radius_qgis2leaf,
							fillColor: feature.properties.color_qgis2leaf,
							color: '#000',
							weight: 1,
							opacity: feature.properties.transp_qgis2leaf,
							fillOpacity: feature.properties.transp_qgis2leaf
							})
						}
					});
				"""
#add points to the cluster group
							if cluster_set == True:
								new_obj += """
				var cluster_group"""+ re.sub('[\W_]+', '', i.name()) + """JSON= new L.MarkerClusterGroup({showCoverageOnHover: false});				
				cluster_group"""+ re.sub('[\W_]+', '', i.name()) + """JSON.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""			
								cluster_num += 1	
							elif cluster_set == False:
								new_obj += """
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				layerOrder[layerOrder.length] = exp_"""+layerName+"""JSON;
				for (index = 0; index < layerOrder.length; index++) {
					feature_group.removeLayer(layerOrder[index]);feature_group.addLayer(layerOrder[index]);
				}
				"""		
						elif i.rendererV2().dump()[0:6] == 'SINGLE' and i.geometryType() == 1:
							layerName=re.sub('[\W_]+', '', i.name())
							if i.providerType() == 'WFS' and encode2JSON == False:
								color_str = str(i.rendererV2().symbol().color().name())
								radius_str = str(i.rendererV2().symbol().width() * 5)
								transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
								transp_str2 = str(i.rendererV2().symbol().alpha())
								stylestr="""
							style: function (feature) {
								return {weight: """+radius_str+""",
										color: '"""+color_str+"""',
										opacity: """+transp_str+""",
										fillOpacity: """+transp_str2+"""};
								},
                                onEachFeature : function (feature, layer) {
									"""+popFuncs+"""
                                    }
                                    """
								new_obj="""
			var """+layerName+"""URL='"""+i.source()+"""&outputFormat=text%2Fjavascript&format_options=callback%3Aget"""+layerName+"""Json';
			"""+layerName+"""URL="""+layerName+"""URL.replace(/SRSNAME\=EPSG\:\d+/, 'SRSNAME=EPSG:4326');
			var exp_"""+layerName+"""JSON = L.geoJson(null, {"""+stylestr+"""}).addTo(map);
			layerOrder[layerOrder.length] = exp_"""+layerName+"""JSON;
			var """+layerName+"""ajax = $.ajax({
					url : """+layerName+"""URL,
					dataType : 'jsonp',
					jsonpCallback : 'get"""+layerName+"""Json',
					contentType : 'application/json',
					success : function (response) {
						L.geoJson(response, {
								onEachFeature : function (feature, layer) {
									"""+popFuncs+"""
									exp_"""+layerName+"""JSON.addData(feature)
								}
							});
						for (index = 0; index < layerOrder.length; index++) {
							map.removeLayer(layerOrder[index]);map.addLayer(layerOrder[index]);
						}
					}
				});
								"""
							else:
								new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					style: function (feature) {
						return {weight: feature.properties.radius_qgis2leaf,
								color: feature.properties.color_qgis2leaf,
								opacity: feature.properties.transp_qgis2leaf,
								fillOpacity: feature.properties.transp_qgis2leaf};
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				layerOrder[layerOrder.length] = exp_"""+layerName+"""JSON;
				for (index = 0; index < layerOrder.length; index++) {
					feature_group.removeLayer(layerOrder[index]);feature_group.addLayer(layerOrder[index]);
				}
				"""		
						elif i.rendererV2().dump()[0:6] == 'SINGLE' and i.geometryType() == 2:
							layerName=re.sub('[\W_]+', '', i.name())
							if i.providerType() == 'WFS' and encode2JSON == False:
								if i.rendererV2().symbol().symbolLayer(0).layerType() == 'SimpleLine':
									color_str = 'none'
									borderColor_str = str(i.rendererV2().symbol().color().name())
									radius_str = str(i.rendererV2().symbol().symbolLayer(0).width() * 5)
								else:
									color_str = str(i.rendererV2().symbol().color().name())
									borderColor_str = str(i.rendererV2().symbol().symbolLayer(0).borderColor().name())
									radius_str = str(i.rendererV2().symbol().symbolLayer(0).borderWidth() * 5)
								transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
								transp_str2 = str(i.rendererV2().symbol().alpha())
								stylestr="""
							style: function (feature) {
								return {color: '"""+borderColor_str+"""',
										fillColor: '"""+color_str+"""',
										weight: """+radius_str+""",
										opacity: """+transp_str+""",
										fillOpacity: """+transp_str+"""};
								},
                                onEachFeature : function (feature, layer){
                                """+popFuncs+"""
                                }
                                """
								new_obj="""
			var """+layerName+"""URL='"""+i.source()+"""&outputFormat=text%2Fjavascript&format_options=callback%3Aget"""+layerName+"""Json';
			"""+layerName+"""URL="""+layerName+"""URL.replace(/SRSNAME\=EPSG\:\d+/, 'SRSNAME=EPSG:4326');
			var exp_"""+layerName+"""JSON = L.geoJson(null, {"""+stylestr+"""}).addTo(map);
			layerOrder[layerOrder.length] = exp_"""+layerName+"""JSON;
			var """+layerName+"""ajax = $.ajax({
					url : """+layerName+"""URL,
					dataType : 'jsonp',
					jsonpCallback : 'get"""+layerName+"""Json',
					contentType : 'application/json',
					success : function (response) {
						L.geoJson(response, {
								onEachFeature : function (feature, layer) {
									"""+popFuncs+"""
									exp_"""+layerName+"""JSON.addData(feature)
								}
							});
						for (index = 0; index < layerOrder.length; index++) {
							map.removeLayer(layerOrder[index]);map.addLayer(layerOrder[index]);
						}
					}
				});
								"""
							else:
								new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					style: function (feature) {
						return {color: feature.properties.border_color_qgis2leaf,
								fillColor: feature.properties.color_qgis2leaf,
								weight: feature.properties.radius_qgis2leaf,
								opacity: feature.properties.transp_qgis2leaf,
								fillOpacity: feature.properties.transp_qgis2leaf};
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				layerOrder[layerOrder.length] = exp_"""+layerName+"""JSON;
				for (index = 0; index < layerOrder.length; index++) {
					map.removeLayer(layerOrder[index]);map.addLayer(layerOrder[index]);
				}
				"""	
						elif i.rendererV2().dump()[0:11] == 'CATEGORIZED' and i.geometryType() == 0 and icon_prov != True:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					pointToLayer: function (feature, latlng) {  
						return L.circleMarker(latlng, {
							radius: feature.properties.radius_qgis2leaf,
							fillColor: feature.properties.color_qgis2leaf,
							color: '#000',
							weight: 0.2,
							opacity: feature.properties.transp_qgis2leaf,
							fillOpacity: feature.properties.transp_qgis2leaf
							})
						}
					});
				"""
				#add points to the cluster group
							if cluster_set == True:
								
								new_obj += """
				var cluster_group"""+ re.sub('[\W_]+', '', i.name()) + """JSON= new L.MarkerClusterGroup({showCoverageOnHover: false});
				cluster_group"""+ re.sub('[\W_]+', '', i.name()) + """JSON.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""			
								cluster_num += 1	
							elif cluster_set == False:
								new_obj += """
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""		
						elif i.rendererV2().dump()[0:11] == 'CATEGORIZED' and i.geometryType() == 1:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					style: function (feature) {
						return {weight: feature.properties.radius_qgis2leaf,
								color: feature.properties.color_qgis2leaf,
								opacity: feature.properties.transp_qgis2leaf,
								fillOpacity: feature.properties.transp_qgis2leaf};
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""		
						elif i.rendererV2().dump()[0:11] == 'CATEGORIZED' and i.geometryType() == 2:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					style: function (feature) {
						return {fillColor: feature.properties.color_qgis2leaf,
								color: '#000',
								weight: 1,
								opacity: feature.properties.transp_qgis2leaf,
								fillOpacity: feature.properties.transp_qgis2leaf};
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""				
						elif i.rendererV2().dump()[0:9] == 'GRADUATED' and i.geometryType() == 0 and icon_prov != True:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					pointToLayer: function (feature, latlng) {  
						return L.circleMarker(latlng, {
							radius: feature.properties.radius_qgis2leaf,
							fillColor: feature.properties.color_qgis2leaf,
							color: '#000',
							weight: 1,
							opacity: feature.properties.transp_qgis2leaf,
							fillOpacity: feature.properties.transp_qgis2leaf
							})
						}
					});
				"""
								#add points to the cluster group
							if cluster_set == True:
								new_obj += """
				var cluster_group"""+ re.sub('[\W_]+', '', i.name()) + """JSON= new L.MarkerClusterGroup({showCoverageOnHover: false});				
				cluster_group"""+ re.sub('[\W_]+', '', i.name()) + """JSON.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""			
								cluster_num += 1	
							elif cluster_set == False:
								new_obj += """
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""	
						elif i.rendererV2().dump()[0:9] == 'GRADUATED' and i.geometryType() == 1:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					style: function (feature) {
						return {weight: feature.properties.radius_qgis2leaf,
								fillColor: feature.properties.color_qgis2leaf,
								color: '#000',
								opacity: feature.properties.transp_qgis2leaf,
								fillOpacity: feature.properties.transp_qgis2leaf};
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""	
						elif i.rendererV2().dump()[0:9] == 'GRADUATED' and i.geometryType() == 2:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					style: function (feature) {
						return {fillColor: feature.properties.color_qgis2leaf,
								color: '#000',
								weight: 1,
								opacity: feature.properties.transp_qgis2leaf,
								fillOpacity: feature.properties.transp_qgis2leaf};
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""		
						elif icon_prov == True and i.geometryType() == 0:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					pointToLayer: function (feature, latlng) {
						return L.marker(latlng, {icon: L.icon({
							iconUrl: feature.properties.icon_exp,
							iconSize:     [24, 24], // size of the icon change this to scale your icon (first coordinate is x, second y from the upper left corner of the icon)
							iconAnchor:   [12, 12], // point of the icon which will correspond to marker's location (first coordinate is x, second y from the upper left corner of the icon)
							popupAnchor:  [0, -14] // point from which the popup should open relative to the iconAnchor (first coordinate is x, second y from the upper left corner of the icon)
			 				})
			 			})
					}}
				);
				"""
				#add points to the cluster group
							if cluster_set == True:
								new_obj += """
				var cluster_group"""+ re.sub('[\W_]+', '', i.name()) + """JSON= new L.MarkerClusterGroup({showCoverageOnHover: false});
				cluster_group"""+ re.sub('[\W_]+', '', i.name()) + """JSON.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""			
								cluster_num += 1
							elif cluster_set == False:
								new_obj += """
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""		
						else:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""		
				
						# store everything in the file
						f5.write(new_pop)
						f5.write(new_obj)
						if visible == 'show all' and cluster_set == False:
							f5.write("""
						//add comment sign to hide this layer on the map in the initial view.
						exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON.addTo(map);""")
						if visible == 'show all' and cluster_set == True:
							if i.geometryType() == 0:
								f5.write("""
						//add comment sign to hide this layer on the map in the initial view.
						cluster_group"""+ re.sub('[\W_]+', '', i.name()) + """JSON.addTo(map);""")
							if i.geometryType() != 0:
								f5.write("""
						//add comment sign to hide this layer on the map in the initial view.
						exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON.addTo(map);""")
						if visible == 'show none' and cluster_set == False:
							f5.write("""
						//delete comment sign to show this layer on the map in the initial view.
						//exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON.addTo(map);""")
						if visible == 'show none' and cluster_set == True:
							if i.geometryType() == 0:
								f5.write("""
						//delete comment sign to show this layer on the map in the initial view.
						//cluster_group"""+ re.sub('[\W_]+', '', i.name()) + """JSON.addTo(map);""")
							if i.geometryType() != 0:
								f5.write("""
						//delete comment sign to show this layer on the map in the initial view.
						//exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON.addTo(map);""")
						f5.close()
				elif i.type() == 1:
					out_raster_name = 'data/' + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.jpg'
					pt2	= i.extent()
					crsSrc = i.crs()    # WGS 84
					crsDest = QgsCoordinateReferenceSystem(4326)  # WGS 84 / UTM zone 33N
					xform = QgsCoordinateTransform(crsSrc, crsDest)
					pt3 = xform.transform(pt2)
					bbox_canvas2 = [pt3.yMinimum(), pt3.yMaximum(),pt3.xMinimum(), pt3.xMaximum()]
					bounds2 = '[[' + str(pt3.yMinimum()) + ',' + str(pt3.xMinimum()) + '],[' + str(pt3.yMaximum()) + ',' + str(pt3.xMaximum()) +']]'
					with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f5_raster:
						
						new_obj = """
				var img_""" + re.sub('[\W_]+', '', i.name()) + """= '""" + out_raster_name + """';
				var img_bounds_""" + re.sub('[\W_]+', '', i.name()) + """ = """+ bounds2 + """;
				var overlay_""" + re.sub('[\W_]+', '', i.name()) + """ = new L.imageOverlay(img_""" + re.sub('[\W_]+', '', i.name()) + """, img_bounds_""" + re.sub('[\W_]+', '', i.name()) + """).addTo(map);
				raster_group.addLayer(overlay_""" + re.sub('[\W_]+', '', i.name()) + """);"""

						f5_raster.write(new_obj)
						f5_raster.close()
	


	#let's add a Title and a subtitle
	if webmap_head != "": 
		titleStart ="""
		var title = new L.Control();
		title.onAdd = function (map) {
			this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
			this.update();
			return this._div;
	    };
	    title.update = function () {
			this._div.innerHTML = '<h2>""" + webmap_head.encode('utf-8') + """</h2>""" + webmap_subhead.encode('utf-8') + """'
		};
		title.addTo(map);"""
		with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f5contr:
			f5contr.write(titleStart)
			f5contr.close()
			#here comes the address search:
	if address == True:
		address_text = """
		var osmGeocoder = new L.Control.OSMGeocoder({
            collapsed: false,
            position: 'topright',
            text: 'Find!',
			});
		osmGeocoder.addTo(map);
		"""
		with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f5addr:
			f5addr.write(address_text)
			f5addr.close()


	#let's add a legend
	if legend == True:
		legendStart = """
		var legend = L.control({position: 'bottomright'});
		
		legend.onAdd = function (map) {
		var div = L.DomUtil.create('div', 'info legend');
		div.innerHTML = "<h3>Legend</h3><table>"""
		for i in reversed(allLayers): 
			for j in layer_list:
				if re.sub('[\W_]+', '', i.name()) == j:
					if i.type() == 0:
						fields = i.pendingFields() 
						field_names = [field.name() for field in fields]
						legend_ico_prov = False
						legend_exp_prov = False
						for field in field_names:
							if str(field) == 'legend_ico':
								legend_ico_prov = True
							if str(field) == 'legend_exp':
								legend_exp_prov = True
						if legend_ico_prov == True and legend_exp_prov == True:
							iter = i.getFeatures()
							for feat in iter:
								fid = feat.id()
								provider = i.dataProvider()
								legend_ico_index = provider.fieldNameIndex('legend_ico')
								legend_exp_index = provider.fieldNameIndex('legend_exp')
								attribute_map = feat.attributes()
								legend_icon = attribute_map[legend_ico_index]
								legend_expression = attribute_map[legend_exp_index]
								print legend_expression
								print legend_icon 
								break
							legendStart += """<tr><td><img src='""" + unicode(legend_icon) + """'></img></td><td>"""+unicode(legend_expression) + """</td></tr>"""

		legendStart += """</table>";
    		return div;
		};
		legend.addTo(map);
"""
		with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f5leg:
			f5leg.write(legendStart)
			f5leg.close()

	# let's add layer control
	controlStart = """
	L.control.layers({'"""+basemapName+"""': basemap},{"""
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f6:
		f6.write(controlStart)
		f6.close()

	for i in allLayers: 
		for j in layer_list:
			if i.type() == 0:
				if re.sub('[\W_]+', '', i.name()) == re.sub('[\W_]+', '', j):
					with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f7:
						if cluster_set == False or i.geometryType() != 0:
							#new_layer = '"' + re.sub('[\W_]+', '', i.name()) + '"' + ": exp_" + re.sub('[\W_]+', '', i.name()) + """JSON,"""
							new_layer = '"' + unicode(i.name()) + '"' + ": exp_" + re.sub('[\W_]+', '', i.name()) + """JSON,"""
						if cluster_set == True and i.geometryType() == 0:
							#new_layer = '"' + re.sub('[\W_]+', '', i.name()) + '"' + ": cluster_group"""+ re.sub('[\W_]+', '', i.name()) + """JSON,"""
							new_layer = '"' + unicode(i.name()) + '"' + ": cluster_group"""+ re.sub('[\W_]+', '', i.name()) + """JSON,"""
						f7.write(new_layer)
						f7.close()
			elif i.type() == 1:
				if re.sub('[\W_]+', '', i.name()) == re.sub('[\W_]+', '', j):
					with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f7:
						#new_layer = '"' + re.sub('[\W_]+', '', i.name()) + '"' + ": overlay_" + re.sub('[\W_]+', '', i.name()) + ""","""
						new_layer = '"' + unicode(i.name()) + '"' + ": overlay_" + re.sub('[\W_]+', '', i.name()) + ""","""
						f7.write(new_layer)
						f7.close()	
	controlEnd = "},{collapsed:false}).addTo(map);"	
	


	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'rb+') as f8:
		f8.seek(-1, os.SEEK_END)
		f8.truncate()
		f8.write(controlEnd)
		f8.close()
	if opacity_raster == True:
		opacityStart = """
		function updateOpacity(value) {
		"""
		with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f9:
			f9.write(opacityStart)
			f9.close()

		for i in allLayers: 
			for j in layer_list:
				if i.type() == 1:
					if re.sub('[\W_]+', '', i.name()) == re.sub('[\W_]+', '', j):
						with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f10:
							new_opc = """
							overlay_""" + re.sub('[\W_]+', '', i.name()) + """.setOpacity(value);"""
							f10.write(new_opc)
							f10.close()	
		opacityEnd = """}"""	
		with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'rb+') as f11:
			f11.seek(-1, os.SEEK_END)
			f11.truncate()
			f11.write(opacityEnd)
			f11.close()
	elif opacity_raster == False:
		print "no opacity control added"

	#here comes the user locate:
	if locate == True:
		end = """
		map.locate({setView: true, maxZoom: 16});
		function onLocationFound(e) {
    		var radius = e.accuracy / 2;
			L.marker(e.latlng).addTo(map)
        	.bindPopup("You are within " + radius + " meters from this point").openPopup();
			L.circle(e.latlng, radius).addTo(map);
		}
		map.on('locationfound', onLocationFound);
		"""
	if locate == False:
		end = ''
	# let's close the file but ask for the extent of all layers if the user wants to show only this extent:
	if extent == 'layer extent':
		end += """
		map.fitBounds(feature_group.getBounds());
	</script>
</body>
</html>
	"""
	if extent == 'canvas extent':
		end += """
	L.control.scale({options: {position: 'bottomleft',maxWidth: 100,metric: true,imperial: false,updateWhenIdle: false}}).addTo(map);
	</script>
</body>
</html>
	"""
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f12:
		f12.write(end)
		f12.close()
	webbrowser.open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html')

