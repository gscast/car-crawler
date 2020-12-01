library("foreign")
library("tidyverse")
library("dplyr")

args <- commandArgs(trailingOnly = TRUE)

# read the input and output paths
if (length(args) < 1) {
  stop("At least one argument must be supplied (input dir)", call. = FALSE)
} else if (length(args) == 1) {
  # default output file
  args[2] <- args[1]
}

dir_path <- args[1]
dst_path <- args[2]

# add files matching the given patterns.
patterns <- c("*AREA_IMOVEL.dbf", "*_Area_imovel_albers.dbf")
files <- c()

for (regex in patterns) {

    to_append <- list.files(
        path = dir_path, pattern = regex,
        full.names = TRUE, recursive = TRUE
    )
    files <- append(files, to_append)
}

date <- as.Date(basename(dir_path), format = "%Y%m%d")

reshape_df <- function(x) {

    #get geocode from folder name
    geocode <- stringr::str_split(
        basename(dirname(dirname(x))), "_")[[1]][2]

    if (is.na(geocode)) {
        # no geocode found
        city_data <- read.dbf(x, as.is = TRUE) %>%
            add_column(DATA = date)
    } else

        city_data <- read.dbf(x, as.is = TRUE) %>%
            add_column(geocodigo = geocode) %>%
            add_column(DATA = date)

    return(city_data)
}

stacked_df <- lapply(files, reshape_df) %>%
    dplyr::bind_rows()

str(stacked_df)
write.dbf(
    as.data.frame(stacked_df),
    file.path(dst_path, paste0(basename(dst_path), "_area_imovel.dbf")))
