library(rgdal)
library(sp)
library(foreign)
library(revgeo)
library(dplyr)
library(httr)
library(rlist)
library(jsonlite)
library(dplyr)

get_city <- function(latitude, longitude) {

    print(latitude)

    geocode_data <- list()
    geocode_frame <- data.frame()

    base_url <- 'https://maps.googleapis.com/maps/api/geocode/json'

    query<-list(
        latlng=paste(latitude, longitude, sep=','),
        key='AIzaSyBDyhoa1AhweKjBdcBsGCbArgj2EQFQqsE'
    )

    resp <- GET(base_url, query = query)

    content_json <-content(resp, as="text")
    content_df <- fromJSON(content_json)
    
    address_components <- df$results[1,]$address_components[[1]]

    city_name <- address_components$long_name[2]
    state_abreviation <- address_components$short_name[3]

    print(city_name)
    print(state_abreviation)
    return(content_df)
}
ipam_2014_fp <- "/media/gabriel/Gabriel/Datasets/CAR/IPAM/2014/MT/CAR_SIRGAS_Mar2014.dbf"

API_key = 'AIzaSyBDyhoa1AhweKjBdcBsGCbArgj2EQFQqsE'
API_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key='

dst_dir <- "/media/gabriel/Gabriel/Datasets/CAR/IPAM_Processed/2014/MT"

if (!dir.exists(dst_dir)) {
    dir.create(dst_dir, recursive = TRUE)
}

ipam_2014_dst <- file.path(dst_dir, basename(ipam_2014_fp))

ipam_2014 <- readOGR(dsn = ipam_2014_fp, layer = "CAR_SIRGAS_Mar2014")
data <- ipam_2014@data

ipam_2014_wgs84 <- spTransform(ipam_2014, CRS("+proj=longlat +datum=WGS84"))

coords_wgs84 <- as.data.frame(coordinates(ipam_2014_wgs84)) %>%
    rename(latitude = 2, longitude = 1)

# print(coords_wgs84[1,]$latitude)

df <- get_city(latitude = coords_wgs84[1,]$latitude, longitude = coords_wgs84[1,]$longitude)
# plot(ipam_2014_wgs84, axes = TRUE)