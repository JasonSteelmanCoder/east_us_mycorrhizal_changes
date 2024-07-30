WITH
viable_trees AS (
    SELECT scientific_name, flame_duration_s, percent_consumed, mean_litter_k, mean_litter_cn, bark_diameter_ratio, bark_diameter_source 
    FROM fire_characteristics
    WHERE
        flame_duration_s IS NOT NULL
        AND percent_consumed IS NOT NULL
        AND mean_litter_k IS NOT NULL
        AND mean_litter_cn IS NOT NULL
        AND bark_diameter_ratio IS NOT NULL
)
SELECT DISTINCT 
    CASE WHEN association = 'AM' THEN '#5AB4AC' ELSE '#D8B365' END AS color_by_association, 
    scientific_name,
    flame_duration_s, 
    percent_consumed, 
    mean_litter_k, 
    mean_litter_cn, 
    bark_diameter_ratio
FROM viable_trees
LEFT JOIN  common_trees
ON LOWER(TRIM(' ' FROM viable_trees.scientific_name)) = LOWER(TRIM(' ' FROM common_trees.genus || ' ' || common_trees.species))
LEFT JOIN species_associations 
ON LOWER(TRIM(BOTH ' ' FROM species_associations.species)) = LOWER(TRIM(BOTH ' ' FROM viable_trees.scientific_name))
