library(foreign)
library(tidyverse)
library(dplyr)

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

# find the files with each year's properties info.
files <- list.files(
  path = dir_path, pattern = "*_area_imovel.dbf",
  full.names = TRUE, recursive = TRUE
)

print(files)

df_list <- lapply(files, read.dbf, as.is = TRUE)
# join the yearly tables.
df_cod_imovel <- bind_rows(df_list)

# get the oldest date for each property with the same identification.
cod_imovel_primeira_data <- df_cod_imovel %>%
  group_by(COD_IMOVEL) %>%
  summarise(PRIMEIRA_DATA = min(DATA)) %>%
  select(COD_IMOVEL, AREA, PRIMEIRA_DATA)

head(cod_imovel_primeira_data)

output_fp <- file.path(
  dst_path,
  paste0(
    basename(dst_path),
    "_cod_imovel_por_data.dbf"
  )
)

write.dbf(
  as.data.frame(cod_imovel_primeira_data),
  output_fp
)

print("Resulting database: ", output_fp)
