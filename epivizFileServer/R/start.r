start <- function() {
  initfile <- system.file("epivizFileServer_init.R", package="epivizFileServer")
  Rserve(args=paste0("--RS-source '", initfile, "'"))
}