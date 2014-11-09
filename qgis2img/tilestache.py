from PIL import Image
from urlparse import urljoin, urlparse

from qgis.core import QgsMapSettings, QgsRectangle, QgsMapRendererParallelJob, QgsCoordinateReferenceSystem, QgsMapRendererSequentialJob
from qgis.core.contextmanagers import qgisapp

from PyQt4.QtGui import QImage
from PyQt4.QtCore import QBuffer, QIODevice, QSize

import qgis2img.render

loadedprojects = {}

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
        projectfile = urljoin(layer.config.dirpath, projectfile)
        scheme, h, file_path, p, q, f = urlparse(projectfile)
        self.projectfile = file_path
        self.project = None

    def renderArea(self, width, height, srs, xmin, ymin, xmax, ymax, zoom):
        # print width, height, srs, xmin, ymin, xmax, ymax, zoom
        try:
            app, project = loadedprojects[self.projectfile]
        except KeyError:
            app = qgisapp(guienabled=False, sysexit=False).__enter__()
            project, _, _, _ = qgis2img.render.read_project(self.projectfile)
            loadedprojects[self.projectfile] = (app, project)

        # settings = QgsMapSettings()
        settings = project.settings()
        crs = QgsCoordinateReferenceSystem()
        crs.createFromSrid(3857)
        settings.setDestinationCrs(crs)
        settings.setCrsTransformEnabled(True)
        extents = QgsRectangle(xmin, ymin, xmax, ymax)
        settings.setExtent(extents)
        settings.setOutputSize(QSize(width, height))
        layers = [layer.id() for layer in project.visiblelayers()]
        image, rendertime = qgis2img.render.render_layers(settings, layers, RenderType=QgsMapRendererSequentialJob)
        print "Render Time: {}ms".format(rendertime)
        return Output(image)

    # def getTypeByExtension(self, extension):
    #     if extension.lower() == "png":
    #         return "application/png", "png"
    #     else:
    #         raise ValueError(extension)