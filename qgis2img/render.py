import os

from qgis.core.contextmanagers import qgisapp
from qgis.core import (
    QgsMapSettings,
    #QgsMapRendererSequentialJob,
    QgsMapRendererParallelJob)

from PyQt4.QtCore import QSize

import projectparser

curr_path = os.path.dirname(os.path.abspath(__file__))
defaultimagepath = os.path.join(curr_path, '..', 'images')

def render_images(alllayers, projectlayers, settings, imagecount, whattorender):
    """
    Render images with the given layers and settings.
    @param alllayers: All the layers to render.
    @param projectlayers: All project layers to render.
    @param settings: The settings to render with
    @param imagecount: The number of passes to do for each layer.
    @param whattorender:
    @return: A generator that will render each image as it unwound.
    """
    def _render_images(name, layerids):
        timings = []
        for i in range(imagecount):
            image, timing = render_layers(settings, layerids)
            timings.append(timing)
            export_image(image, name, defaultimagepath)
        return timings

    if 'layer' in whattorender:
        for layer in alllayers:
            timings = _render_images(layer.name(), [layer.id()])
            yield layer.name(), timings
    if 'project' in whattorender:
        projectids = [layer.id() for layer in projectlayers]
        timings = _render_images("Project", projectids)
        yield "Project", timings

def render(settings):
    """
    Render the given settings to a image and save to disk.
    name: The name of the final result file.
    settings: QgsMapSettings containing the settings to render
    exportpath: The folder for the images to be exported to.
    """
    job = QgsMapRendererParallelJob(settings)
    #job = QgsMapRendererSequentialJob(settings)
    job.start()
    job.waitForFinished()
    image = job.renderedImage()
    return image, job.renderingTime()

def render_layers(settings, layers):
    """
    Render the given layers to a image.
    @param layers: The images to render.
    @param settings: The settings used to render the layer.
    @return: The image and the render time.
    """
    settings.setLayers(layers)
    return render(settings)

def export_image(image, name, exportpath=defaultimagepath):
    """
    Export the image with the given name to the folder.
    @param image: The image to export.
    @param name: The name of the result image.
    @param exportpath: The export path.
    """
    if not os.path.exists(exportpath):
        os.mkdir(exportpath)
    image.save(os.path.join(exportpath, name + '.png'))

def read_project(projectfile):
    """
    Read the given project file and extract the layers from it.
    @param projectfile: The project file to load
    @return: A tuple with the project project instance, all project layers, visible layers, settings
    """
    project = projectparser.Project.fromFile(projectfile)
    layers = project.maplayers()
    projectlayers = list(project.visiblelayers())
    settings = project.settings()
    return project, layers, projectlayers, settings

def print_stats(layers, stats, settings):
    results = []
    maxlengthname = max([len(layer.name()) for layer in layers])
    for layer, timings in stats:
        time = float(sum(timings)) / len(timings) / 1000
        stddev = (sum(map(lambda x: (x/1000.-time)**2, timings)) / len(timings))**0.5
        results.append(
            "Layer: {0:{maxlen}} {1:>10} sec     (stddev {2:>10} sec)".format(
                layer, time, stddev, maxlen=maxlengthname))

    width = len(max(results, key=len))
    print "{0:*^{width}}".format("Results", width=width)
    print "Scale: {}".format(settings.scale())
    print "\n".join(results)

def run(args):
    """
    Run qgis2img in benchmark mode.
    @param args: Args passed into the application.
    @return:
    """
    command = args.subparser_name
    if command == "bench":
        rendertypes = args.types.split('|')
        renderpasses = args.passes
    else:
        rendertypes = 'project'
        renderpasses = 1

    size = QSize(*args.size)
    if args.file.endswith('qgs'):
        with qgisapp(guienabled=False) as app:
            parser, layers, projectlayers, settings = read_project(args.file)
            settings.setOutputSize(size)
            print "Project Loaded with:", [layer.name() for layer in layers]
            print "Rendering images with {0} passes".format(renderpasses)
            ## Good to go
            renderresults = render_images(layers, projectlayers, settings, renderpasses, rendertypes)
            if command == "bench":
                print_stats(layers, renderresults, settings)
            else:
                # Just unwind the generator to run the export.
                results = list(renderresults)
            print "Done"
