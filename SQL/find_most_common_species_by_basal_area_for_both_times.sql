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

), top_species AS (

	-- grab the list of top 75 species
	SELECT 
		spcd,
		fire_classification
	FROM fire_adaptation

), basals_by_plot_obs AS (


	-- find basal areas of each species for each observation of a plot
	-- only include species that are in the top 75
	-- also, note the time period of each observation
	SELECT 
		eut.plt_cn,
		eut.spcd,
		ts.fire_classification,
		ROUND(SUM(((PI() * (eut.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal), 6) AS basal_area,
		CASE
			WHEN eut.invyr > 1979 AND eut.invyr < 1999
			THEN 1
			WHEN eut.invyr > 2014 AND eut.invyr < 2023
			THEN 2
			ELSE NULL
		END AS time_period
	FROM east_us_tree eut
	JOIN top_species ts
	ON 
		ts.spcd = eut.spcd			-- this filters out species that are not in the top 75
		AND ts.fire_classification IS NOT NULL		-- this filters out oxydendrum and salix
	JOIN east_us_cond euc
	ON 
		euc.plt_cn = eut.plt_cn
		AND euc.condid = eut.condid 
	WHERE 
		euc.stdorgcd = 0 		-- exclude timberland
		AND eut.statuscd = 1	-- only count live trees
	GROUP BY 
		eut.plt_cn,
		eut.spcd,
		ts.fire_classification,
		eut.invyr
		
), avg_basal_for_species_plot_time_period AS (
	-- average the basal areas of top species in all observations to get average basal areas of each species in each plot in each time period
	SELECT 
		original_cn,
		bpo.time_period,
		spcd,
		fire_classification,
		AVG(basal_area) AS mean_basal_area_on_plot
	FROM basals_by_plot_obs bpo
	JOIN plot_cns pcns
	ON bpo.plt_cn = pcns.alias_cn
	WHERE 
		bpo.time_period IS NOT NULL			-- the observation should be during T1 or T2
	GROUP BY 
		original_cn,
		spcd,
		bpo.fire_classification,
		bpo.time_period
), county_values AS (
	-- add county information and average by county
	SELECT 
		eup.statecd,
		eup.unitcd,
		eup.countycd,
		abspt.time_period,
		abspt.spcd,
		abspt.fire_classification,
		SUM(abspt.mean_basal_area_on_plot) AS basal_area_in_county		-- this is the sum of the mean basal areas for every plot in the county in the time period
	FROM avg_basal_for_species_plot_time_period abspt
	JOIN east_us_plot eup
	ON eup.cn = abspt.original_cn
	GROUP BY 
		eup.statecd,
		eup.unitcd,
		eup.countycd,
		abspt.time_period,
		abspt.spcd,
		abspt.fire_classification
), adapted_basal_areas AS (
	-- find sums of fire-adapted and intolerant basal areas for each county
	SELECT 
		statecd, 
		unitcd, 
		countycd, 
		time_period,
		fire_classification,
		SUM(basal_area_in_county) AS basal_area_in_county
	FROM county_values cv
	GROUP BY 
		statecd,
		unitcd,
		countycd,
		time_period,
		fire_classification
), proportions AS (
	-- find proportions of adapted and intolerant
	SELECT 
		statecd,
		unitcd,
		countycd,
		time_period,
		fire_classification,
		basal_area_in_county,
		ROUND(basal_area_in_county / SUM(basal_area_in_county) OVER (
			PARTITION BY 
				statecd, 
				unitcd,
				countycd,
				time_period
		), 2) AS proportion_of_county_basal_area
	FROM adapted_basal_areas aba
), t1 AS (
	-- separate out time period 1
	SELECT * 
	FROM proportions 
	WHERE time_period = 1
), t2 AS (
	-- separate out time period 2
	SELECT * 
	FROM proportions
	WHERE time_period = 2
), grouped_by_tolerance AS (
	-- join t1 and t2 to allow comparison
	SELECT 
		COALESCE(t1.statecd, t2.statecd) AS statecd,
		COALESCE(t1.unitcd, t2.unitcd) AS unitcd,
		COALESCE(t1.countycd, t2.countycd) AS countycd,
		COALESCE(t1.fire_classification, t2.fire_classification) AS fire_classification,
		t1.proportion_of_county_basal_area AS t1_proportion,
		t2.proportion_of_county_basal_area AS t2_proportion
	FROM t1
	FULL OUTER JOIN t2 
	ON 
		t1.statecd = t2.statecd
		AND t1.unitcd = t2.unitcd
		AND t1.countycd = t2.countycd
		AND t1.fire_classification = t2.fire_classification
), adapted AS (
	-- separate out adapted
	SELECT * 
	FROM grouped_by_tolerance
	WHERE fire_classification = 'adapted'
), intolerant AS (
	-- separate out intolerant
	SELECT * 
	FROM grouped_by_tolerance
	WHERE fire_classification = 'intolerant'
), fully_joined AS (
	-- join adapted and intolerant
	SELECT
		COALESCE(ad.statecd, intol.statecd) AS statecd,
		COALESCE(ad.unitcd, intol.unitcd) AS unitcd,
		COALESCE(ad.countycd, intol.countycd) AS countycd,
		ad.t1_proportion AS t1_adapted,
		intol.t1_proportion AS t1_intolerant,
		ad.t2_proportion AS t2_adapted,
		intol.t2_proportion AS t2_intolerant
	FROM adapted ad
	FULL OUTER JOIN intolerant intol 
	ON 
		ad.statecd = intol.statecd
		AND ad.unitcd = intol.unitcd
		AND ad.countycd = intol.countycd
), prepared_data AS (
	-- add zeros in places where the counterpart is 1
	SELECT 
		statecd,
		unitcd,
		countycd,
		CASE
			WHEN t1_intolerant = 1
			THEN 0
			ELSE t1_adapted
		END AS t1_adapted,
		CASE
			WHEN t1_adapted = 1
			THEN 0
			ELSE t1_intolerant
		END AS t1_intolerant,
		CASE
			WHEN t2_intolerant = 1
			THEN 0
			ELSE t2_adapted
		END AS t2_adapted,
		CASE
			WHEN t2_adapted = 1
			THEN 0
			ELSE t2_intolerant
		END AS t2_intolerant	
	FROM fully_joined fj
)
-- grab the delta adapted dominance for each county
SELECT 
	statecd,
	unitcd,
	countycd,
	t2_adapted - t1_adapted AS delta_adapted_proportion  		-- a positive delta means an increase in adapted basal area from t1 to t2, negative means a decrease. Null means that data was missing for T1 or T2
FROM prepared_data pd





