WITH 
spcd_by_basal AS (

  SELECT east_us_tree.spcd, ROUND(SUM(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal), 2) AS basal_area
  FROM east_us_tree 
  LEFT JOIN east_us_cond
  ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot

  WHERE 

  east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2023 AND									-- at T2

  (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland            
  east_us_tree.statuscd = 1			-- only count live trees            

  GROUP BY east_us_tree.spcd
  ORDER BY basal_area DESC

)
SELECT spcd_by_basal.spcd, common_name, genus, species, spcd_by_basal.basal_area
FROM spcd_by_basal
JOIN ref_species
ON spcd_by_basal.spcd = ref_species.spcd
ORDER BY basal_area DESC;