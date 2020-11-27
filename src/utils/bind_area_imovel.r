library("foreign")
library("tidyverse")
library("dplyr")

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 1) {
  stop("At least one argument must be supplied (input dir)", call. = FALSE)
} else if (length(args) == 1) {
  # default output file
  args[2] <- args[1]
}

print(args)

dir_path <- args[1]
dst_path <- args[2]

# select the databases containing the properties total area
files <- list.files(
    path = dir_path, pattern = "*AREA_IMOVEL.dbf",
    full.names = TRUE, recursive = TRUE
)

reshape_df <- function(x) {

    parent_dir <- basename(dirname(dirname(x)))

    city_data <- read.dbf(x, as.is = TRUE) %>%
        group_by(NOM_MUNICI, COD_ESTADO) %>%
        summarise(NUM_IMOVEIS = n_distinct(COD_IMOVEL)) %>%
        add_column(DIR_PAI = parent_dir)

    return(city_data)
}

stacked_df <- lapply(files, reshape_df) %>%
    bind_rows() %>%
    arrange((desc(NUM_IMOVEIS)))

glimpse(stacked_df)
write.dbf(
    as.data.frame(stacked_df),
    file.path(dst_path, paste0(basename(dst_path), "_area_imovel.dbf")))