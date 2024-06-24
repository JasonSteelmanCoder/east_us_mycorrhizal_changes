-- This query uses ntn.csv as sites, and NTN-ALL-a-s-dep.csv as chemistry. Both files are downloaded from https://nadp.slh.wisc.edu/networks/national-trends-network/ . 

SELECT sites.siteid, latitude, longitude, COUNT(yr) AS num_years, MIN(yr) AS start_year, MAX(yr) AS end_year
FROM chemistry 
JOIN sites 
ON chemistry.siteid = sites.siteid
WHERE totaln IS NOT NULL          -- exclude sites/years with missing N data
AND yr > 1979 AND yr < 2023           -- constrain the years to the years of our project
AND dayssample > 180              -- exclude "years" where the experiment lasted less than 6 months
GROUP BY sites.siteid, latitude, longitude
ORDER BY sites.siteid, num_years DESC;