#!/usr/bin/env python

from render import run
import argparse

parser = argparse.ArgumentParser(description="QGIS project file and layer image export tool")

subs = parser.add_subparsers(dest="subparser_name", help="Sub command help")
bench_parser = subs.add_parser("bench", help="Bench mark render times")
bench_parser.set_defaults(func=run)

bench_parser.add_argument('file', help="Project file to load into QGIS")
bench_parser.add_argument('--size', type=int, nargs=2, default=[1580, 906], help="Image output size")
bench_parser.add_argument('--passes', type=int, default=3, help="Number of render passes per layer")
bench_parser.add_argument('--types', choices=['layer', 'project', 'layer|project'], default='layer|project',
                                                                                  help="What to render options are layer|project,"
                                                                                 "layer or project. layer|project will render"
                                                                                 "all layers as the if the projcet is open in QGIS.")

export_parser = subs.add_parser("export", help="Export a image of the project")
export_parser.set_defaults(func=run)
export_parser.add_argument('file', help="Project file to export")
export_parser.add_argument('--size', type=int, nargs=2, default=[1580, 906], help="Image output size")

args = parser.parse_args()
args.func(args)
