setClass("ResourceSet",
         representation(
           sourceString="character",
           resources="list"
         ))

setMethod("show", "ResourceSet",
         function(object) {
           cat(paste0("ResourceSet:\n",
                  "  source: ", object@sourceString, "\n",
                  "  ",length(object@resources), " resources\n"))
         })

ResourceSet <- function(sourceString) {
  new("ResourceSet", sourceString=sourceString, resources=list())
}
