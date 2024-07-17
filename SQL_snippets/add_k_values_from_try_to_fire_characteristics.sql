WITH 
averages AS (
	SELECT speciesname, AVG(stdvalue) FROM cleaned_try_decomp WHERE stdvalue IS NOT NULL GROUP BY speciesname ORDER BY speciesname
)
UPDATE fire_characteristics
SET mean_litter_k = averages.avg
FROM averages
WHERE 
	mean_litter_k IS NULL
	AND LOWER(TRIM(BOTH ' ' FROM averages.speciesname)) = LOWER(TRIM(BOTH ' ' FROM fire_characteristics.scientific_name))
