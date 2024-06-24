-- This query uses the chemistry table, which is made using NTN-ALL-a-s-dep.csv from https://nadp.slh.wisc.edu/networks/national-trends-network/
-- It also uses the site table, wich is made using the table 'ntn' from  https://nadp.slh.wisc.edu/networks/national-trends-network/
-- All values of -9 must be made null before this query will work properly.
-- criteria1 refers to "Percentage of the summary period for which there are valid samples."

WITH relevant_chem 
AS (
    SELECT siteid, yr, totaln, criteria1, dayssample 
    FROM chemistry 
    WHERE totaln IS NOT NULL          -- exclude sites/years with missing N data
    AND yr > 1979 AND yr < 2023           -- constrain the years to the years of our project
    AND dayssample > 180              -- exclude "years" where the experiment lasted less than 6 months
)
SELECT 
	relevant_chem.siteid, 
    latitude, 
    longitude, 
    SUM(totaln) AS cumul_n, 
    SUM(dayssample * criteria1 / 100) AS validdays,         -- multiply the timespan of the experiment by the percent of days with valid measurements
    ROUND((SUM(totaln)/(SUM(dayssample * criteria1 / 100)) * 365)::DECIMAL, 3) AS n_kg_ha_yr        -- find the daily n deposition, then multiply by 365 to annualize it
FROM relevant_chem 
LEFT JOIN sites 
ON relevant_chem.siteid = sites.siteid
GROUP BY relevant_chem.siteid, latitude, longitude;

