-- how many plots are observed once? twice? six times?
-- maybe a quarter of plots are only observed once.
WITH obs_counts AS (
  SELECT statecd, countycd, plot, count(plot) AS observations
  FROM east_us_plot 
  GROUP BY statecd, countycd, plot
  ORDER BY observations DESC
)
SELECT observations, COUNT(observations) AS num_plots
FROM obs_counts
GROUP BY observations
ORDER BY observations


-- what is the average number of times that a plot is visited?
-- around 2.6
WITH obs_counts AS (
  SELECT statecd, countycd, plot, count(plot) AS observations
  FROM east_us_plot 
  GROUP BY statecd, countycd, plot
  ORDER BY observations DESC
)
SELECT avg(observations) FROM obs_counts



-- when are the first and the last observations for plots with more than one observation? How far apart are they?
-- 1991, 2008, 16.6 years
WITH obs_counts AS (
  SELECT statecd, countycd, plot, count(plot) AS observations, MIN(invyr) AS first_obs, MAX(invyr) AS last_obs, MAX(invyr) - MIN(invyr) AS timespan
  FROM east_us_plot 
  GROUP BY statecd, countycd, plot
  ORDER BY observations DESC
)
SELECT AVG(first_obs), AVG(last_obs), AVG(timespan) FROM obs_counts WHERE observations > 1





-- assume that we want plots observed in the 90's and observed again in the 00's. how many plots will we have
-- 14,445 plots
WITH nineties AS (
  SELECT statecd, countycd, plot
  FROM east_us_plot 
  WHERE invyr > 1989 AND invyr < 2000
  GROUP BY statecd, countycd, plot
), noughties AS (
  SELECT statecd, countycd, plot
  FROM east_us_plot 
  WHERE invyr > 1999 AND invyr < 2010
  GROUP BY statecd, countycd, plot
)
SELECT nineties.statecd, nineties.countycd, nineties.plot 
FROM nineties
INNER JOIN noughties
ON nineties.statecd = noughties.statecd AND nineties.countycd = noughties.countycd AND nineties.plot = noughties.plot




-- are the plots from the 90's 00's example above geographically representative?
-- no. 16/26 states. some states have only 10's of plots
WITH viable_plots AS (
  WITH nineties AS (
    SELECT statecd, countycd, plot
    FROM east_us_plot 
    WHERE invyr > 1989 AND invyr < 2000
    GROUP BY statecd, countycd, plot
  ), noughties AS (
    SELECT statecd, countycd, plot
    FROM east_us_plot 
    WHERE invyr > 1999 AND invyr < 2010
    GROUP BY statecd, countycd, plot
  )
  SELECT nineties.statecd, nineties.countycd, nineties.plot 
  FROM nineties
  INNER JOIN noughties
  ON nineties.statecd = noughties.statecd AND nineties.countycd = noughties.countycd AND nineties.plot = noughties.plot
)
SELECT statecd, count(statecd)
FROM viable_plots
GROUP BY statecd
ORDER BY count DESC



-- assume that we want plots observed in the 70's/80's and observed again in the 90's/00's. how many plots will we have
-- 90,470 plots
WITH old_plots AS (
  SELECT statecd, countycd, plot
  FROM east_us_plot 
  WHERE invyr > 1969 AND invyr < 1990
  GROUP BY statecd, countycd, plot
), new_plots AS (
  SELECT statecd, countycd, plot
  FROM east_us_plot 
  WHERE invyr > 1989 AND invyr < 2010
  GROUP BY statecd, countycd, plot
)
SELECT old_plots.statecd, old_plots.countycd, old_plots.plot 
FROM old_plots
INNER JOIN new_plots
ON old_plots.statecd = new_plots.statecd AND old_plots.countycd = new_plots.countycd AND old_plots.plot = new_plots.plot




-- are the plots from the 70's/80's and 90's/00's example above geographically representative?
-- sort of. 21 states, with a decent number of counties each
WITH viable_plots AS (
  WITH old_plots AS (
    SELECT statecd, countycd, plot
    FROM east_us_plot 
    WHERE invyr > 1969 AND invyr < 1990
    GROUP BY statecd, countycd, plot
  ), new_plots AS (
    SELECT statecd, countycd, plot
    FROM east_us_plot 
    WHERE invyr > 1989 AND invyr < 2010
    GROUP BY statecd, countycd, plot
  )
  SELECT old_plots.statecd, old_plots.countycd, old_plots.plot 
  FROM old_plots
  INNER JOIN new_plots
  ON old_plots.statecd = new_plots.statecd AND old_plots.countycd = new_plots.countycd AND old_plots.plot = new_plots.plot
)
SELECT statecd, count(statecd)
FROM viable_plots
GROUP BY statecd
ORDER BY count DESC



-- what states are missing from the results above?
-- Georgia, Maine, New York, Ohio, Tennessee
WITH state_counts AS (
  WITH viable_plots AS (
    WITH old_plots AS (
      SELECT statecd, countycd, plot
      FROM east_us_plot 
      WHERE invyr > 1969 AND invyr < 1990
      GROUP BY statecd, countycd, plot
    ), new_plots AS (
      SELECT statecd, countycd, plot
      FROM east_us_plot 
      WHERE invyr > 1989 AND invyr < 2010
      GROUP BY statecd, countycd, plot
    )
    SELECT old_plots.statecd, old_plots.countycd, old_plots.plot 
    FROM old_plots
    INNER JOIN new_plots
    ON old_plots.statecd = new_plots.statecd AND old_plots.countycd = new_plots.countycd AND old_plots.plot = new_plots.plot
  )
  SELECT statecd, count(statecd)
  FROM viable_plots
  GROUP BY statecd
  ORDER BY count DESC
)
SELECT state_name 
FROM east_us_counties
LEFT JOIN state_counts
ON state_counts.statecd = east_us_counties.statecd
WHERE state_counts.statecd IS NULL
GROUP BY state_name



-- how many plots are there total?
-- 296,972 plots
SELECT statecd, countycd, plot 
FROM east_us_plot 
GROUP BY statecd, countycd, plot


-- how many conditions are there?
-- 3,160,166
SELECT east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 
FROM east_us_plot 
INNER JOIN east_us_cond
ON east_us_plot.statecd = east_us_cond.statecd AND east_us_plot.countycd = east_us_cond.countycd AND east_us_plot.plot = east_us_cond.plot


-- how many plots have corresponding conditions?
-- 296,972 plots. i.e. all of them.
SELECT east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 
FROM east_us_plot 
INNER JOIN east_us_cond
ON east_us_plot.statecd = east_us_cond.statecd AND east_us_plot.countycd = east_us_cond.countycd AND east_us_plot.plot = east_us_cond.plot
GROUP BY east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 


-- what states have plots with corresponding conditions?
-- all 26 states
WITH conditioned_plots AS (
  SELECT east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 
  FROM east_us_plot 
  INNER JOIN east_us_cond
  ON east_us_plot.statecd = east_us_cond.statecd AND east_us_plot.countycd = east_us_cond.countycd AND east_us_plot.plot = east_us_cond.plot
  GROUP BY east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 
)
SELECT statecd FROM conditioned_plots GROUP BY statecd


-- how many plots have values for TRTCD1?
-- 122,109 plots (a bit less than half of them)
SELECT east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 
FROM east_us_plot 
INNER JOIN east_us_cond
ON east_us_plot.statecd = east_us_cond.statecd AND east_us_plot.countycd = east_us_cond.countycd AND east_us_plot.plot = east_us_cond.plot
WHERE trtcd1 IS NOT NULL
GROUP BY east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 


-- what states have values for TRTCD1?
-- all 26 of them!
WITH trtcd_plots AS (
  SELECT east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 
  FROM east_us_plot 
  INNER JOIN east_us_cond
  ON east_us_plot.statecd = east_us_cond.statecd AND east_us_plot.countycd = east_us_cond.countycd AND east_us_plot.plot = east_us_cond.plot
  WHERE trtcd1 IS NOT NULL
  GROUP BY east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 
)
SELECT statecd FROM trtcd_plots GROUP BY statecd


-- how many plots have values for trtcd1_p2a?
-- None of them!
SELECT east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 
FROM east_us_plot 
INNER JOIN east_us_cond
ON east_us_plot.statecd = east_us_cond.statecd AND east_us_plot.countycd = east_us_cond.countycd AND east_us_plot.plot = east_us_cond.plot
WHERE trtcd1_p2a IS NOT NULL
GROUP BY east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 




-- how many plots have values for HARVEST_TYPE1_SRS?
-- 36,727 plots
SELECT east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 
FROM east_us_plot 
INNER JOIN east_us_cond
ON east_us_plot.statecd = east_us_cond.statecd AND east_us_plot.countycd = east_us_cond.countycd AND east_us_plot.plot = east_us_cond.plot
WHERE HARVEST_TYPE1_SRS IS NOT NULL
GROUP BY east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 


-- what states have values for HARVEST_TYPE1_SRS?
-- 6 states: NC, MS, KY, FL, VA, GA, SC, TN, AL
WITH harvest_plots AS (
  SELECT east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 
  FROM east_us_plot 
  INNER JOIN east_us_cond
  ON east_us_plot.statecd = east_us_cond.statecd AND east_us_plot.countycd = east_us_cond.countycd AND east_us_plot.plot = east_us_cond.plot
  WHERE HARVEST_TYPE1_SRS IS NOT NULL
  GROUP BY east_us_plot.statecd, east_us_plot.countycd, east_us_plot.plot 
)
SELECT state_name 
FROM harvest_plots 
JOIN east_us_counties
ON harvest_plots.statecd = east_us_counties.statecd
GROUP BY state_name


-- how many trees are observed more than once? (based on the natural key without year)
-- 4993 out of 12075 trees, or about 41%
WITH counting AS (
  SELECT statecd, unitcd, countycd, plot, subp, tree, COUNT(invyr) AS num_obs 
  FROM ri_tree
  GROUP BY statecd, unitcd, countycd, plot, subp, tree 
  ORDER BY COUNT(invyr) DESC
)
SELECT * 
FROM counting
WHERE num_obs > 1


-- when a tree is observed more than once, how long elapses between the first and last observation?
-- 4-17 years
WITH counting AS (
  SELECT statecd, unitcd, countycd, plot, subp, tree, COUNT(invyr) AS num_obs, MIN(invyr), MAX(invyr), MAX(invyr) - MIN(invyr) AS time_elapsed
  FROM ri_tree
  GROUP BY statecd, unitcd, countycd, plot, subp, tree 
)
SELECT * 
FROM counting
WHERE num_obs > 1
ORDER BY time_elapsed


-- How many trees have a prev_tre_cn?
-- 8,141 out of 20,909 trees
SELECT statecd, unitcd, countycd, plot, subp, tree, invyr, prev_tre_cn
FROM ri_tree
WHERE prev_tre_cn IS NOT NULL


-- Are there duplicate values of prev_tre_cn?
-- no.
SELECT prev_tre_cn, COUNT(prev_tre_cn)
FROM ri_tree
GROUP BY prev_tre_cn
ORDER BY count DESC

-- Do trees ever have a prev_tre_cn that matches their current cn?
-- no.
SELECT cn, prev_tre_cn 
FROM ri_tree
WHERE cn = prev_tre_cn


-- Can we locate cn's that match prev_tre_cn's?
-- yes. all of them.
SELECT cn FROM ri_tree WHERE cn IN (
	SELECT prev_tre_cn FROM ri_tree
)

-- Are cn's that match prev_tre_cn's actually the same tree (as defined by the natural key minus year)?
-- yes. see prev_cn_checker.py for definitive answer.
SELECT prev_tre_cn FROM ri_tree WHERE prev_tre_cn IS NOT NULL
	-- grabbed prev_tre_cn 62271032010538
SELECT statecd, unitcd, countycd, plot, subp, tree FROM ri_tree WHERE prev_tre_cn = 62271032010538
	-- results: 44	1	7	35	3	8
SELECT statecd, unitcd, countycd, plot, subp, tree FROM ri_tree WHERE cn = 62271032010538
	-- results: 44	1	7	35	3	8

SELECT prev_tre_cn FROM ri_tree WHERE prev_tre_cn IS NOT NULL
	-- grabbed prev_tre_cn 55943131010538
SELECT statecd, unitcd, countycd, plot, subp, tree FROM ri_tree WHERE prev_tre_cn = 55943131010538
	-- results: 44	1	7	77	3	2
SELECT statecd, unitcd, countycd, plot, subp, tree FROM ri_tree WHERE cn = 55943131010538
	-- results: 44	1	7	77	3	2


-- show trees that are observed more than once, but don't have prev_tre_cn

WITH counting AS (
  SELECT statecd, unitcd, countycd, plot, subp, tree, COUNT(invyr) AS num_obs 
  FROM ri_tree
  WHERE prev_tre_cn IS NULL
  GROUP BY statecd, unitcd, countycd, plot, subp, tree 
  ORDER BY COUNT(invyr) DESC
)
SELECT * 
FROM counting
WHERE num_obs > 1
