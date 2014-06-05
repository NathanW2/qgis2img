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
$ python.exe qgis2img --project parcels.qgs --passes 5
Project Loaded with: [u'PARCEL_region - Shp', u'PARCEL_region - Spatialite']
Rendering images with 5 passes
Layer: PARCEL_region - Shp      4.907 sec
Layer: PARCEL_region - Spatialite       3.66 sec
Layer: Project     5.3378 sec
```

Layers only:
```
$ python.exe qgis2img --project parcels.qgs --passes 5 --types layer
Project Loaded with: [u'PARCEL_region - Shp', u'PARCEL_region - Spatialite']
Rendering images with 5 passes
Layer: PARCEL_region - Shp      4.907 sec
Layer: PARCEL_region - Spatialite       3.66 sec
```
