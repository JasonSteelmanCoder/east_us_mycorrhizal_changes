-- find all common trees that don't have data from the spreadsheet
WITH 
limited_trees AS (
	SELECT * FROM common_trees ORDER BY basal_area DESC LIMIT 70
)
SELECT rank_by_basal_area, limited_trees.spcd, limited_trees.common_name, limited_trees.genus, limited_trees.species, limited_trees.basal_area, flame_duration_s, percent_consumed
FROM limited_trees
LEFT JOIN fire_characteristics 
ON fire_characteristics.fia_species_code = limited_trees.spcd
WHERE percent_consumed IS NULL
ORDER BY percent_consumed 



-- find all common trees that don't have data from TRY
WITH 
limited_trees AS (
	SELECT * FROM common_trees ORDER BY basal_area DESC LIMIT 70
)
SELECT rank_by_basal_area, limited_trees.spcd, limited_trees.common_name, limited_trees.genus, limited_trees.species, limited_trees.basal_area, litter_decomp_rate, litter_c_n, bark_thickness_per_diameter
FROM limited_trees
LEFT JOIN try_data 
ON LOWER(TRIM(' ' FROM accspeciesname)) = LOWER(TRIM (' ' FROM (limited_trees.genus::text || ' ' || limited_trees.species::text)))
WHERE litter_decomp_rate IS NULL
ORDER BY rank_by_basal_area

 



-- find all common trees that have data from the spreadsheet AND data from TRY
WITH 
limited_trees AS (
	SELECT * FROM common_trees ORDER BY basal_area DESC LIMIT 70
)
SELECT rank_by_basal_area, fia_species_code, fire_characteristics.common_name, scientific_name, fire_characteristics.genus, fire_characteristics.species, flame_duration_s, percent_consumed, litter_decomp_rate, litter_c_n, bark_thickness_per_diameter
FROM fire_characteristics
INNER JOIN try_data
ON LOWER(TRIM(' ' FROM accspeciesname)) = LOWER(TRIM(' ' FROM scientific_name))
INNER JOIN limited_trees
ON LOWER(TRIM(' ' FROM accspeciesname)) = LOWER(TRIM(' ' FROM (limited_trees.genus::text || ' ' || limited_trees.species::text)))
WHERE flame_duration_s IS NOT NULL
ORDER BY rank_by_basal_area