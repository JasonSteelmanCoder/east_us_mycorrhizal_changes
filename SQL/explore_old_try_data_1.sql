SELECT 
	REGEXP_REPLACE(speciesname, '^(([^ ]+ ){2}).*$', '\1') AS speciesname, 
  ROUND(AVG(
    CASE
  		WHEN unitname = 'm' THEN stdvalue::DOUBLE PRECISION * 1000
    	ELSE stdvalue::DOUBLE PRECISION
  	END
  )::DECIMAL, 2) AS mean_bark_thickness
FROM old_try_data_1 
WHERE traitname = 'Bark thickness'
GROUP BY speciesname





WITH 
limited_trees AS (
	SELECT * FROM common_trees ORDER BY basal_area DESC LIMIT 70
)
SELECT 
	rank_by_basal_area,
	REGEXP_REPLACE(speciesname, '^(([^ ]+ ){2}).*$', '\1') AS speciesname, 
  ROUND(AVG(
    CASE
  		WHEN unitname = 'm' THEN stdvalue::DOUBLE PRECISION * 1000
    	ELSE stdvalue::DOUBLE PRECISION
  	END
  )::DECIMAL, 2) AS mean_bark_thickness
FROM limited_trees
INNER JOIN old_try_data_1 
ON 
	traitname = 'Bark thickness'
  AND LOWER(TRIM(REGEXP_REPLACE(speciesname, '^(([^ ]+ ){2}).*$', '\1'))) = LOWER(TRIM(limited_trees.genus || ' ' || limited_trees.species))
GROUP BY speciesname, rank_by_basal_area
ORDER BY rank_by_basal_area