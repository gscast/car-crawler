# CAR-dataset
Tools for working on the CAR shapefile datasets.

Currently the following scripts are avaiLable:
- uncompress_dbf.py: bach unzipping of databases of interest.
- collect_ipam_brasil.py: unite all properties information from the cities shapefile into a single database and add a geocode for referencing.
- get_oldest_date.py join all dataframes generated with add_geocodigo_col.r and select the oldest registration date for every property in the database.