-- find total basal area for eastern US
WITH by_species AS (
  SELECT east_us_tree.spcd, ROUND(SUM(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal), 4) AS basal_area
  FROM east_us_tree 
  LEFT JOIN east_us_cond
  ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot  AND east_us_tree.invyr = east_us_cond.invyr AND east_us_tree.condid = east_us_cond.condid 

  WHERE 

  east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2023 AND									-- in T2

  (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland            
  east_us_tree.statuscd = 1			-- only count live trees            

  GROUP BY east_us_tree.spcd
  ORDER BY basal_area DESC
)
SELECT SUM(basal_area) AS total_basal_area FROM by_species



-- find percent of hemi-national total basal area for each species
WITH 
spcd_by_basal AS (

  -- grab all of the species id's with their basal_areas in T2
  SELECT east_us_tree.spcd, ROUND(SUM(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal), 4) AS basal_area
  FROM east_us_tree 
  LEFT JOIN east_us_cond
  ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot  AND east_us_tree.invyr = east_us_cond.invyr AND east_us_tree.condid = east_us_cond.condid 

  WHERE 

  east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2023 AND									-- in T2

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
  
  ROUND((basal_area::decimal / 87718.6749) * 100, 5) AS pct_of_basal
FROM spcd_by_basal
INNER JOIN ref_species
ON ref_species.spcd = spcd_by_basal.spcd
ORDER BY pct_of_basal DESC




-- find percent of hemi-national total basal area for each species in the 73 (excluding oxydendron and salix)
WITH 
spcd_by_basal AS (

  -- grab all of the species id's with their basal_areas in T2
  SELECT east_us_tree.spcd, ROUND(SUM(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal), 4) AS basal_area
  FROM east_us_tree 
  LEFT JOIN east_us_cond
  ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot  AND east_us_tree.invyr = east_us_cond.invyr AND east_us_tree.condid = east_us_cond.condid 

  WHERE 

  east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2023 AND									-- in T2

  (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland            
  east_us_tree.statuscd = 1			-- only count live trees    
  
  AND east_us_tree.spcd NOT IN (922, 711)		-- exclude oxydendron and salix

  GROUP BY east_us_tree.spcd
  ORDER BY basal_area DESC

)
SELECT 
	spcd_by_basal.spcd, 
  scientific_name,
  basal_area, 
  
  -- MAKE SURE YOU CHANGE THE TOTAL BASAL AREA IN THE LINE BELOW WHEN CHANGING TIMEFRAMES!
  
  ROUND((basal_area::decimal / 87718.6749) * 100, 1) AS pct_of_basal
FROM spcd_by_basal
INNER JOIN ref_species
ON ref_species.spcd = spcd_by_basal.spcd
ORDER BY basal_area DESC
LIMIT 73



-- add up the percent of hemi-national basal area that is accounted for by our 73 species
WITH percents AS (
  WITH 
  spcd_by_basal AS (

    -- grab all of the species id's with their basal_areas in T2
    SELECT east_us_tree.spcd, ROUND(SUM(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal), 4) AS basal_area
    FROM east_us_tree 
    LEFT JOIN east_us_cond
    ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot  AND east_us_tree.invyr = east_us_cond.invyr AND east_us_tree.condid = east_us_cond.condid 

    WHERE 

    east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2023 AND									-- in T2

    (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland            
    east_us_tree.statuscd = 1			-- only count live trees    

    AND east_us_tree.spcd NOT IN (922, 711)		-- exclude oxydendron and salix

    GROUP BY east_us_tree.spcd
    ORDER BY basal_area DESC

  )
  SELECT 
    spcd_by_basal.spcd, 
    scientific_name,
    basal_area, 

    -- MAKE SURE YOU CHANGE THE TOTAL BASAL AREA IN THE LINE BELOW WHEN CHANGING TIMEFRAMES!

    ROUND((basal_area::decimal / 87718.6749) * 100, 1) AS pct_of_basal
  FROM spcd_by_basal
  INNER JOIN ref_species
  ON ref_species.spcd = spcd_by_basal.spcd
  ORDER BY basal_area DESC
  LIMIT 73
)
SELECT SUM(pct_of_basal) AS percent_basal_represented FROM percents

