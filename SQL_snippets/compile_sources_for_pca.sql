SELECT 
	fire_characteristics.scientific_name, 
  association, 
  fire_classification, 
  pct_of_basal, 
  percent_consumed, 
  smoulder_duration_s, 
  fire_trait_citation, 
  mean_litter_cn,
  mean_litter_cn_source,
  mean_litter_k,
  mean_litter_k_source,
  bark_diameter_ratio, 
  bark_diameter_source
FROM fire_characteristics
INNER JOIN ref_species 
ON ref_species.spcd = fire_characteristics.fia_species_code
INNER JOIN fire_adaptation 
ON fire_adaptation.spcd = fire_characteristics.fia_species_code
INNER JOIN basal_areas 
ON basal_areas.spcd = fire_characteristics.fia_species_code
WHERE 
	percent_consumed IS NOT NULL
  AND smoulder_duration_s IS NOT NULL
  AND mean_litter_cn IS NOT NULL
  AND mean_litter_k IS NOT NULL
  AND bark_diameter_ratio IS NOT NULL
ORDER BY pct_of_basal DESC