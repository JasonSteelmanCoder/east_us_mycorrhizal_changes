-- inspect the species that have values from Pellegrini to identify any duplicates
SELECT scientific_name, bark_dbh_ratio, bark_dbh_source, mm_bt_in_10cm_tree
FROM fire_characteristics 
INNER JOIN pellegrini 
ON LOWER(TRIM(BOTH ' ' FROM fire_characteristics.scientific_name)) = LOWER(TRIM(BOTH ' ' FROM pellegrini.species))
ORDER BY bark_dbh_source



-- update species with data from Pellegrini
UPDATE fire_characteristics
SET bark_dbh_source = 'Pellegrini 2017', bark_dbh_ratio = (pellegrini.mm_bt_in_10cm_tree * 0.01)
FROM pellegrini
WHERE
	bark_dbh_ratio IS NULL
  AND bark_dbh_source IS NULL
	AND LOWER(TRIM(BOTH ' ' FROM fire_characteristics.scientific_name)) = LOWER(TRIM(BOTH ' ' FROM pellegrini.species))