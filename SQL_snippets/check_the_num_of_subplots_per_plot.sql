-- FIND HOW MANY PLOTS HAVE EACH NUMBER OF SUBPLOTS
WITH count_of_subplots AS (
  WITH subplots AS (
    -- grab each of the subplots in the east US
    SELECT statecd, unitcd, countycd, plot, subp 
    FROM east_us_tree 
    GROUP BY statecd, unitcd, countycd, plot, subp 
    ORDER BY statecd, unitcd, countycd, plot, subp
  )
  -- grab each plot with its count of subplots
  SELECT statecd, unitcd, countycd, plot, COUNT(subp) AS num_subplots
  FROM subplots 
  GROUP BY statecd, unitcd, countycd, plot
  ORDER BY num_subplots DESC
)
-- grab each number of subplots with the count of plots that have that number
SELECT num_subplots, COUNT(num_subplots) AS plots_with_this_num_subplots
FROM count_of_subplots
GROUP BY num_subplots
ORDER BY num_subplots





-- EXAMINE AN INDIVIDUAL PLOT
SELECT * FROM east_us_plot WHERE statecd = 13 AND unitcd = 1 AND countycd = 39 AND plot = '90025'