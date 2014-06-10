# qgis2img

A tool for generating images and running benchmarks against QGIS projects 

## Usage

```
$qgis2img --help
usage: qgis2img [-h] {bench,export} ...

QGIS project file and layer image export tool

positional arguments:
  {bench,export}  Sub command help
    bench         Benchmark render times
    export        Export a image of the project

optional arguments:
  -h, --help      show this help message and exit


$qgis2img bench --help
usage: qgis2img bench [-h] [--size SIZE SIZE] [--passes PASSES]
                      [--types {layer,project,layer|project}]
                      file

positional arguments:
  file                  Project file to load into QGIS

optional arguments:
  -h, --help            show this help message and exit
  --size SIZE SIZE      Image output size
  --passes PASSES       Number of render passes per layer
  --types {layer,project,layer|project}
                        What to render options are layer|project,layer or
                        project. layer|project will renderall layers as the if
                        the projcet is open in QGIS.
```

## Example:

```
$ qgis2img bench parcels.qgs --passes 5
Project Loaded with: [u'PARCEL_region - Shp', u'PARCEL_region - Spatialite']
Rendering images with 5 passes
Layer: PARCEL_region - Shp      4.907 sec
Layer: PARCEL_region - Spatialite       3.66 sec
Layer: Project     5.3378 sec
```

Layers only:
```
$ gis2img bench parcels.qgs --passes 5 --types layer
Project Loaded with: [u'PARCEL_region - Shp', u'PARCEL_region - Spatialite']
Rendering images with 5 passes
Layer: PARCEL_region - Shp      4.907 sec
Layer: PARCEL_region - Spatialite       3.66 sec
```

## NOTE

Requires QGIS 2.4 (QGIS 2.3 dev).
