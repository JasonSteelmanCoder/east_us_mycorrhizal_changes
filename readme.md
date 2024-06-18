# Introduction:

This repository contains programs to build maps of the change in arbuscular mycorrhizal 
versus ectomycorrhizal dominance in the forests of the eastern United States from a T1 of 1980-1998 
through a T2 of 2015-2022. It also includes the necessary software to build comparable maps with several 
potentially correlated phenomena. These include fire frequency, nitrogen deposition, mean annual 
temperature, mean annual precipitation, and ecoregion.

## Change in AM / EM Dominance Map:

This map uses the FIA database to track changes in the dominance of arbuscular 
mycorrhizal (AM) versus ectomycorrhizal (EM) trees in the eastern United States from T1 to T2 of 2015 - 
2022. Recorded changes are used to build a county-by-county map of the 26 states east of the Mississippi 
River, in which color indicates the difference over time in the dominance of AM and EM species. 

## Data Used for AM / EM Dominance:

The majority of the data used in the AM / EM map comes from the FIA database, and can be downloaded 
for free at https://apps.fs.usda.gov/fia/datamart/datamart.html. 

For each state, you will need three tables: TREE, PLOT, and COND from FIA Datamart. You will also need the 
REF_SPECIES table. Detailed descriptions of these tables can be found at 
https://www.fs.usda.gov/research/sites/default/files/2023-11/wo-fiadb_user_guide_p2_9-1_final.pdf.

Data on the mycorrhizal affiliation of various tree genera come largely from the works of 
Brundrett and Tedersoo and of Akhmetzhanova, Soudzilovskaia, et al. (https://esapubs.org/archive/ecol/E093/059/)
Relevant data from these two sources have been included for your convenience as 
mycorrhiza_brundrett_tedersoo.csv and mycorrhiza_akhmetzhanova.csv. Other trees are 
classified in the file called mycorrhiza_mkt.csv. The original sources for those 
classifications are included in the `source` column of that table.

## Steps to Build the AM / EM Map:

    1. Go to FIA Datamart. For each of the states east of the Mississippi River, download the zip file 
    for plot, tree, and cond. Unzipping those files will leave you with a csv file for each. Put all of 
    the plot files in one folder, the tree files in another, and the cond files in a third.
    
    2. csv_to_sql_converter.py contains a function that takes in a csv file and outputs a SQL query that 
    will create a postgres table to hold the contents of the csv. converter_looper.py will run that 
    function once for every csv file in a folder. You should run converter_looper.py once for the plot 
    files folder, once for tree files, and once for cond files.     
    
    3. When converter_looper.py finishes running, copy its output into a Postgres query. Running the 
    query will create columns for the contents of the CSV files to later be filled into. 

    
    4. Run copier_looper.py on your plot folder, your tree folder, and your cond folder. It will create 
    SQL queries to copy the contents of the CSV files into their corresponding tables in the database.  

    Note: The query created by converter_looper.py may choose incorrect data types for some columns. To 
    fix a column with the incorrect datatype, run alterer_looper.py to write queries for all states. 
    Then run those queries on the database to adjust datatypes for all states at once. When all 
    datatypes are correctly assigned, the copy queries will run without throwing an error.
    
    5. Combine the by-state plot, tree, and cond tables in the database  into one East-US table for plot 
    and one for tree
    
    6. Use csv_to_sql_converter.py to create a SQL query to create mycorrhiza_akhmetzhanova, 
    mycorrhiza_brundrett_tedersoo, and mycorrhiza_mkt tables in your database. Copy their values into the 
    new tables from the CSV files of the same name.  
    
    7. Download REF_SPECIES from datamart and insert it into the database. Again, you can use 
    csv_to_sql_converter.py to write your SQL query.
    
    8 Use assign_associations_to_species_nums_in_REF_SPECIES.sql to add an associations column to the 
    REF_SPECIES table.
    
    9. Use loop_ratio_finder.py to find the basal area of AM and basal area of EM trees for each county 
    and compare them
    
    10. Download a counties shapefile from the Census Bureau website and remove counties east of the 
    Mississippi River
    
    11. Use shapefile_field_filler.py to add data from percents_and_ratios csv to shapefile fields.
    
    12. Color counties by their attirbutes (shapefile > symbology > categorized. Don't forget to click 
    'classify'!)

## Fire Frequency Map:

This map tracks how many times in the study period (1980 - 2022) a forest plot within the county was 
observed to have fire damage. 

## Data Used for the Fire Frequency Map:

This data comes from the plot table of the FIA database.

## Steps to Build the Fire Frequency Map:

    1. If you haven't already, follow steps 1-5 from the AM/EM Pipeline directions (The tree table is 
    not necessary if you only want fire data.)
    
    2. Use loop_fire_finder.py to create a CSV file with all the counties and their associated number 
    of burned plots 
    
    3. Convert the csv to an excel workbook for importing to arcgis pro
    
    4. Add shapefile to arcgis pro project as a new layer
    
    5. Add the fire data excel workbook to the arcgis pro project
    
    6. Add a column to the shapefile and a column to the fire data table that combines their state and 
    county codes into one value
    
    7. Join the table with the shapefile
    
    8. Color counties by the attribute firedplots

## Temperature and Precipitation Maps:

The temperature and precipitation maps track the mean annual temperature and precipitation for a given 
county.

## Data Used for the Temperature and Precipitation Maps:

Data for these maps is from 30 Year Normals datasets provided by the PRISM Climate Group. 

## Steps to Build the Temperature and Precipitation Maps:

    1. Go to https://prism.oregonstate.edu/normals/
    
    2. Choose precipitation or temperature and select Download Data (.asc)
    
    3. Unzip the folder
    
    4. On a new map in ArcGIS Pro, click add data. Select the Raster Dataset from the folder you just 
    unzipped
    
    5. Export the raster and remove the original file from the GIS project
    
    6. Add a layer with the East US shapefile. (see the AM/EM pipeline directions for more details)
    
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

    4. Use annual_n_deposition_by_site.sql on the tables to find kg/ha/yr of N deposited at each 
    latitude and longitude

    5. Save the results to a csv file

    6. Add data from the csv file to your map in ArcGIS Pro

    7. Create Points from table

    8. Do DWI on the points to make a raster (cell size should be small. I settled on 0.1)

    9. Add your counties shapefile

    10. Do raster to points conversion

    11. Do a spatial join between the shapefile and the points

    12. Color your counties based on the resulting values in the shapefile's attirbute table (kg/ha/yr 
    from 1980 to 2022)

## Ecoregions Map:

The ecoregions map assigns an ecoregion to each county in the eastern United States.

## Data Used for the Ecoregions Map:

This map uses a raster provided by the US Forestry Service, delineating the ecoregions of the US.

## Steps to Build the Ecoregions Map:

    1. At https://data.fs.usda.gov/geodata/edw/datasets.php?dsetCategory=geoscientificinformation 
    download Ecological Provinces shapefile
    
    2. Add the raster layer to your map
    
    3. Add the shapefile for counties to your map
    
    4. Clip the raster to the size of the counties shapefile
    
    5. Create a python notebook  
    
    6. Run assign_regions_to_counties.py in the notebook
    
    7. Assign colors to the layer based on region_id

