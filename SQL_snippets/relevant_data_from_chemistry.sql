-- This query uses the chemistry table, which is made using NTN-ALL-a-s-dep.csv from https://nadp.slh.wisc.edu/networks/national-trends-network/
-- All values of -9 must be made null before this query will work properly.

-- This query grabs only relevant data from the chemistry table.
-- The query excludes years outside our range and years where there is not totaln data 
-- It also excludes years where less than 180 days of data was collected

SELECT siteid, yr, totaln, criteria1, dayssample 
FROM chemistry 
WHERE totaln IS NOT NULL
AND yr > 1979 AND yr < 2023
AND dayssample > 180;
