library(epivizr)

mgr = epivizr:::EpivizDeviceMgr$new()

data(tcga_colon_example)
colon_blocks_ms <- mgr$addMeasurements(colon_blocks, "450k colon blocks")
