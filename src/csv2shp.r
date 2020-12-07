library(foreign)
library(tidyverse)
library(dplyr)

csv_path <- "/home/gabriel/Desktop/tmp/1200013.csv"
dbf_path <- "/home/gabriel/Desktop/tmp/SHAPE_1200013/AREA_IMOVEL/AREA_IMOVEL.dbf"

area_imovel_colnames <- colnames(dbf_df)

dbf_df <- read.dbf(dbf_path, as.is = TRUE) %>%
            mutate(NUM_AREA = round(NUM_AREA, digits = 4)) %>%
            arrange(COD_IMOVEL)

csv_df <- read.csv2(csv_path, skip = 3, header = FALSE, as.is = TRUE,
                    col.names = area_imovel_colnames) %>%
                mutate(NUM_AREA = as(NUM_AREA),
                       NUM_MODULO = as.numeric(NUM_MODULO)) %>%
                arrange(COD_IMOVEL)


attr(csv_df, 'data_types') <- attributes(dbf_df)$data_types

head(dbf_df)
head(csv_df)