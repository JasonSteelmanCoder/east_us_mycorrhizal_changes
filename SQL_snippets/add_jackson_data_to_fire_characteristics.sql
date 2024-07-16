-- inspect the rows that could be filled with Jackson data. This helps identify data that has more than one source.
SELECT scientific_name, fire_characteristics.bark_dbh_ratio, fire_characteristics.bark_dbh_source, jackson.bark_dbh_ratio 
FROM fire_characteristics
INNER JOIN jackson
ON LOWER(TRIM(BOTH ' ' FROM fire_characteristics.scientific_name)) = LOWER(TRIM(BOTH ' ' FROM jackson.species))
ORDER BY bark_dbh_source


-- update rows with Jackson data
UPDATE fire_characteristics
SET bark_dbh_source = 'Jackson 1999', bark_dbh_ratio = jackson.bark_dbh_ratio
FROM jackson
WHERE 
	bark_dbh_source IS NULL
	AND fire_characteristics.bark_dbh_ratio IS NULL
  AND LOWER(TRIM(BOTH ' ' FROM fire_characteristics.scientific_name)) = LOWER(TRIM(BOTH ' ' FROM jackson.species))