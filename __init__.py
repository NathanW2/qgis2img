from __future__ import division
import os
import argparse

from qgisapp import qgisapp
from qgis.core import QgsProviderRegistry, QgsMapLayerRegistry, QgsProject, QgsMapSettings, \
                      QgsMapRendererParallelJob, QgsMapRendererSequentialJob

from PyQt4.QtCore import QDir, QFileInfo, QSize

curr_path = os.path.dirname(os.path.abspath(__file__))
imagepath = os.path.join(curr_path, 'images')

def render_images(layers):
    for layerid, layer in layers.iteritems():
        timings = []
        for i in range(renderpasses):
            timings.append(render_layer(layer))
        yield layer, timings

def render_layer(layer):
    settings = QgsMapSettings()
    settings.setOutputSize(size)
    settings.setLayers([layer.id()])
    settings.setExtent(settings.fullExtent())
    job = QgsMapRendererParallelJob(settings)
    #job = QgsMapRendererSequentialJob(settings)
    job.start()
    job.waitForFinished()
    image = job.renderedImage()
    if not os.path.exists(imagepath):
        os.mkdir(imagepath)
    image.save(os.path.join(imagepath, layer.name() + '.png'))
    return job.renderingTime()

def read_project(doc):
    layers = QgsMapLayerRegistry.instance().mapLayers()
    print "Project Loaded with:", [layer.name() for layer in layers.values()]
    print "Rendering images with {0} passes".format(renderpasses)
    print_stats(render_images(layers))

def print_stats(stats):
    results = []
    for layer, timings in stats:
        results.append("Layer: {0} {1:>10} sec".format(layer.name(), (sum(timings) / len(timings)) / 1000))
    print "\n".join(results)

def main(app, projectfile):
    QgsProject.instance().readProject.connect(read_project)
    QDir.setCurrent(os.path.dirname(projectfile))
    fileinfo = QFileInfo(projectfile)
    QgsProject.instance().read(fileinfo)

if __name__ == "__main__":
    global size
    global renderpasses

    parser = argparse.ArgumentParser(description="Benchmark QGIS project file and layer loading times")
    parser.add_argument('--project', dest='project', help="Project file to load into QGIS")
    parser.add_argument('--size', dest='size', default='1580x906', help="Image output size")
    parser.add_argument('--passes', dest='passes', type=int, default=3, help="Number of render passes per layer")
    args = parser.parse_args()

    if not args.project:
        parser.print_help()
        parser.exit()

    width, height = args.size.split('x')
    size = QSize(int(width), int(height))

    renderpasses = args.passes

    # Good to go
    with qgisapp(guienabled=False) as app:
        main(app, args.project)
