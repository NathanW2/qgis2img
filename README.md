# qgis2img

A tool for generating images and running benchmarks against QGIS projects 

## Usage

```
usage: qgis2img [-h] [--size SIZE] [--passes PASSES] [--types TYPES] file

Benchmark QGIS project file and layer loading times

positional arguments:
  file             Project file to load into QGIS

optional arguments:
  -h, --help       show this help message and exit
  --size SIZE      Image output size
  --passes PASSES  Number of render passes per layer
  --types TYPES    What to render. Options are layer|project, layer, or project.
                   layer|project will render all layers as the if the project
                   is open in QGIS.
```

## Example:

```
$ python.exe qgis2img parcels.qgs --passes 5
Project Loaded with: [u'PARCEL_region - Shp', u'PARCEL_region - Spatialite']
Rendering images with 5 passes
Layer: PARCEL_region - Shp      4.907 sec
Layer: PARCEL_region - Spatialite       3.66 sec
Layer: Project     5.3378 sec
```

Layers only:
```
$ python.exe qgis2img parcels.qgs --passes 5 --types layer
Project Loaded with: [u'PARCEL_region - Shp', u'PARCEL_region - Spatialite']
Rendering images with 5 passes
Layer: PARCEL_region - Shp      4.907 sec
Layer: PARCEL_region - Spatialite       3.66 sec
```
