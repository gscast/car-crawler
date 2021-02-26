# Gera um arquivo .dbf integrando as informações contidas nos shapefiles
library(foreign)
library(tidyverse)
library(dplyr)
library(gsubfn)
library(data.table)

# read the input and output dir_paths from user
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

    return(list(dir_path = dir_path, dst_path = dst_path))
}

# get date from dir_path
extract_date <- function(dir_path) {
    # here the accepted date patterns are defined.
    date_patterns <- c("%Y%m%d", "%Y")
    date <- NA

    for (date_pattern in date_patterns) {
        date <- as.Date(basename(dir_path), format = date_pattern)
        if (!is.na(date)) {
            break
        }
    }

    # check the validity dirname format.
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
    files <- list.files(
        path = dir_path, pattern = "albers.dbf$",
        full.names = TRUE, recursive = TRUE
    )

    if (!length(files)) {
        stop(
            "No valid *.dbf files found",
            .call = FALSE
        )
    }
    # print(files)
    # stop()
    return(files)
}

# add the register date and geocode in each dbf observation
add_date <- function(file, date) {
    city_data <- data.table(read.dbf(file, as.is = TRUE))
    city_data[, DATA := date]
    return(city_data)
}

user_input <- read_input()

car_brasil <- rbindlist((
    lapply(fetch_dbf(user_input$dir_path), add_date,
        date = extract_date(user_input$dir_path))),
    use.names = TRUE
)

output_fp <- file.path(
    user_input$dst_path,
    paste0(
        basename(user_input$dir_path),
        "_CAR_Brasil.csv"
    )
)

str(car_brasil)
fwrite(car_brasil, output_fp, sep = ";")