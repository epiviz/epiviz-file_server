library(epivizFileServer)

args <- commandArgs(TRUE)
resourceSet_source <- ""
if (length(args) > 1) {
  resourceSet_source <- args[2]
}

message("Running epivizFileServer with resourceSet source", resourceSet_source)
resourceSet <- ResourceSet(resourceSet_source)
fileServer <- EpivizFileServer(resourceSet)

#colon_blocks <- rtracklayer::import("example_data/colon_blocks.bed")
#fileServer$mgr$addMeasurements(colon_blocks, "450k colon blocks")
