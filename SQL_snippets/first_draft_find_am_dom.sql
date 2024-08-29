-- FIND AM DOMINANCE USING THE AVERAGE DOMINANCE OF EACH PLOT
-- (INCLUDE STANDARD ERROR OF COUNTY)
-- this first draft uses the earliest observation at T1 and the latest observation at T2. We later decided to take average values of plot observations during T1 and T2.
-- see find_am_dom.sql for the new code.

-- get the AM dom measurement for each plot in the county at T1
WITH plots AS (
	WITH trees AS (
    WITH min_year_of_plot AS (
      -- find the earliest year of observation for each plot
      SELECT MIN(invyr), east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd, east_us_plot.plot
      FROM east_us_plot
      WHERE east_us_plot.invyr > 1979 AND east_us_plot.invyr < 1999
      GROUP BY east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd, east_us_plot.plot
      ORDER BY east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd, east_us_plot.plot, min
    )
    -- grab all of the trees in the county that are part of a first observation
    SELECT east_us_tree.invyr, east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 3) as basal_area, east_us_tree.spcd, ref_species.association
    FROM east_us_tree 
    LEFT JOIN ref_species
    ON east_us_tree.spcd = ref_species.spcd
    LEFT JOIN east_us_cond
    ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot AND east_us_tree.invyr = east_us_cond.invyr AND east_us_tree.condid = east_us_cond.condid
    JOIN min_year_of_plot
    ON east_us_tree.invyr = min_year_of_plot.min AND east_us_tree.statecd = min_year_of_plot.statecd AND east_us_tree.unitcd = min_year_of_plot.unitcd AND east_us_tree.countycd = min_year_of_plot.countycd AND east_us_tree.plot::text = min_year_of_plot.plot::text 
    WHERE 

    east_us_tree.invyr > 1979 AND east_us_tree.invyr < 1999 AND										-- at T1

    east_us_tree.statecd = 13 AND  
    --east_us_tree.unitcd = {unitcd} AND
    east_us_tree.countycd = 59 AND 

    (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland
    east_us_tree.statuscd = 1			-- only count live trees

    ORDER BY statecd, unitcd, countycd, plot, subp, tree
  )
  -- grab plots and their associated AM and EM basal_areas
  SELECT 
    statecd, 
    unitcd, 
    countycd, 
    plot, 
    SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END) AS am_basal_area, 
    SUM(CASE WHEN association = 'EM' THEN basal_area ELSE 0 END) AS em_basal_area, 
    SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END)::DOUBLE PRECISION / (SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END) + SUM(CASE WHEN association != 'AM' THEN basal_area ELSE 0 END))::DOUBLE PRECISION AS am_dom
  FROM trees
  GROUP BY statecd, unitcd, countycd, plot
)
-- grab the county's average am dom, over all of its plots
SELECT statecd, unitcd, countycd, AVG(am_dom) AS am_dom_t1
FROM plots
GROUP BY statecd, unitcd, countycd
ORDER BY statecd, unitcd, countycd