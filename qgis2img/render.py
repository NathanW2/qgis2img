import os

from qgis.core import QgsProviderRegistry, QgsMapLayerRegistry, QgsProject, QgsMapSettings, \
    QgsMapRendererParallelJob, QgsMapRendererSequentialJob

from PyQt4.QtCore import QDir, QFileInfo, QSize

curr_path = os.path.dirname(os.path.abspath(__file__))
imagepath = os.path.join(curr_path, '..', 'images')

def render_images(layers, projectlayers, settings):
    if 'layer' in rendertypes:
        for layerid, layer in layers.iteritems():
            timings = []
            for i in range(renderpasses):
                timings.append(render_layer(layer, settings))
            yield layer.name(), timings
    if 'project' in rendertypes:
        timings = []
        for i in range(renderpasses):
            timings.append(render_project(projectlayers, settings))
        yield "Project", timings

def render(name, settings):
    settings.setOutputSize(size)
    job = QgsMapRendererParallelJob(settings)
    #job = QgsMapRendererSequentialJob(settings)
    job.start()
    job.waitForFinished()
    image = job.renderedImage()
    if not os.path.exists(imagepath):
        os.mkdir(imagepath)
    image.save(os.path.join(imagepath, name + '.png'))
    return job.renderingTime()

def render_project(layers, settings):
    settings.setLayers(layers)
    return render(QgsProject.instance().title(), settings)

def render_layer(layer, settings):
    settings.setLayers([layer.id()])
    return render(layer.name(), settings)

def read_project(doc):
    layers = QgsMapLayerRegistry.instance().mapLayers()
    print "Project Loaded with:", [layer.name() for layer in layers.values()]
    print "Rendering images with {0} passes".format(renderpasses)
    import projectparser
    parser = projectparser.ProjectParser(doc)
    projectlayers = list(parser.visiblelayers())
    settings = parser.settings()
    renderimages = render_images(layers, projectlayers, settings)
    print_stats(renderimages, settings)

def print_stats(stats, settings):
    results = []
    layers = QgsMapLayerRegistry.instance().mapLayers().values()
    maxlengthname = max([len(layer.name()) for layer in layers])
    for layer, timings in stats:
        time = float(sum(timings)) / len(timings) / 1000
        results.append("Layer: {0:{maxlen}} {1:>10} sec".format(layer, time, maxlen=maxlengthname))

    width = len(max(results, key=len))
    print "{0:*^{width}}".format("Results", width=width)
    print "Scale: {}".format(settings.scale())
    print "\n".join(results)

def main(app, loadedfile, imagesize, passes, types):
    global size
    global renderpasses
    global rendertypes

    size = QSize(imagesize[0], imagesize[1])
    renderpasses = passes
    rendertypes = types

    if loadedfile.endswith('qgs'):
        QgsProject.instance().readProject.connect(read_project)
        QDir.setCurrent(os.path.dirname(loadedfile))
        fileinfo = QFileInfo(loadedfile)
        QgsProject.instance().read(fileinfo)
