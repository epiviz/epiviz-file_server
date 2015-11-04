library(epivizFileServer)

args <- commandArgs(TRUE)

resourceSet_source <- ""
if (length(args) > 0) {
  resourceSet_source <- args[1]
}

message("Running epivizFileServer with resourceSet source", resourceSet_source)
resourceSet <- ResourceSet(resourceSet_source)
fileServer <- EpivizFileServer(resourceSet)
