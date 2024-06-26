SELECT STATECD, UNITCD, COUNTYCD, PLOT, INVYR
FROM plot 
WHERE INVYR > 1979 AND INVYR < 1996
GROUP BY STATECD, INVYR, UNITCD, COUNTYCD, PLOT
ORDER BY COUNTYCD, PLOT, INVYR;


-- SELECT STATECD, UNITCD, COUNTYCD, PLOT, INVYR
-- FROM plot 
-- WHERE INVYR > 2017 AND INVYR < 2023
-- GROUP BY STATECD, INVYR, UNITCD, COUNTYCD, PLOT
-- ORDER BY COUNTYCD, PLOT, INVYR; 