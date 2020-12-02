library(foreign)
library(tidyverse)
library(dplyr)
library(gsubfn)

# read the input and output dir_paths
read_input <- function() {
    args <- commandArgs(trailingOnly = TRUE)

    if (length(args) < 1) {
        stop("At least one argument must be supplied (input dir)",
            call. = FALSE
        )
    } else if (length(args) == 1) {
        # default output file
        args[2] <- args[1]
    }

    dir_path <- args[1]
    dst_path <- args[2]

    return(list(dirpath = dir_path, dst_path = dst_path))
}

# get date from dir_path
extract_date <- function(dir_path) {
    date_patterns <- c("%Y%m%d", "%Y")
    date <- NA

    for (date_pattern in date_patterns) {
        date <- as.Date(basename(dir_path), format = date_pattern)
        if (!is.na(date)) {
            break
        }
    }

    # check the dirname format. it should be a date containing a year
    if (is.na(date)) {
        stop(paste(
            "Could not extract date from the input directory.",
            dir_path,
            "should be named with one of the folowwing patterns:",
            date_pattern
        ),
        .call = FALSE
        )
    }

    return(date)
}

# fetch the database files in dir_path matching the valid patterns.
fetch_dbf <- function(dir_path) {
    patterns <- c("*AREA_IMOVEL.dbf", "*_Area_imovel_albers.dbf")
    files <- c()

    for (regex in patterns) {
        to_append <- list.files(
            path = dir_path, pattern = regex,
            full.names = TRUE, recursive = TRUE
        )
        files <- append(files, to_append)
    }

    if (!length(files)) {
        stop(
            "No valid *.dbf files found",
            .call = FALSE
        )
    }

    return(files)
}

user_input <- read_input()
dir_path <- user_input["dir_path"]
dst_path <- user_input["dst_path"]

data_registro <- extract_date(dir_path)
files <- fetch_dbf(dir_path)

# add the register date and geocode in each dbf observation
reshape_df <- function(file) {
    city_data <- read.dbf(file, as.is = TRUE) %>%
        add_column(DATA = data_registro)

    # get geocode from folder name
    geocode <- stringr::str_split(
        basename(dirname(dirname(x))), "_"
    )[[1]][2]

    # geocode found
    if (!is.na(geocode)) {
        city_data <- add_column(city_data, geocodigo = geocode)
    }

    return(city_data)
}

stacked_df <- lapply(files, reshape_df) %>%
    dplyr::bind_rows()

str(stacked_df)

output_fp <- file.path(dst_path, paste0(basename(dst_path), "_area_imovel.dbf"))
write.dbf(
    as.data.frame(stacked_df),
    output_fp
)

print("Resulting database: ", output_fp)
