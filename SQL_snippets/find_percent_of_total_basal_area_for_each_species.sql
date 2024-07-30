
WITH 
spcd_by_basal AS (

  SELECT east_us_tree.spcd, ROUND(SUM(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal), 2) AS basal_area
  FROM east_us_tree 
  LEFT JOIN east_us_cond
  ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot

  WHERE 

  east_us_tree.invyr > 1979 AND east_us_tree.invyr < 2023 AND									-- for duration

  (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland            
  east_us_tree.statuscd = 1			-- only count live trees            

  GROUP BY east_us_tree.spcd
  ORDER BY basal_area DESC

)
SELECT 
	spcd_by_basal.spcd, 
  scientific_name,
  basal_area, 
  
  -- MAKE SURE YOU CHANGE THE TOTAL BASAL AREA IN THE LINE BELOW WHEN CHANGING TIMEFRAMES!
  
  ROUND((basal_area::decimal / 2177806.18) * 100, 5) AS pct_of_basal
FROM spcd_by_basal
INNER JOIN ref_species
ON ref_species.spcd = spcd_by_basal.spcd
ORDER BY pct_of_basal DESC