library(foreign)
library(tidyverse)
library(dplyr)
library(RSQLite)

sql_path <- "/media/gabriel/Gabriel/Datasets/CAR/Bases_Antigas/datas_imoveis201703.sqlite"

con <- dbConnect(drv = RSQLite::SQLite(), dbname = sql_path)

## list all tables
tables <- dbListTables(con)

## exclude sqlite_sequence (contains table information)
tables <- tables[tables != "sqlite_sequence"]

df_list <- vector("list", length = length(tables))

## create a data.frame for each table
for (i in seq(along = tables)) {
    df_list[[i]] <- dbGetQuery(
        conn = con,
        statement = paste("SELECT * FROM '",
            tables[[i]], "'",
            sep = ""
        )
    )
}

df <- df_list[[1]] %>%
    transmute(COD_IMOVEL = cod_imovel,
              DATA = as.Date(dat_criacao))
head(df)
str(df)
dbDisconnect(con)
