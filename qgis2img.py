import os

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
        results.append("Layer: {0} {1:>10} sec".format(layer.name(), (float(sum(timings)) / len(timings)) / 1000))
    print "\n".join(results)

def main(app, projectfile, imagesize, passes):
    global size
    global renderpasses

    size = QSize(imagesize[0], imagesize[1])
    renderpasses = passes

    QgsProject.instance().readProject.connect(read_project)
    QDir.setCurrent(os.path.dirname(projectfile))
    fileinfo = QFileInfo(projectfile)
    QgsProject.instance().read(fileinfo)
