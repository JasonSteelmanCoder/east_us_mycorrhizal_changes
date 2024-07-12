WITH
viable_trees AS (
	SELECT scientific_name, flame_duration_s, percent_consumed, mean_litter_k, mean_litter_cn, bark_dbh_ratio 
  FROM fire_characteristics
  WHERE
    flame_duration_s IS NOT NULL
    AND percent_consumed IS NOT NULL
    AND mean_litter_k IS NOT NULL
    AND mean_litter_cn IS NOT NULL
)
SELECT rank_by_basal_area, scientific_name, common_name, genus, species, flame_duration_s, percent_consumed, mean_litter_k, mean_litter_cn, bark_dbh_ratio	
FROM viable_trees
LEFT JOIN  common_trees
ON LOWER(TRIM(' ' FROM viable_trees.scientific_name)) = LOWER(TRIM(' ' FROM common_trees.genus || ' ' || common_trees.species))
ORDER BY rank_by_basal_area

-- sort trees by how many characteristics have values
WITH
viable_trees AS (
	SELECT scientific_name, flame_duration_s, percent_consumed, mean_litter_k, mean_litter_cn, bark_dbh_ratio
  FROM fire_characteristics
--  WHERE
--    flame_duration_s IS NOT NULL
--    AND percent_consumed IS NOT NULL
--    AND mean_litter_k IS NOT NULL
--    AND mean_litter_cn IS NOT NULL
)
SELECT rank_by_basal_area, scientific_name, common_name, genus, species,  
  	(CASE WHEN mean_litter_k IS NULL THEN 1 ELSE 0 END + CASE WHEN flame_duration_s IS NULL THEN 1 ELSE 0 END + CASE WHEN percent_consumed IS NULL THEN 1 ELSE 0 END + CASE WHEN mean_litter_cn IS NULL THEN 1 ELSE 0 END + CASE WHEN bark_dbh_ratio IS NULL THEN 1 ELSE 0 END) AS num_missing_values,
    flame_duration_s, percent_consumed, mean_litter_k, mean_litter_cn, bark_dbh_ratio
FROM viable_trees
LEFT JOIN  common_trees
ON LOWER(TRIM(' ' FROM viable_trees.scientific_name)) = LOWER(TRIM(' ' FROM common_trees.genus || ' ' || common_trees.species))
ORDER BY (
  CASE WHEN mean_litter_k IS NULL THEN 1 ELSE 0 END + CASE WHEN flame_duration_s IS NULL THEN 1 ELSE 0 END + CASE WHEN percent_consumed IS NULL THEN 1 ELSE 0 END + CASE WHEN mean_litter_cn IS NULL THEN 1 ELSE 0 END + CASE WHEN bark_dbh_ratio IS NULL THEN 1 ELSE 0 END
), rank_by_basal_area



SELECT common_name, scientific_name, genus, species, mean_bark_thickness_cm, bark_thickness_citation, bark_dbh_ratio, bark_dbh_source 
FROM fire_characteristics
ORDER BY bark_dbh_ratio



SELECT * FROM duplicate_sources