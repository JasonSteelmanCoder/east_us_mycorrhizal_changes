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



