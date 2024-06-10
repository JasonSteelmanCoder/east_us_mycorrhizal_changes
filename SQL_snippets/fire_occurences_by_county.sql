SELECT  east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd, COUNT(east_us_plot.invyr) AS fires
FROM east_us_cond 
LEFT JOIN east_us_plot
ON east_us_cond.plt_cn = east_us_plot.cn
WHERE 
	east_us_plot.statecd = 37 AND east_us_plot.countycd = 85 AND
  east_us_plot.invyr > 1979 AND east_us_plot.invyr < 2023 AND
  (dstrbcd1 = 30 OR dstrbcd1 = 31 OR dstrbcd1 = 32
  or dstrbcd2 = 30  OR dstrbcd2 = 31 OR dstrbcd2 = 32
  or dstrbcd3 = 30  OR dstrbcd3 = 31 OR dstrbcd3 = 32 )
GROUP BY east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd;