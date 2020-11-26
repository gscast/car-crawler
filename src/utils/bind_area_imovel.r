library("foreign")
library("tidyverse")
library("dplyr")

dir_path <- paste0(
    "/home/gabriel/Documents/UFMG/IC/data/CAR/2020",
    "/car_180220/ACRE"
)

empty_df <- TRUE
files <- list.files(
    path = dir_path, pattern = "*AREA_IMOVEL.dbf",
    full.names = TRUE, recursive = TRUE
)

lapply(files, function(x) {
    df <- read.dbf(x, as.is = TRUE) %>%
        group_by(NOM_MUNICI, COD_ESTADO, TIPO_IMOVE, SITUACAO, CONDICAO_I) %>%
        summarise(NUM_IMOVEIS = n_distinct(COD_IMOVEL)) %>%
        arrange(desc(NUM_IMOVEIS))

    if (empty_df) {
        empty_df <<- FALSE
        stacked_df <<- df
    } else {
        stacked_df <<- rbind(stacked_df, df)
    }
})

glimpse(stacked_df)
