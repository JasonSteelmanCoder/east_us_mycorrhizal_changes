-- find which trees have all four relevant values (bark_thickness_per_diameter is not ready yet)
SELECT scientific_name, flame_duration_s, percent_consumed, mean_litter_k, mean_litter_cn 
FROM fire_characteristics
WHERE
	flame_duration_s IS NOT NULL
  AND percent_consumed IS NOT NULL
  AND mean_litter_k IS NOT NULL
  AND mean_litter_cn IS NOT NULL
  
  
-- match the trees that have all four relevant values (excluding bark_thickness_per_diameter) with their records in the common_trees table
-- (note that Tilia americana matches three different FIA records)
WITH
viable_trees AS (
	SELECT scientific_name, flame_duration_s, percent_consumed, mean_litter_k, mean_litter_cn 
  FROM fire_characteristics
  WHERE
    flame_duration_s IS NOT NULL
    AND percent_consumed IS NOT NULL
    AND mean_litter_k IS NOT NULL
    AND mean_litter_cn IS NOT NULL
)
SELECT * 
FROM viable_trees
LEFT JOIN  common_trees
ON LOWER(TRIM(' ' FROM viable_trees.scientific_name)) = LOWER(TRIM(' ' FROM common_trees.genus || ' ' || common_trees.species))
ORDER BY scientific_name



-- Find why mean_litter_cn has fewer values than other characteristics
SELECT scientific_name, flame_duration_s, percent_consumed, mean_litter_k, mean_litter_cn, mean_perc_litter_c, mean_perc_litter_n
FROM fire_characteristics
WHERE mean_litter_cn IS NULL