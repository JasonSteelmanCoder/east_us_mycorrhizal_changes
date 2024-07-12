
UPDATE fire_characteristics
SET 
	bark_dbh_ratio = subquery.avg_stdvalue, 
	bark_dbh_source = 'TRY data 34741'
FROM ( 
  -- work from a version of cleaned_try_bark_diameter where each speckes is matched with its average stdvalue
	SELECT accspeciesname, AVG(stdvalue) AS avg_stdvalue FROM cleaned_try_bark_diameter GROUP BY accspeciesname
) AS subquery
WHERE 
	bark_dbh_ratio IS NULL
  AND LOWER(TRIM(BOTH ' ' FROM fire_characteristics.scientific_name)) = LOWER(TRIM(BOTH ' ' FROM subquery.accspeciesname))




UPDATE fire_characteristics
SET 
	mean_litter_cn = subquery.avg_stdvalue, 
	litter_citation = CASE
  	WHEN litter_citation IS NOT NULL THEN litter_citation || ' c:n from TRY data 34741'
    ELSE 'c:n from TRY data 34741'
  END
FROM ( 
    -- work from a version of cleaned_try_c_n where each species has its average stdvalue
	SELECT accspeciesname, AVG(stdvalue) AS avg_stdvalue FROM cleaned_try_c_n GROUP BY accspeciesname
) AS subquery
WHERE 
	mean_litter_cn IS NULL
  AND LOWER(TRIM(BOTH ' ' FROM fire_characteristics.scientific_name)) = LOWER(TRIM(BOTH ' ' FROM subquery.accspeciesname))