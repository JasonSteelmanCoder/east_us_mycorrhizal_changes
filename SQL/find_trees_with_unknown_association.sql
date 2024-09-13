-- FIND ACCOUNTED AND UNACCOUNTED NUMBERS FOR T1:

SELECT 

    ROUND(sum(CASE WHEN tot_bas_t1 = 'None' THEN 0 ELSE tot_bas_t1::double precision END)::decimal, 0) AS total_basal_area, 
  	
    ROUND(sum(CASE WHEN ambasar_t1 = 'None' THEN 0 ELSE ambasar_t1::double precision END + CASE WHEN embasar_t1 = 'None' THEN 0 ELSE embasar_t1::double precision END)::decimal, 0) AS accounted_for_basal_area, 
  
    ROUND((sum(CASE WHEN tot_bas_t1 = 'None' THEN 0 ELSE tot_bas_t1::double precision END) - sum(CASE WHEN ambasar_t1 = 'None' THEN 0 ELSE ambasar_t1::double precision END + CASE WHEN embasar_t1 = 'None' THEN 0 ELSE embasar_t1::double precision END))::DECIMAL, 0) AS unknown_basal_area
  
FROM east_us_percents_and_ratios;

-- FIND ACCOUNTED AND UNACCOUNTED NUMBERS FOR T2:

SELECT 

	ROUND(sum(CASE WHEN tot_bas_t2 = 'None' THEN 0 ELSE tot_bas_t2::double precision END)::decimal, 0) AS total_basal_area, 
  	
    ROUND(sum(CASE WHEN ambasar_t2 = 'None' THEN 0 ELSE ambasar_t2::double precision END + CASE WHEN embasar_t2 = 'None' THEN 0 ELSE embasar_t2::double precision END)::decimal, 0) AS accounted_for_basal_area, 
  
    ROUND((sum(CASE WHEN tot_bas_t2 = 'None' THEN 0 ELSE tot_bas_t2::double precision END) - sum(CASE WHEN ambasar_t2 = 'None' THEN 0 ELSE ambasar_t2::double precision END + CASE WHEN embasar_t2 = 'None' THEN 0 ELSE embasar_t2::double precision END))::DECIMAL, 0) AS unknown_basal_area
  
FROM east_us_percents_and_ratios;


-- FIND SPECIES FOR UNACCOUNTED:

SELECT east_us_tree.spcd, ref_species.common_name, ref_species.genus, ref_species.species, ref_species.association
FROM east_us_tree 
LEFT JOIN ref_species
ON east_us_tree.spcd = ref_species.spcd
LEFT JOIN east_us_cond
ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot
WHERE 

(east_us_tree.invyr > 1979 AND east_us_tree.invyr < 1999 OR										-- at T1
east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2023) AND										-- at T2

-- east_us_tree.statecd = 44 AND  
-- east_us_tree.unitcd = {unitcd} AND
-- east_us_tree.countycd = {countycd} AND 
            
(east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland
east_us_tree.statuscd = 1 AND			-- only count live trees 

-- association != 'AM' AND association != 'EM'
association IS NULL

GROUP BY east_us_tree.spcd, ref_species.common_name, ref_species.genus, ref_species.species, ref_species.association;





-- FIND ONLY THE GENERA
SELECT ref_species.genus
FROM east_us_tree 
LEFT JOIN ref_species
ON east_us_tree.spcd = ref_species.spcd
LEFT JOIN east_us_cond
ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot
WHERE 

(east_us_tree.invyr > 1979 AND east_us_tree.invyr < 1999 OR										-- at T1
east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2023) AND										-- at T2

-- east_us_tree.statecd = 44 AND  
-- east_us_tree.unitcd = {unitcd} AND
-- east_us_tree.countycd = {countycd} AND 
            
(east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland
east_us_tree.statuscd = 1 AND			-- only count live trees 

-- association != 'AM' AND association != 'EM'
association IS NULL

GROUP BY ref_species.genus;