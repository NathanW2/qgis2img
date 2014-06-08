import os

from qgis.core import (
    QgsProviderRegistry,
    QgsMapLayerRegistry,
    QgsProject,
    QgsMapSettings,
    #QgsMapRendererSequentialJob,
    QgsMapRendererParallelJob)

from PyQt4.QtCore import QDir, QFileInfo, QSize

curr_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(curr_path, '..', 'images')


def render_images(layers, project_layers, settings):
    if 'layer' in RENDER_TYPES:
        for layer_id, layer in layers.iteritems():
            timings = []
            for i in range(RENDER_PASSES):
                timings.append(render_layer(layer, settings))
            yield layer.name(), timings
    if 'project' in RENDER_TYPES:
        timings = []
        for i in range(RENDER_PASSES):
            timings.append(render_project(project_layers, settings))
        yield "Project", timings


def render(name, settings):
    settings.setOutputSize(IMAGE_SIZE)
    job = QgsMapRendererParallelJob(settings)
    #job = QgsMapRendererSequentialJob(settings)
    job.start()
    job.waitForFinished()
    image = job.renderedImage()
    if not os.path.exists(image_path):
        os.mkdir(image_path)
    image.save(os.path.join(image_path, name + '.png'))
    return job.renderingTime()


def render_project(layers, settings):
    settings.setLayers(layers)
    # noinspection PyUnresolvedReferences
    return render(QgsProject.instance().title(), settings)


def render_layer(layer, settings):
    settings.setLayers([layer.id()])
    return render(layer.name(), settings)


def read_project(doc):
    # noinspection PyUnresolvedReferences
    layers = QgsMapLayerRegistry.instance().mapLayers()
    print "Project Loaded with:", [layer.name() for layer in layers.values()]
    print "Rendering images with {0} passes".format(RENDER_PASSES)
    import project_parser
    parser = project_parser.ProjectParser(doc)
    project_layers = list(parser.visible_layers())
    settings = parser.settings()
    images = render_images(layers, project_layers, settings)
    print_stats(images, settings)


def print_stats(stats, settings):
    results = []
    # noinspection PyUnresolvedReferences
    layers = QgsMapLayerRegistry.instance().mapLayers().values()
    maximum_name_length = max([len(layer.name()) for layer in layers])
    for layer, timings in stats:
        time = float(sum(timings)) / len(timings) / 1000
        results.append(
            "Layer: {0:{maxlen}} {1:>10} sec".format(
                layer, time, maxlen=maximum_name_length))

    width = len(max(results, key=len))
    print "{0:*^{width}}".format("Results", width=width)
    print "Scale: {}".format(settings.scale())
    print "\n".join(results)


def main(load_file, image_size, passes, render_types):
    global IMAGE_SIZE
    global RENDER_PASSES
    global RENDER_TYPES

    IMAGE_SIZE = QSize(image_size[0], image_size[1])
    RENDER_PASSES = passes
    RENDER_TYPES = render_types

    if load_file.endswith('qgs'):
        QgsProject.instance().readProject.connect(read_project)
        QDir.setCurrent(os.path.dirname(load_file))
        file_info = QFileInfo(load_file)
        # noinspection PyUnresolvedReferences
        QgsProject.instance().read(file_info)
