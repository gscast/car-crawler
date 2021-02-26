library(foreign)
library(tidyverse)
library(dplyr)
library(data.table)

read_input <- function() {
       args <- commandArgs(trailingOnly = TRUE)
       return(args[1])
}

# fetch the database files in dir_path matching the valid patterns.
fetch_csv <- function(dir_path) {
       files <- list.files(
              path = dir_path, pattern = "*\\.csv$",
              full.names = TRUE, recursive = TRUE
       )

       if (!length(files)) {
              stop(
                     "No valid *.csv files found",
                     .call = FALSE
              )
       }

       return(files)
}

col_names <- c(
       "COD_IMOVEL", "NUM_AREA", "COD_ESTADO",
       "NOM_MUNICI", "NUM_MODULO", "TIPO_IMOVE",
       "SITUACAO", "CONDICAO_I"
)

convert_csv <- function(csv) {
       print(csv)
       dt <- fread(csv, col.names = col_names)
       head(dt)
       stop()
       write.dbf(gsub(".csv$", ".dbf", file), dt)
}

lapply(fetch_csv(read_input()), convert_csv)
