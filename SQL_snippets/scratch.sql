    WITH 
    combos AS (
          -- find all combinations of counties and ecoregions (ecoregions are displayed as booleans for whether they equal epi-endogeic)
          SELECT 
              east_us_counties.statecd, 
              east_us_counties.countycd, 
              ecological_groups.ecological_group,
              COALESCE(ecological_groups.ecological_group = 'Epi-Endogeic', false) AS is_epiendogeic_row
          FROM east_us_counties
          LEFT JOIN worms_drake 
          ON east_us_counties.statecd = worms_drake.statecd AND east_us_counties.countycd = worms_drake.countycd
      		LEFT JOIN chang_fips
      		ON chang_fips.statecd = east_us_counties.statecd AND chang_fips.countycd = east_us_counties.countycd
          LEFT JOIN ecological_groups
          ON 
      			(ecological_groups.family = worms_drake.family AND ecological_groups.name = worms_drake.name) 
      			OR (ecological_groups.species = chang_fips.species)
          GROUP BY east_us_counties.statecd, east_us_counties.countycd, ecological_groups.ecological_group
          ORDER BY east_us_counties.statecd, east_us_counties.countycd, ecological_groups.ecological_group
    )
    SELECT statecd, countycd, BOOL_OR(is_epiendogeic_row) AS has_epiendogeic
    FROM combos
    GROUP BY statecd, countycd
    ORDER BY statecd, countycd;
    
    