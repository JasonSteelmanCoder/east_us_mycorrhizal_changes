SELECT  east_us_plot.invyr, east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot, dstrbcd1, dstrbcd2, dstrbcd3
FROM east_us_cond 
LEFT JOIN east_us_plot
ON east_us_cond.plt_cn = east_us_plot.cn
WHERE (dstrbcd1 = 30 OR dstrbcd1 = 31 OR dstrbcd1 = 32
or dstrbcd2 = 30  OR dstrbcd2 = 31 OR dstrbcd2 = 32
or dstrbcd3 = 30  OR dstrbcd3 = 31 OR dstrbcd3 = 32 )
AND east_us_plot.statecd = 51 AND east_us_plot.countycd = 65
ORDER BY east_us_plot.invyr, east_us_plot.plot;