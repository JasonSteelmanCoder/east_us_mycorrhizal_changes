WITH old_data AS (
  SELECT STATECD, UNITCD, COUNTYCD, PLOT, INVYR
  FROM plot 
  WHERE INVYR > 1979 AND INVYR < 1996
  GROUP BY STATECD, INVYR, UNITCD, COUNTYCD, PLOT
  ORDER BY COUNTYCD, PLOT, INVYR
), 
new_data AS (
  SELECT STATECD, UNITCD, COUNTYCD, PLOT, INVYR
  FROM plot 
  WHERE INVYR > 2017 AND INVYR < 2023
  GROUP BY STATECD, INVYR, UNITCD, COUNTYCD, PLOT
  ORDER BY COUNTYCD, PLOT
)
SELECT old_data.STATECD, old_data.UNITCD, old_data.COUNTYCD, old_data.PLOT, old_data.INVYR, new_data.INVYR
FROM old_data
INNER JOIN new_data
ON 
	old_data.statecd = new_data.statecd AND
    old_data.unitcd = new_data.unitcd AND
	old_data.countycd = new_data.countycd AND
	old_data.plot = new_data.plot
;
