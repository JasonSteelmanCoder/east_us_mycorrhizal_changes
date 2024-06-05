Introduction:

This project uses the FIA database to track changes in the dominance of arbuscular 
mycorrhizal (AM) versus ectomycorrhizal (EM) trees in the eastern United States from a T1 of 1980-1998 
through a T2 of 2015-2022. Recorded changes are used to build a county-by-county map of the 
26 states east of the Mississippi River, in which color indicates the difference over time in 
the dominance of AM and EM species. 

Data Used:

The majority of the data used in this project comes from the FIA database, and can be 
downloaded for free at https://apps.fs.usda.gov/fia/datamart/datamart.html. 

For each state, you will need three tables: TREE, PLOT, and COND from FIA Datamart. You will also need the 
REF_SPECIES table. Detailed descriptions of these tables can be found at 
https://www.fs.usda.gov/research/sites/default/files/2023-11/wo-fiadb_user_guide_p2_9-1_final.pdf.

Data on the mycorrhizal affiliation of various tree genera come largely from the works of 
Brundrett and Tedersoo and of Akhmetzhanova, Soudzilovskaia, et al. (https://esapubs.org/archive/ecol/E093/059/)
Relevant data from these two sources have been included for your convenience as 
mycorrhiza_brundrett_tedersoo.csv and mycorrhiza_akhmetzhanova.csv. Other trees are 
classified in the file called mycorrhiza_mkt.csv. The original sources for those 
classifications are included in the `source` column of that table.

Steps:

    download plot, tree, and cond csv files
    for each plot file, tree file, and cond file: (using converter_looper.py, copier_looper.py, and alterer_looper.py)
    use python to write a sql query that creates a table with the csv files' columns (csv_to_sql_converter.py)
    copy the sql query over to populate a table with column names
    use sql 'COPY FROM' to copy the data into the tables from the csv
    combine the by-state plot, tree, and cond tables into one East-US table for plot and one for tree
    copy mycorrhizal associations into database from Brundrett and Tedersoo paper and from 'rediscovered treasures' paper
    download REF_SPECIES from datamart and insert it into database with python and sql (csv_to_sql_converter.py again)
    add `association` column to REF_SPECIES using SQL (data from tedersoo and from "a rediscovered treasure" at https://esapubs.org/archive/ecol/E093/059/ and on desktop as myco_db) (assign_associations_to_species_nums_in_REF_SPECIES.sql)
    find the basal area of am and basal area of em trees for each county and compare them
    use loop_ratio_finder.py to populate a csv with basal areas and change
    download shapefiles and remove unnecessary counties
    add data from percents_and_ratios csv to shapefile fields (shapefile_field_filler.py)
    color counties by their attirbutes (shapefile > symbology > categorized. Don't forget to click 'classify'!)

