--UPDATE ecological_groups
--SET ecological_group = NULL;

WITH 
assigned AS (
  SELECT worm_sp_occur_phillips.family, worm_sp_occur_phillips.genus, worm_sp_occur_phillips.speciesbinomial, worm_sp_occur_phillips.ecological_group 
  FROM ecological_groups
  JOIN worm_sp_occur_phillips
  ON ecological_groups.family = worm_sp_occur_phillips.family AND ecological_groups.genus = worm_sp_occur_phillips.genus AND ecological_groups.name = worm_sp_occur_phillips.speciesbinomial
  WHERE worm_sp_occur_phillips.ecological_group != 'Unknown'
  GROUP BY worm_sp_occur_phillips.family, worm_sp_occur_phillips.genus, worm_sp_occur_phillips.speciesbinomial, worm_sp_occur_phillips.ecological_group 
  ORDER BY worm_sp_occur_phillips.family, worm_sp_occur_phillips.genus, worm_sp_occur_phillips.speciesbinomial, worm_sp_occur_phillips.ecological_group 
) 
UPDATE ecological_groups
SET ecological_group = assigned.ecological_group
FROM assigned
WHERE 
	ecological_groups.family = assigned.family 
  AND ecological_groups.genus = assigned.genus
  AND ecological_groups.name = assigned.speciesbinomial;

-- Add some ecological group assignments based on manual inspection of the Phillips data
UPDATE ecological_groups
SET ecological_group = 'Epi-Endogeic'
WHERE name = 'Metaphire houletti';		-- not automatically assigned because of a typo where an extra 't' was inserted in the Drake data

UPDATE ecological_groups
SET name = 'Metaphire houleti'
WHERE name = 'Metaphire houletti'; 		-- fix typo from Drake data

UPDATE ecological_groups
SET ecological_group = 'Epi-Endogeic'
WHERE name = 'Dichogaster bolaui ';		-- not automatically assigned because of a trailing space in the Drake data

UPDATE ecological_groups
SET name = 'Dichogaster bolaui'
WHERE name = 'Dichogaster bolaui '; 		-- fix trailing space from Drake data

UPDATE ecological_groups
SET ecological_group = 'Epigeic'
WHERE name = 'Lumbricus cf. rubellus';		-- The 'cf.' prevents automatic assignment, but this worm was most likely found at a layer resembling that of the epigeic group

UPDATE ecological_groups
SET ecological_group = 'Endogeic'
WHERE name = 'Pontoscolex corethrurus';		-- The `speciesbinomial` in Phillips matches the `name` in Drake.

UPDATE ecological_groups
SET ecological_group = 'Endogeic'
WHERE name = 'Allolobophoridella eiseni';		-- The `speciesbinomial` in Phillips matches the `name` in Drake.

