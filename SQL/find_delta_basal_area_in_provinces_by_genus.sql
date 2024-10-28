WITH time_region_genus_percent AS (
	WITH time_region_genera AS (
		WITH tree_observations AS (
			-- grab all live tree observations on non-timberland conditions
			-- include information on their region and genus
			-- calculate basal area
			-- assign the tree observations to t1 or t2
			SELECT 
				CASE WHEN eup.invyr > 1979 AND eup.invyr < 1999 THEN 1 ELSE 2 END AS time_period,
				eur.statecd,
				eur.countycd,
				eup.plot,
				eup.invyr,
				eur.region_id,
				ROUND(((PI() * (eut.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 5) AS basal_area,
				rs.genus
			FROM east_us_region eur
			JOIN east_us_plot eup
			ON 
				eup.statecd = eur.statecd
				AND eup.countycd = eur.countycd
			JOIN east_us_tree eut
			ON 
				eut.statecd = eup.statecd
				AND eut.countycd = eup.countycd
				AND eut.plot = eup.plot
				AND eut.invyr = eup.invyr
			JOIN east_us_cond euc
			ON 
				euc.statecd = eut.statecd
				AND euc.countycd = eut.countycd
				AND euc.plot = eut.plot
				AND euc.invyr = eut.invyr
				AND euc.condid = eut.condid
			JOIN ref_species rs
			ON rs.spcd = eut.spcd
			WHERE 
				(eup.invyr > 1979 AND eup.invyr < 1999)
				OR
				(eup.invyr > 2014 AND eup.invyr < 2023)
				AND eut.statuscd = 1													-- tree must be live
				AND (euc.industrialcd_fiadb IS NULL OR euc.industrialcd_fiadb = 0)		-- condition must not be timberland
			ORDER BY 
				time_period,
				eur.statecd,
				eur.countycd,
				eup.plot,
				invyr
		)
		-- group by time period, region and genus, summing basal areas
		SELECT 
			time_period,
			region_id,
			genus,
			SUM(basal_area) AS basal_area
		FROM tree_observations tobs
		GROUP BY 
			time_period,
			region_id,
			genus
		ORDER BY 
			time_period,
			region_id,
			basal_area DESC
	)
	-- calculate percent of a region in a time period that is represented by each species
	SELECT 
		time_period,
		region_id,
		genus,
		basal_area,
		basal_area::DECIMAL / SUM(basal_area) OVER (
			PARTITION BY time_period, region_id
		) * 100 AS pct_of_bas_area_for_region_in_time_pd
	FROM time_region_genera trg
	ORDER BY 
		time_period,
		region_id,
		pct_of_bas_area_for_region_in_time_pd DESC
),
time_period_1 AS (
	-- grab all of the regions, genera, and percents for t1
	SELECT *
	FROM time_region_genus_percent trgp
	WHERE time_period = 1
),
time_period_2 AS (
	-- grab all of the regions, genera, and percents for t2
	SELECT *
	FROM time_region_genus_percent trgp
	WHERE time_period = 2
)
-- join t1 to t2, matching regions and genera
SELECT 
	COALESCE(t1.region_id, t2.region_id) AS region_id,
	COALESCE(t1.genus, t2.genus) AS genus,
	COALESCE(t1.pct_of_bas_area_for_region_in_time_pd, 0) AS t1_pct_of_bas_area_in_province,
	COALESCE(t2.pct_of_bas_area_for_region_in_time_pd, 0) AS t2_pct_of_bas_area_in_province,
	COALESCE(t2.pct_of_bas_area_for_region_in_time_pd, 0) - COALESCE(t1.pct_of_bas_area_for_region_in_time_pd, 0) AS delta_percent_of_bas_area_in_province
FROM time_period_1 t1
FULL OUTER JOIN time_period_2 t2
ON 
	t1.region_id = t2.region_id
	AND t1.genus = t2.genus
ORDER BY 
	region_id,
	delta_percent_of_bas_area_in_province DESC