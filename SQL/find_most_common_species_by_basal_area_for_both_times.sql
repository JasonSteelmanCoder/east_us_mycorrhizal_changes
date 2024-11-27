WITH plot_cns AS (
	WITH RECURSIVE plot_cte AS (
		-- grab a list of plot_cn's matched with their original cn
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
	-- grab a list of plot_cn's matched with their original cn
	SELECT 
		plot_cte.original_cn, 
		UNNEST(plot_cte.cn_sequence) AS alias_cn
	FROM plot_cte
	JOIN obs_nums
	ON 
		plot_cte.original_cn = obs_nums.original_cn
		AND ARRAY_LENGTH(plot_cte.cn_sequence, 1) = obs_nums.num

), basals_by_plot_obs AS (
	-- find basal areas of each species for each observation of a plot	
	SELECT 
		eut.plt_cn,
		eut.spcd,
		ROUND(SUM(((PI() * (eut.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal), 6) AS basal_area
	FROM east_us_tree eut
	JOIN east_us_cond euc
	ON 
		euc.plt_cn = eut.plt_cn
		AND euc.condid = eut.condid 
	WHERE 
		eut.invyr > 2014 AND eut.invyr < 2023		-- at T2
		AND euc.stdorgcd = 0 		-- exclude timberland
		AND eut.statuscd = 1	-- only count live trees
	GROUP BY 
		eut.plt_cn,
		eut.spcd

), avg_basal_by_plot AS (
	-- average the basal areas of all species in all observations to get average basal areas of each plot
	SELECT 
		original_cn,
		spcd,
		AVG(basal_area) AS mean_basal_area_on_plot
	FROM basals_by_plot_obs bpo
	JOIN plot_cns pcns
	ON bpo.plt_cn = pcns.alias_cn
	GROUP BY 
		original_cn,
		spcd
)
-- sum the plots to get basal areas for each species across the whole eastern US
SELECT 
	abp.spcd,
	common_name,
	genus,
	species,
	ROUND(SUM(mean_basal_area_on_plot), 6) AS basal_area
FROM avg_basal_by_plot abp
JOIN ref_species rs
ON abp.spcd = rs.spcd
GROUP BY 
	abp.spcd,
	common_name,
	genus,
	species
ORDER BY basal_area DESC
LIMIT 75


-- TODO: 
-- make basal area into proportion
-- repeat for T1





