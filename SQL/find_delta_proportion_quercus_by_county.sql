WITH plot_cns AS (


	WITH RECURSIVE plot_cte AS (
		-- find the original plot cn for each plot observation
		SELECT 
			cn AS original_cn,
			array[cn]::bigint[] AS cn_sequence
		FROM east_us_plot
		WHERE prev_plt_cn IS NULL
		
		UNION ALL
	
		SELECT 
			plot_cte.original_cn,
			plot_cte.cn_sequence || east_us_plot.cn
		FROM plot_cte
		JOIN east_us_plot
		ON east_us_plot.prev_plt_cn = plot_cte.cn_sequence[ARRAY_LENGTH(plot_cte.cn_sequence, 1)]
			
	), obs_nums AS (
		SELECT 
			original_cn, 
			MAX(ARRAY_LENGTH(cn_sequence, 1))  AS num
		FROM plot_cte
		GROUP BY original_cn
	)
	-- grab the original plot cn for each plot observation
	SELECT 
		plot_cte.original_cn, 
		UNNEST(plot_cte.cn_sequence) AS alias_cn
	FROM plot_cte
	JOIN obs_nums
	ON 
		plot_cte.original_cn = obs_nums.original_cn
		AND ARRAY_LENGTH(plot_cte.cn_sequence, 1) = obs_nums.num

), observations AS (
	-- grab quercus and non-quercus basal areas for each plot observation
	-- also, make note of the time period of the observation
	SELECT 
		eut.plt_cn,
		SUM(CASE 
			WHEN rs.genus = 'Quercus'
			THEN ((PI() * (eut.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal 
			ELSE 0
		END) AS quercus_basal_area,
		SUM(CASE 
			WHEN rs.genus != 'Quercus'
			THEN ((PI() * (eut.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal 
			ELSE 0
		END) AS other_basal_area,
		CASE
			WHEN eut.invyr > 1979 AND eut.invyr < 1999  
			THEN 1
			WHEN eut.invyr > 2014 AND eut.invyr < 2023 
			THEN 2
			ELSE NULL
		END AS time_period
	FROM east_us_tree eut
	JOIN east_us_cond euc
	ON 
		euc.plt_cn = eut.plt_cn
		AND euc.condid = eut.condid
	JOIN ref_species rs
	ON rs.spcd = eut.spcd
	WHERE
		euc.stdorgcd = 0 		-- exclude timberland
		AND eut.statuscd = 1	-- only count live trees
	GROUP BY 
		eut.plt_cn,
		eut.invyr
), plot_values AS (
	-- add an original-plot-cn column and group by it, averaging basal areas for each plot, for each time period
	SELECT
		original_cn,
		AVG(quercus_basal_area) mean_quercus_basal_area_for_plot,
		AVG(other_basal_area) AS mean_other_basal_area_for_plot,
		time_period
	FROM observations obs
	JOIN plot_cns pcns
	ON pcns.alias_cn = obs.plt_cn
	WHERE time_period IS NOT NULL		-- observations should be in T1 or T2
	GROUP BY 
		original_cn,
		time_period
), county_values AS (
	-- add county information, then group by county, summing the basal areas of the plots in each county and time period
	SELECT
		eup.statecd,
		eup.unitcd,
		eup.countycd,
		SUM(pv.mean_quercus_basal_area_for_plot) AS sum_of_quercus_basal_areas_in_county, 
		SUM(pv.mean_other_basal_area_for_plot) AS sum_of_other_basal_areas_in_county,
		pv.time_period
	FROM plot_values pv
	JOIN east_us_plot eup
	ON pv.original_cn = eup.cn
	GROUP BY 
		eup.statecd,
		eup.unitcd,
		eup.countycd,
		pv.time_period
), t1 AS (
	-- separate out the t1 rows
	SELECT *
	FROM county_values
	WHERE time_period = 1
), t2 AS (
	-- separate out the t2 rows
	SELECT *
	FROM county_values
	WHERE time_period = 2
), joined_counties AS (
	-- join t1 and t2 to allow comparison across time for each county
	SELECT
		COALESCE(t1.statecd, t2.statecd) AS statecd,
		COALESCE(t1.unitcd, t2.unitcd) AS unitcd,
		COALESCE(t1.countycd, t2.countycd) AS countycd,
		t1.sum_of_quercus_basal_areas_in_county AS t1_quercus_basal,
		t1.sum_of_other_basal_areas_in_county AS t1_other_basal,
		t2.sum_of_quercus_basal_areas_in_county AS t2_quercus_basal,
		t2.sum_of_other_basal_areas_in_county AS t2_other_basal
	FROM t1
	FULL OUTER JOIN t2 
	ON 
		t1.statecd = t2.statecd
		AND t1.unitcd = t2.unitcd
		AND t1.countycd = t2.countycd
)
-- find proportions for t1 and t2, then compare them
SELECT
	statecd,
	unitcd,
	countycd,
	t1_quercus_basal / (t1_quercus_basal + t1_other_basal) AS t1_proportion_quercus,
	t2_quercus_basal / (t2_quercus_basal + t2_other_basal) AS t2_proportion_quercus,
	(t2_quercus_basal / (t2_quercus_basal + t2_other_basal)) - (t1_quercus_basal / (t1_quercus_basal + t1_other_basal)) AS delta_proportion_quercus
FROM joined_counties jc





