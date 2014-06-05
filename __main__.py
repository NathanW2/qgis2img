from qgisapp import qgisapp
import qgis2img
import argparse

parser = argparse.ArgumentParser(description="Benchmark QGIS project file and layer loading times")
parser.add_argument('--project', dest='project', help="Project file to load into QGIS")
parser.add_argument('--size', dest='size', default='1580x906', help="Image output size")
parser.add_argument('--passes', dest='passes', type=int, default=3, help="Number of render passes per layer")
args = parser.parse_args()

if not args.project:
    parser.print_help()
    parser.exit()

width, height = args.size.split('x')

# Good to go
with qgisapp(guienabled=False) as app:
    qgis2img.main(app, args.project, (int(width), int(height)), args.passes)
