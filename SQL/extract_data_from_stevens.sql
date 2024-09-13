WITH prepared_names AS (
	SELECT REPLACE(scientific_name, '_', ' ') AS speciesname 
	FROM stevens_fire_characteristics
  ORDER BY speciesname
)
SELECT speciesname 
FROM prepared_names
INNER JOIN fire_characteristics
ON LOWER(TRIM(BOTH ' ' FROM prepared_names.speciesname)) = LOWER(TRIM(BOTH ' ' FROM fire_characteristics.scientific_name))



SELECT * 
FROM stevens_fire_characteristics 
WHERE scientific_name IN ('Abies_concolor', 'Picea_glauca', 'Pseudotsuga_menziesii')
