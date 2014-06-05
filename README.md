# qgis2img

A tool for generating images and running benchmarks against QGIS projects 

## Usage

```
usage: qgis2img [-h] [--project PROJECT] [--size SIZE] [--passes PASSES]

Benchmark QGIS project file and layer loading times

optional arguments:
  -h, --help         show this help message and exit
  --project PROJECT  Project file to load into QGIS
  --size SIZE        Image output size
  --passes PASSES    Number of render passes per layer
```

## Example:

```
python.exe F:/dev/qgis2img --project F:\dev\qgis2img\projects\parcels.qgs --passes 5
```
