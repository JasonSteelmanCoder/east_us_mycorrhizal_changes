-- find if there are invasive species at all in each county
SELECT east_us_plot.statecd, east_us_plot.countycd, count(DISTINCT ecological_groups.ecological_group) > 0 AS has_invasives
FROM east_us_plot
LEFT JOIN worms_drake 
ON east_us_plot.statecd = worms_drake.statecd AND east_us_plot.countycd = worms_drake.countycd
LEFT JOIN ecological_groups
ON ecological_groups.family = worms_drake.family AND ecological_groups.name = worms_drake.name
GROUP BY east_us_plot.statecd, east_us_plot.countycd
ORDER BY has_invasives;



-- find if there are EPIGEIC invasive species in each county
WITH 
combos AS (
  -- find all combinations of counties and ecoregions (ecoregions are displayed as booleans for whether they equal epigeic)
  SELECT 
    east_us_plot.statecd, 
    east_us_plot.countycd, 
    COALESCE(ecological_groups.ecological_group = 'Epigeic', false) AS is_epigeic_row
  FROM east_us_plot
  LEFT JOIN worms_drake 
  ON east_us_plot.statecd = worms_drake.statecd AND east_us_plot.countycd = worms_drake.countycd
  LEFT JOIN ecological_groups
  ON ecological_groups.family = worms_drake.family AND ecological_groups.name = worms_drake.name
  GROUP BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
  ORDER BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
)
SELECT statecd, countycd, BOOL_OR(is_epigeic_row) AS has_epigeic
FROM combos
GROUP BY statecd, countycd
ORDER BY statecd, countycd;


-- find if there are ANECIC invasive species in each county
WITH 
combos AS (
  -- find all combinations of counties and ecoregions (ecoregions are displayed as booleans for whether they equal anecic)
  SELECT 
    east_us_plot.statecd, 
    east_us_plot.countycd, 
  	ecological_groups.ecological_group,
    COALESCE(ecological_groups.ecological_group = 'Anecic', false) AS is_anecic_row
  FROM east_us_plot
  LEFT JOIN worms_drake 
  ON east_us_plot.statecd = worms_drake.statecd AND east_us_plot.countycd = worms_drake.countycd
  LEFT JOIN ecological_groups
  ON ecological_groups.family = worms_drake.family AND ecological_groups.name = worms_drake.name
  GROUP BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
  ORDER BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
)
SELECT statecd, countycd, BOOL_OR(is_anecic_row) AS has_anecic
FROM combos
GROUP BY statecd, countycd
ORDER BY statecd, countycd;


-- find if there are ENDOGEIC invasive species in each county
WITH 
combos AS (
  -- find all combinations of counties and ecoregions (ecoregions are displayed as booleans for whether they equal endogeic)
  SELECT 
    east_us_plot.statecd, 
    east_us_plot.countycd, 
    COALESCE(ecological_groups.ecological_group = 'Endogeic', false) AS is_endogeic_row
  FROM east_us_plot
  LEFT JOIN worms_drake 
  ON east_us_plot.statecd = worms_drake.statecd AND east_us_plot.countycd = worms_drake.countycd
  LEFT JOIN ecological_groups
  ON ecological_groups.family = worms_drake.family AND ecological_groups.name = worms_drake.name
  GROUP BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
  ORDER BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
)
SELECT statecd, countycd, BOOL_OR(is_endogeic_row) AS has_endogeic
FROM combos
GROUP BY statecd, countycd
ORDER BY statecd, countycd;



-- find if there are EPI-ENDOGEIC invasive species in each county
WITH 
combos AS (
  -- find all combinations of counties and ecoregions (ecoregions are displayed as booleans for whether they equal epi-endogeic)
  SELECT 
    east_us_plot.statecd, 
    east_us_plot.countycd, 
  	ecological_groups.ecological_group,
    COALESCE(ecological_groups.ecological_group = 'Epi-Endogeic', false) AS is_epiendogeic_row
  FROM east_us_plot
  LEFT JOIN worms_drake 
  ON east_us_plot.statecd = worms_drake.statecd AND east_us_plot.countycd = worms_drake.countycd
  LEFT JOIN ecological_groups
  ON ecological_groups.family = worms_drake.family AND ecological_groups.name = worms_drake.name
  GROUP BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
  ORDER BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
)
SELECT statecd, countycd, BOOL_OR(is_epiendogeic_row) AS has_epiendogeic
FROM combos
GROUP BY statecd, countycd
ORDER BY statecd, countycd;