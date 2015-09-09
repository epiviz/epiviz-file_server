library(epivizr)

mgr = epivizr:::EpivizDeviceMgr$new()

colon_blocks <- rtracklayer::import("example_data/colon_blocks.bed")
mgr$addMeasurements(colon_blocks, "450k colon blocks")
