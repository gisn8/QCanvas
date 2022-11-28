""" 
Resources: 
https://docs.qgis.org/3.22/en/docs/pyqgis_developer_cookbook/canvas.html
https://gis.stackexchange.com/questions/402007/qgsmapcanvas-set-layers-not-showing-any-layers
"""
import sys

from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from qgis.PyQt.QtGui import QColor

from qgis.core import QgsVectorLayer
from qgis.gui import QgsMapCanvas



class Canvas_Dlg(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
	
	
	def initUI(self):
		self.setWindowTitle('Standalone Map Canvas')  
		
		self.layout = self.set_layout()
		
		self.setLayout(self.layout)
		
		self.show()
		
	def import_vlayer(self):
		path_to_gpkg = '/home/nathan/working.gpkg'
		# append the layername part
		gpkg_layer = path_to_gpkg + "|layername=corps"
		self.vlayer = QgsVectorLayer(gpkg_layer, "corps", "ogr")
		# Optional; will set to random color otherwise
		# self.vlayer.renderer().symbol().setColor(QColor("blue"))
		
		return self.vlayer
		
	def setup_canvas(self):
		self.canvas = QgsMapCanvas()
		
		# set extent to the extent of our layer
		self.vlayer = self.import_vlayer()
		# print(self.vlayer.extent())
		self.canvas.setExtent(self.vlayer.extent())
		self.canvas.zoomScale(self.canvas.scale()*1.1) # zooms out 10% from strict extent
		
		# print(self.vlayer.crs())
		self.canvas.setDestinationCrs(self.vlayer.crs())
		# print(self.canvas.mapSettings().destinationCrs())
		
		# set the map canvas layer set
		self.canvas.setLayers([self.vlayer])
		self.canvas.show()
		
		self.canvas.refreshAllLayers()
		
		return self.canvas

	
	def set_layout(self):
		self.vbox_main = QVBoxLayout()
		
		self.canvas = self.setup_canvas()
		print(self.canvas.scale()) # Showing in case we want to set labels etc to canvas properties. Likely need to import QgsMapMouseEvent if we want refreshed
		
		self.vbox_main.addWidget(self.canvas)
		
		return self.vbox_main


if __name__ == '__main__':
	app = QApplication(sys.argv)
	frame = Canvas_Dlg()
	sys.exit(app.exec_())
