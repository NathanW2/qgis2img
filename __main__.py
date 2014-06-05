from qgisapp import qgisapp
import qgis2img
import argparse

parser = argparse.ArgumentParser(description="Benchmark QGIS project file and layer loading times")
parser.add_argument('file', help="Project file to load into QGIS")
parser.add_argument('--size', dest='size', default='1580x906', help="Image output size")
parser.add_argument('--passes', dest='passes', type=int, default=3, help="Number of render passes per layer")
parser.add_argument('--types', dest='types', default='layer|project', help="What to render options are layer|project,"
                                                                                 "layer or project. layer|project will render"
                                                                                 "all layers as the if the projcet is open in QGIS.")
args = parser.parse_args()

if not args.file:
    parser.print_help()
    parser.exit()

width, height = args.size.split('x')
rendertypes = args.types.split('|')

# Good to go
with qgisapp(guienabled=False) as app:
    qgis2img.main(app, args.file, (int(width), int(height)), args.passes, rendertypes)
