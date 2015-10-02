start <- function() {
  args <- commandArgs(TRUE)
  resourceSet_source <- ""
  if (length(args) > 1) {
    resourceSet_source <- args[2]
  }

  initfile <- system.file("epivizFileServer_init.r", package="epivizFileServer")
  cat("Starting Rserve with init script", initfile, "and resourceSet source", resourceSet_source, "\n")
  Rserve::Rserve(args=paste0("--RS-source '", initfile, "' --args ", resourceSet_source))
}
