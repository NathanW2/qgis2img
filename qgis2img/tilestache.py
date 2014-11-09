from PIL import Image

from qgis.core import QgsMapSettings, QgsRectangle, QgsMapRendererParallelJob, QgsCoordinateReferenceSystem, QgsMapRendererSequentialJob
from qgis.core.contextmanagers import qgisapp

from PyQt4.QtGui import QImage
from PyQt4.QtCore import QBuffer, QIODevice, QSize

from qgis2img import projectparser

qgis = None
project = None

class Output:
    def __init__(self, content):
        self.content = content

    def save(self, out, format):
        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        self.content.save(buffer, "PNG")
        out.write(buffer.data())
        buffer.close()

class Provider:
    def __init__(self, layer, projectfile):
        self.layer = layer
        self.projectfile = projectfile
        self.project = None

    def renderArea(self, width, height, srs, xmin, ymin, xmax, ymax, zoom):
        print width, height, srs, xmin, ymin, xmax, ymax, zoom
        global qgis
        if not qgis:
            qgis = qgisapp(guienabled=False, sysexit=False).__enter__()

        global project
        if not project:
            project = projectparser.Project.fromFile(self.projectfile)

        layer = project.maplayers()[0]
        print "VALID", layer.isValid()

        # settings = project.settings()

        settings = QgsMapSettings()
        crs = QgsCoordinateReferenceSystem()
        crs.createFromSrid(3857)
        settings.setDestinationCrs(crs)
        settings.setCrsTransformEnabled(True)
        extents = QgsRectangle(xmin, ymin, xmax, ymax)
        settings.setExtent(extents)
        settings.setOutputSize(QSize(width, height))
        print settings.destinationCrs().authid()
        print extents.toString()
        projectids = [layer.id() for layer in project.visiblelayers()]
        settings.setLayers(projectids)

        # job = QgsMapRendererParallelJob(settings)
        job = QgsMapRendererSequentialJob(settings)
        job.start()
        job.waitForFinished()
        image = job.renderedImage()
        return Output(image)

    def getTypeByExtension(self, extension):
        if extension.lower() == "png":
            return "application/png", "png"
        else:
            raise ValueError(extension)