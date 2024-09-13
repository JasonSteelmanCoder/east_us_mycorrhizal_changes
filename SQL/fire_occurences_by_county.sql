        SELECT 
        	east_us_plot.statecd, 
          east_us_plot.unitcd, 
          east_us_plot.countycd,
          SUM(
            CASE 
              WHEN
                (dstrbcd1 = 30 OR dstrbcd1 = 31 OR dstrbcd1 = 32
                or dstrbcd2 = 30  OR dstrbcd2 = 31 OR dstrbcd2 = 32
                or dstrbcd3 = 30  OR dstrbcd3 = 31 OR dstrbcd3 = 32 )
              THEN 1
              ELSE 0
            END 
          ) AS fire_observations,
          COUNT(DISTINCT east_us_plot.plot) AS plots,
          COUNT(east_us_plot.plot) AS observations
        FROM east_us_plot 
        LEFT JOIN east_us_cond 
        ON east_us_cond.plt_cn = east_us_plot.cn
        WHERE 
            east_us_plot.statecd = 12 AND east_us_plot.countycd = 3 AND
            east_us_plot.invyr > 1998 AND east_us_plot.invyr < 2023 AND
            (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0)
        GROUP BY east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd;