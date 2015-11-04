setClass("EpivizFileServer",
         representation(
           mgr="EpivizDeviceMgr",
           resourceSet="ResourceSet"
         ))

setMethod("show", "EpivizFileServer",
          function(object) {
            cat(paste0("EpivizFileServer:\n"))
            show(object@resourceSet)
            show(object@mgr)
          })

EpivizFileServer <- function(resourceSet) {
  mgr <- epivizr:::EpivizDeviceMgr$new()
  new("EpivizFileServer", mgr=mgr, resourceSet=resourceSet)
}

handle_request <- function(fileServer, action, msgData) {
  fileServer@mgr$handle(action, msgData)
}
