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

Steps to build map:

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
    
    9. Find the basal area of AM and basal area of EM trees for each county and compare them
    
    use loop_ratio_finder.py to populate a csv with basal areas and change
    
    download shapefiles and remove unnecessary counties
    
    add data from percents_and_ratios csv to shapefile fields (shapefile_field_filler.py)
    
    color counties by their attirbutes (shapefile > symbology > categorized. Don't forget to click 'classify'!)


