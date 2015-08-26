# epivizFileServer

An Rserve-based server of data from files for the [epiviz](http://epiviz.org) visualization tool.

## Design

The goal of this piece of software is to be able to serve data in disk files to the epiviz web app
through a socket connection.

We will use current R/Bioc infrastructure to interface to file in `BED`, `Wig`, `BAM` and `VCF` formats.
It will use the `epivizr` package to handle the epiviz data exchange protocol.

## Usage

To start an epivizFileServer instance use

```{bash}
R CMD epivizFileServer <options> measurements.yaml
```

File `measurements.yaml` indicates location and description of data files to be served. For example

```{yaml}
colon_methblocks:
  type: blocks
  path: /data/experiment/blocks.bed
colon_methsmooth:
  type: bp
  path: /data/experiment/cancer_smoothed.wig
colon_expression:
  type: feature
  assay: /data/experiment/cancer_expression.csv
  rowRanges: /data/experiment/cancer_annotation.bed
  colData: /data/experiment/cancer_pdata.csv
```

Each entry in the yaml file will be a `measurement` in `epiviz` parlance that can be included in visualizations. Data files are assumed to be accessible through the file system in the host running the epivizFileServer process.

###File types supported

| file type | R interface | epiviz class        | current epiviz support    |
|-----------|-------------|---------------------|---------------------------|
| bed       | rtracklayer | EpivizBlockData     |   uncached                |
| wig       | rtracklayer | EpivizWigData       |  cached                   |
| bam       | Rsamtools   | EpivizAlignmentData | uncached coverage         |
| vcf       | VariantTools| N/A                 | none                      |

On the UI side, the connection to the epivizFileServer is specified in a settings file

```{javascript}
epiviz.Config.SETTINGS = {
  websocketProviders: ["http://my.epivizfileserver.host:8000"]
}
```

## Architecture

Rserve will be started with a initialization script that will create the
epivizr objects that serve data from each file in the file description yaml
file.

The JS app will open a Websocket connection and send requests using the existing
epiviz DataProvider API. 

_Unclear_: For security we want something between the rserve instance and the
JS client. 

Options: 
  - Rserve proxy (not well documented)
  - Rserve object capabilities (this may be fine, need further study) 
  - middleware (e.g. node, python running WebSocket), easiest to get started with. python version can build on [epivizpy](http://https://github.com/epiviz/epivizpy) and existing
  Rserve client). This also mimics the setup we have for our WebDataProvider using mysql,
  and, if necessary, it might be easier to transition away from Rserve for the actual data
  handling.
  
  

