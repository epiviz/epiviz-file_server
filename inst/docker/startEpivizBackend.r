#!/usr/bin/env r

suppressMessages(library(docopt))
suppressMessages(library(Rserve))

doc <- "Usage: startEpivizBackend.r [-p <path>]

Options:
  -p --path <path> Path to yaml metadata file, overriden by environment variable EPIVIZFS_BACKEND_PATH [default: metadata.yaml]

Examples:
  startEpivizBackend.r -p /epivizfs_data/metadata.yaml
"

opt <- docopt(doc)
resourceSet_source <- opt$path

pathFromEnv <- Sys.getenv("EPIVIZFS_BACKEND_PATH")
if (length(pathFromEnv) > 0 && file.exists(pathFromEnv)) {
  resourceSet_source <- pathFromEnv
}

if (!file.exists(resourceSet_source)) {
  stop("Resource set metadata file not found ", resourceSet_source)
}

initfile <- system.file("epivizFileServer_init.r", package="epivizFileServer")
Rserve::Rserve(args=paste0("--quiet --vanilla --RS-source '", initfile, "' --args ", resourceSet_source))
