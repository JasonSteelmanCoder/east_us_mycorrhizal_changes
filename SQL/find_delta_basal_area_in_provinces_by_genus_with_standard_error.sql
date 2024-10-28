WITH delta_county_basal_areas AS (
	WITH time_county_genus_pct AS (
		WITH time_county_genus_basal AS (
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
					AND rs.genus != 'Tree'													-- tree must have an identified species
					AND (euc.industrialcd_fiadb IS NULL OR euc.industrialcd_fiadb = 0)		-- condition must not be timberland
				ORDER BY 
					time_period,
					eur.statecd,
					eur.countycd,
					eup.plot,
					invyr
			)
			-- group by time period, county, region and genus. sum basal areas. 
			-- the resulting rows are basal areas of genera in each county in each time period
			SELECT 
				time_period,
				statecd,
				countycd,
				region_id,
				genus,
				SUM(basal_area) AS basal_area
			FROM tree_observations tobs
			GROUP BY 
				time_period,
				statecd,
				countycd,
				region_id,
				genus
			ORDER BY 
				time_period,
				statecd,
				countycd,
				basal_area DESC
		)
		-- add column for percent of county's basal area
		SELECT 
			time_period,
			statecd,
			countycd,
			region_id,
			genus,
			(basal_area / SUM(basal_area) OVER (
				PARTITION BY time_period, statecd, countycd, region_id
			)) * 100 AS pct_of_county_basal
		FROM time_county_genus_basal tcgb
	),
	time_period_1 AS (
		-- grab all rows in t1
		SELECT * 
		FROM time_county_genus_pct
		WHERE time_period = 1
	),
	time_period_2 AS (
		-- grab all rows in t2
		SELECT * 
		FROM time_county_genus_pct
		WHERE time_period = 2
	)	
	-- outer join t1 and t2, matching counties and genera
	SELECT 
		COALESCE(t1.statecd, t2.statecd) AS statecd,
		COALESCE(t1.countycd, t2.countycd) AS countycd,
		COALESCE(t1.region_id, t2.region_id) AS region_id, 
		COALESCE(t1.genus, t2.genus) AS genus, 
		COALESCE(t1.pct_of_county_basal, 0) AS t1_pct_of_county,
		COALESCE(t2.pct_of_county_basal, 0) AS t2_pct_of_county,
		COALESCE(t2.pct_of_county_basal, 0) - COALESCE(t1.pct_of_county_basal, 0) AS delta_county_basal_area
	FROM time_period_1 t1
	FULL OUTER JOIN time_period_2 t2
	ON 
		t1.statecd = t2.statecd
		AND t1.countycd = t2.countycd
		AND t1.region_id = t2.region_id
		AND t1.genus = t2.genus
)
-- group by region and genus, averaging delta_county_basal_area and finding the standard error
SELECT 
	region_id,
	genus,
	AVG(delta_county_basal_area) AS mean_delta_basal_area,
	STDDEV_SAMP(delta_county_basal_area) / SQRT(COUNT(delta_county_basal_area)) AS std_error_of_counties_w_this_genus_in_the_province
FROM delta_county_basal_areas dcba
GROUP BY 
	region_id,
	genus
ORDER BY 
	region_id,
	mean_delta_basal_area DESC


