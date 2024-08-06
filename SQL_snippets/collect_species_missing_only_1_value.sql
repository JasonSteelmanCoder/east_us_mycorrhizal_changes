WITH
viable_trees AS (
    SELECT scientific_name, flame_duration_s, percent_consumed, mean_litter_k, mean_litter_cn, bark_diameter_ratio, bark_vol_percent, smoulder_duration_s
    FROM fire_characteristics
    WHERE
        CASE WHEN flame_duration_s IS NOT NULL THEN 1 ELSE 0 END +
        CASE WHEN percent_consumed IS NOT NULL THEN 1 ELSE 0 END +
        CASE WHEN mean_litter_k IS NOT NULL THEN 1 ELSE 0 END +
        CASE WHEN mean_litter_cn IS NOT NULL THEN 1 ELSE 0 END +
        CASE WHEN bark_diameter_ratio IS NOT NULL THEN 1 ELSE 0 END +
  		CASE WHEN bark_vol_percent IS NOT NULL THEN 1 ELSE 0 END +
  		CASE WHEN smoulder_duration_s IS NOT NULL THEN 1 ELSE 0 END
  		= 6
)
SELECT DISTINCT  
    scientific_name,
    flame_duration_s, 
    percent_consumed, 
    mean_litter_k, 
    mean_litter_cn, 
    bark_diameter_ratio,
    bark_vol_percent,
    smoulder_duration_s,
    association, 
    fire_classification
FROM viable_trees
LEFT JOIN  common_trees
ON LOWER(TRIM(' ' FROM viable_trees.scientific_name)) = LOWER(TRIM(' ' FROM common_trees.genus || ' ' || common_trees.species))
LEFT JOIN species_associations 
ON LOWER(TRIM(BOTH ' ' FROM species_associations.species)) = LOWER(TRIM(BOTH ' ' FROM viable_trees.scientific_name))
LEFT JOIN fire_adaptation
ON LOWER(TRIM(' ' FROM viable_trees.scientific_name)) = LOWER(TRIM(' ' FROM fire_adaptation.genus || ' ' || fire_adaptation.species))
