startBackend <- function() {
  args <- commandArgs(TRUE)
  resourceSet_source <- ""
  if (length(args) > 1) {
    resourceSet_source <- args[2]
  }

  initfile <- system.file("epivizFileServer_init.r", package="epivizFileServer")
  cat("Starting Rserve with init script", initfile, "and resourceSet source", resourceSet_source, "\n")
  Rserve::Rserve(args=paste0("--RS-source '", initfile, "' --args ", resourceSet_source))
}

startFrontend <- function() {
  python_dir <- system.file("frontend", package="epivizFileServer")
  command <- paste0("cd ", python_dir, " & ",
                    "python main.py")
  system(command)
}
