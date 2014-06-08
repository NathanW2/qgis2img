from PyQt4.QtXml import QDomDocument

from qgis.gui import QgsMapCanvasLayer
from qgis.core import (
    QgsVectorLayer,
    QgsRasterLayer,
    QgsMapLayerRegistry,
    QgsMapSettings)


def iterate_nodes(nodes):
    for index in xrange(nodes.length()):
        yield nodes.at(index).toElement()


class ProjectParser(object):
    def __init__(self, xmldoc):
        self.doc = xmldoc

    @classmethod
    def from_file(cls, filename):
        xml = open(filename).read()
        doc = QDomDocument()
        doc.setContent(xml)
        return cls(doc)

    @staticmethod
    def _create_layer(self, node):
        layer_type = node.attribute('type')
        if layer_type == "vector":
            layer = QgsVectorLayer()
        elif layer_type == "raster":
            layer = QgsRasterLayer()
        else:
            return None
        layer.readLayerXML(node)
        return layer.id(), layer

    def create_layers(self):
        """
        Get all configured canvas layers in the project
        """
        layers = QgsMapLayerRegistry.instance().mapLayers()

        def make_layer(layer_id, visible_flag):
            try:
                layer = layers[layer_id]
            except KeyError:
                return None
            return QgsMapCanvasLayer(layer, visible_flag)

        layer_set = [
            make_layer(layerid, visible) for layerid, visible in self.layers()]
        layer_set = filter(None, layer_set)
        return layer_set

    @property
    def canvas_node(self):
        nodes = self.doc.elementsByTagName("mapcanvas")
        return nodes.at(0)

    @staticmethod
    def _get_layer(node):
        file_list = node.elementsByTagName("legendlayerfile")
        layer_file = file_list.at(0).toElement()
        layer_id = layer_file.attribute('layer_id')
        visible = int(layer_file.attribute('visible'))
        return layer_id, bool(visible)

    def map_layers(self):
        layer_nodes = self.doc.elementsByTagName("maplayer")
        return (self._create_layer(elm) for elm in iterate_nodes(layer_nodes))

    def layers(self):
        legend_nodes = self.doc.elementsByTagName("legendlayer")
        return (self._get_layer(elm) for elm in iterate_nodes(legend_nodes))

    def settings(self):
        canvas_nodes = self.doc.elementsByTagName("mapcanvas")
        node = canvas_nodes.at(0).toElement()
        settings = QgsMapSettings()
        settings.readXML(node)
        return settings

    def visible_layers(self):
        legend_nodes = self.doc.elementsByTagName("legendlayer")
        layers = (self._get_layer(elm) for elm in iterate_nodes(legend_nodes))
        for legend_id, visible in layers:
            if visible:
                yield legend_id

