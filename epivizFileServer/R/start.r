start <- function() {
  args <- commandArgs(TRUE)
  resourceSet_source <- NULL
  if (length(args) > 1) {
    resourceSet_source <- args[1]
  }

  message("Running epivizFileServer with resourceSet source", resourceSet_source)
  resourceSet <- ResourceSet(resourceSetSource)
  fileServer <- EpivizFileServer(resourceSet)

  Rserve::run.Rserve()
}
