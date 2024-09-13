WITH associations 
AS (
  SELECT ref_species.spcd, association FROM ref_species
)

SELECT east_us_tree.spcd, associations.association 
FROM east_us_tree LEFT JOIN associations ON associations.spcd = east_us_tree.spcd 
WHERE 
	statecd = 23 AND countycd = 3 AND 
  invyr > 1979 AND invyr < 1996 AND
  
  -- invyr > 2017 AND invyr < 2023 AND
  
  statuscd = 1
  
GROUP BY east_us_tree.spcd, associations.association
;