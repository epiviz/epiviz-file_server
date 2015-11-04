setClass("ResourceSet",
         representation(
           sourceString="character",
           resources="list"
         ))

setMethod("show", "ResourceSet",
         function(object) {
           cat(paste0("ResourceSet:\n",
                  "  source: ", object@sourceString, "\n",
                  "  ", length(object@resources), " resources\n"))
         })

setClass("Resource",
         representation(
           name="character",
           dataObject="ANY",
           record="list"
         ))

setMethod("show", "Resource",
          function(object) {
            cat(paste0("Resource <", object@name, ">:\n",
                       " data class: ", class(object@dataObject)))
          })

.createResource <- function(name, record, basedir) {
  path <- file.path(basedir, record$url)
  format <- tools::file_ext(path)

  if (!is.null(record$filetype)) {
    format <- record$filetype
  }
  object <- rtracklayer::FileForFormat(path, format)
  columns <- record$columns
  datatype <- record$datatype
  new("Resource", name=name, dataObject=object, record=record)
}

.parseResources_yaml <- function(filepath) {
  resourceRecords <- yaml::yaml.load_file(filepath)
  basedir <- dirname(tools::file_path_as_absolute(filepath))
  mapply(.createResource, name=names(resourceRecords), record=resourceRecords, basedir=basedir)
}

.parseResources <- function(sourceString) {
  # parse based on filetype
  .parser <- switch(tools::file_ext(sourceString),
                    yml=.parseResources_yaml,
                    yaml=.parseResources_yaml,
                    .parseResources_path)
  .parser(sourceString)
}

ResourceSet <- function(sourceString) {
  resources <- .parseResources(sourceString)
  new("ResourceSet", sourceString=sourceString, resources=resources)
}
