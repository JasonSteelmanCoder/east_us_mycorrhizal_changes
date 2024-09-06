# Introduction:

This repository contains programs to build maps of the change in arbuscular mycorrhizal 
versus ectomycorrhizal tree dominance in forests of the eastern United States from a T1 of 1980-1998 
through a T2 of 2015-2022. It also includes the necessary software to build comparable maps with several 
potentially correlated phenomena. These include fire frequency, atmospheric nitrogen deposition, mean annual 
temperature, mean annual precipitation, and ecoregion.

## Change in AM / EM Dominance Map:

This map uses the Forest Inventory and Analysis (FIA) database to track changes in the dominance of arbuscular 
mycorrhizal (AM) versus ectomycorrhizal (EM) trees in the eastern United States from T1 (1980-1998) to T2 of 2015 - 
2022. Recorded changes are used to build a county-by-county map of the 26 states east of the Mississippi 
River, in which color indicates the difference over time in the dominance of AM and EM species. 

## Data Used for AM / EM Dominance:

The majority of the data used in the AM / EM map comes from the FIA database, and can be downloaded 
for free at https://apps.fs.usda.gov/fia/datamart/datamart.html. 

For each state, you will need three tables: TREE, PLOT, and COND from FIA Datamart. You will also need the 
REF_SPECIES table. Detailed descriptions of these tables can be found at 
https://www.fs.usda.gov/research/sites/default/files/2023-11/wo-fiadb_user_guide_p2_9-1_final.pdf.

Data on the mycorrhizal affiliation of various tree genera come largely from the works of 
Brundrett and Tedersoo (https://doi.org/10.1007/s11104-020-04627-9) (https://doi.org/10.1111/nph.15440) 
and of Akhmetzhanova, Soudzilovskaia, et al. (https://esapubs.org/archive/ecol/E093/059/).
Relevant data from these two sources have been included for your convenience as 
mycorrhiza_brundrett_tedersoo.csv and mycorrhiza_akhmetzhanova.csv. Other trees are 
classified in the file called mycorrhiza_mkt.csv. The original sources for those 
classifications are included in the 'source' column of that table.

## Steps to Build the AM / EM Map:

    1. Go to FIA Datamart. For each of the states east of the Mississippi River, download the zip file 
    for plot, tree, and cond. Unzipping those files will leave you with a csv file for each. Put all of 
    the plot files in one folder, the tree files in another, and the cond files in a third.
    
    2. csv_to_sql_converter.py contains a function that takes in a csv file and outputs a SQL query that 
    will create a postgres table to hold the contents of the csv. converter_looper.py will run that 
    function once for every csv file in a folder. You should run converter_looper.py once for the plot 
    files folder, once for tree files, and once for cond files.     
    
    3. When converter_looper.py finishes running, copy its output into a Postgres query. Running the 
    query will create columns for the contents of the csv files to later be filled into. 

    
    4. Run copier_looper.py on your plot folder, your tree folder, and your cond folder. It will create 
    SQL queries to copy the contents of the csv files into their corresponding tables in the database.  

    Note: The query created by converter_looper.py may choose incorrect data types for some columns. To 
    fix a column with the incorrect datatype, run alterer_looper.py to write queries for all states. 
    Then run those queries on the database to adjust datatypes for all states at once. When all 
    datatypes are correctly assigned, the copy queries will run without throwing an error.
    
    5. Combine the by-state plot, tree, and cond tables in the database  into one East-US table for plot 
    and one for tree
    
    6. Use csv_to_sql_converter.py to create a SQL query to create mycorrhiza_akhmetzhanova, 
    mycorrhiza_brundrett_tedersoo, and mycorrhiza_mkt tables in your database. Copy their values into the 
    new tables from the csv files of the same name.  
    
    7. Download REF_SPECIES from datamart and insert it into the database. Again, you can use 
    csv_to_sql_converter.py to write your SQL query.
    
    8 Use assign_associations_to_species_nums_in_REF_SPECIES.sql to add an associations column to the 
    REF_SPECIES table.
    
    9. Use am_dominance_finder.py to find the basal area of AM and basal area of EM trees for each county 
    and compare them.
    
    10. Download a counties shapefile from the Census Bureau website and remove counties east of the 
    Mississippi River
    
    11. Use shapefile_field_filler.py to add data from percents_and_ratios csv to shapefile fields.
    
    12. Color counties by their attirbutes (shapefile > symbology > categorized. Don't forget to click 
    'classify'!)

## Fire Frequency Map:

This map tracks how many times a forest plot within the county was 
observed to have fire damage between 1999 and 2023. 

## Data Used for the Fire Frequency Map:

This data comes from the plot table of the FIA database.

## Steps to Build the Fire Frequency Map:

    1. If you haven't already, follow steps 1-5 from the AM/EM Pipeline directions (The tree table is 
    not necessary if you only want fire data.)
    
    2. Use loop_fire_finder.py to create a CSV file with all the counties and their associated number 
    of burned plots 
    
    3. Convert the csv to an excel workbook for importing to arcgis pro
    
    4. Add a layer with the East US Counties shapefile. (see the AM/EM pipeline directions for more details)
    
    5. Add the excel workbook with the fire data to the arcgis pro project
    
    6. Add a column to the shapefile and a column to the fire data table that combines their state and 
    county codes into one value
    
    7. Join the table with the shapefile

    8. Calculate a new column in the shapefile's attribute table by dividing fire_observations by plots
    
    9. Color counties by the calculated column

## Temperature and Precipitation Maps:

The temperature and precipitation maps track the mean annual temperature and precipitation for a given 
county.

## Data Used for the Temperature and Precipitation Maps:

Data for these maps is from 30 Year Normals datasets provided by the PRISM Climate Group. 

## Steps to Build the Temperature and Precipitation Maps:

    1. Go to https://prism.oregonstate.edu/normals/
    
    2. Choose precipitation or temperature and select 'Download Data (.asc)'
    
    3. Unzip the folder
    
    4. On a new map in ArcGIS Pro, click 'add data'. Select the Raster Dataset from the folder you just 
    unzipped
    
    5. Export the raster and remove the original file from the GIS project
    
    6. Add a layer with the East US Counties shapefile. (see the AM/EM pipeline directions for more details)
    
    7. Don't forget to export the features and remove the original file from the project
    
    8. In geoprocessing, do a 'raster to point' conversion on the raster
    
    9. In geoprocessing, do a spatial join. 
    
        - The target is the shapefile. 
    
        - Join features should be the points made from the raster.  
    
        - In 'Fields', click edit, then select grid_code, then set the 'source fields' to 'Mean'
    
        - Click Ok
    
        - Click run
    
    10. In symbology, set your shapefile layer to be colored by grid_code. (grid code contains the 
    temperature or precipitation values)
    
    11. In the attribute table, rename grid_code to show that it is temperature or precip
    
    12. In the attribute table, click the hamburger menu and export the table to a csv file

## Nitrogen Deposition Map:

The nitrogen deposition map shows an estimate of the annual kilograms per hectare per year of nitrogen deposition for each county.

## Data Used for the Nitrogen Deposition Map:

The data for this map comes from the National Atmospheric Deposition Program's National Trends Network datasets.

## Steps to Build the Nitrogen Deposition Map:

    1. At https://nadp.slh.wisc.edu/networks/national-trends-network/ download ntn.csv and 
    NTN-ALL-a-s-dep.csv

    2. Add the two tables to a database (see the AM/EM pipeline directions for more details)

    3. Change values of -9 to NULL

    4. Use annual_n_deposition_by_site.sql on the tables to find kg/ha/yr of N deposited, as well as latitude and longitude, at each site

    5. Save the results to a csv file

    6. Add data from the csv file to your map in ArcGIS Pro

    7. Create Points from table

    8. Do DWI on the points to make a raster (cell size should be small. I settled on 0.1)

    9. Add your counties shapefile

    10. Do raster to points conversion

    11. Do a spatial join between the shapefile and the points

    12. Color your counties based on the resulting values in the shapefile's attribute table (kg/ha/yr 
    from 1980 to 2022)

## Ecoregions Map:

The ecoregions map assigns an ecoregion to each county in the eastern United States.

## Data Used for the Ecoregions Map:

This map uses a raster provided by the US Forest Service, delineating the ecoregions of the US.

## Steps to Build the Ecoregions Map:

    1. At https://data.fs.usda.gov/geodata/edw/datasets.php?dsetCategory=geoscientificinformation 
    download Ecological Provinces shapefile
    
    2. Add the raster layer to your map
    
    3. Add the shapefile for counties to your map
    
    4. Clip the raster to the size of the counties shapefile
    
    5. Create a python notebook  
    
    6. Run assign_regions_to_counties.py in the notebook
    
    7. Assign colors to the layer based on region_id

## Invasive Earthworms Maps:

The invasive earthworms maps reflect, for each county, whether the data shows reports of invasive earthworms in that county. There is a map for invasive worms generally, and one each for epigeic, anecic, endogeic, and epi-endogeic ecological groups.

## Data Used for the Invasive Earthworms Maps:

Reports of earthworm presence are from the Phillips, Chang, and Drake datasets. Assignments of species to ecological groups is based on Phillips, with input from Mac Callaham. All of the observations reported by Chang are non-native. Some of the Phillips data is labeled native or non-native. That has been supplemented by Mac Callaham for species that have values of NA in the Phillips data. Drake observations were labeled non-native if Drake reports them as not being Nearctic. Nearctic species, meanwhile, were scrutinized by Mac as well.

## Steps to Build the Invasive Earthworms Maps:

    1. Get 1880_philips sites and worm_species_occurrence, worms_drake, ecological_groups_callaham, drake_nearctic_worms___presumed_native_to_east_us_MKT_MAC, and phillips_worms_in_east_us_without_native_assignment_MKT_MAC datasets
    
    2. Add datasets to database as sites_phillips, worm_sp_occur_phillips, worms_drake, ecological_groups_callaham, drake_nativeness, and phillips_nativeness, respectively
    
    3. Use update_phillips_native_column.sql to eliminate some of the 'NA' values in Phillips' 'native' column
    
    4. Make a csv from phillips_sites site_name, latitude_decimal_degrees, longitude_decimal_degrees
    
    5. Run lat_long_to_county.py to get counties for each site in the csv
    
    6. Add the phillips_sites_fips.csv into the database as phillips_sites_fips 
    
    7. Download county_fips_master.csv from https://github.com/kjhealy/fips-codes/blob/master/county_fips_master.csv
    
    8. Copy county_fips_master.csv into the database as county_fips
    
    9. Run make_east_us_counties_table_from_county_fips_table.sql  
    
    10. Get the "Chang et al supplement" file and convert it to a csv
    
    11. Add the "Chang et al supplement" file to the database as worms_chang

    12. Run lat_long_to_county_chang.py to get counties for each site in the csv
    
    13. Add the resulting chang_fips csv as a table in the database
    
    14. Use add_statecd_to_worms_drake.sql to make columns in worms_drake table with statecd and countycd that are compatible with the rest of the project
    
    15. Use create_ecological_groups_table.sql to create a table for ecological groups of species found in the eastern US
    
    16. Add an empty column, ecological_group, to the ecological_groups table
    
    17. Use add_ecological_groups_to_ecological_groups_table.sql to update the ecological_groups table
    
    18. Use ecological_group_finder.py to make a csv with the presence of each ecological group for each county
    
    19. Add the east_us_shapefile to your map (see the AM/EM pipeline directions for more details)
    
    20. Add your ecological groups csv to the map as a table (don't forget to export it and remove the original from the project)
    
    21. Make a column in the exported table that combines statecd and countycd into a single value for each row
    
    22. Join the table with the shapefile
    
    23. Color your map layer according to whichever ecological group(s) you want to display

## Fire Reports Map:

For each county, this map measures how many official reports of wildfires have been filed in lattitudes and longitudes corresponding to that county, per year, per km^2.

## Data Used for the Fire Reports Map:

The data used is from RDS-2013-0009.6_Data_Format4_SQLITE.zip, downloaded at https://www.fs.usda.gov/rds/archive/catalog/RDS-2013-0009.6

## Steps to Build the Fire Reports Map:

    1. Download RDS-2013-0009.6_Data_Format4_SQLITE.zip from https://www.fs.usda.gov/rds/archive/catalog/RDS-2013-0009.6

    2. Optionally use jo_data_explorer.py to explore the data. Several useful queries are in the comments at the bottom of the program.

    3. Use fire_reports_by_latitude_finder.py to create a csv with unique fire reports
    
    4. In an ArcGIS project, add a shapefile of the eastern US, along with the csv you just created (fire_report_unique_lat_long_dates.csv)
    
    5. Use the Table to Point tool to make points based on the latitudes and longitudes in the table
    
    6. Do a spatial merge between the map and the points to get a feature layer where all of the counties have a column, Join Count, that shows the number of reports that happened within the county's borders
    
    7. Calculate a new column in the attribute table using the python expression below. 
    
        ```
            # reports refers to the number of reports, called `Join count` in the attribute table
            # land_area is the land area of the county.
            # I divide land_area by 1000000 because it is recorded in my shapefile as a much larger into
            # 28 is the number of years in the data. We divide by it to get a per-year rate
            
            def double_div(reports, land_area):
                return (reports / (land_area / 1000000)) / 28
        ```  
    
    8. Color your map based on the new column. The units will be reports/km^2/year

## Steps to plot fire-adaptation vs ECM dominance by eco-region:

    1. Use find_most_common_species_by_basal_area.sql to find the 75 most abundant species by basal area
    
    2. Make the most common species by basal area into a database table called fire_adaptation
    
    3. Run adaptation_ratio_finder.py to find the relevant values and save them to a file called adaptation_by_county.csv
    
    4. Run compare_pct_em_pct_adapted.py to build visualizations from the numbers
    
    5. Run compare_em_vs_adapted_by_region.py to get visualizations for each ecological region