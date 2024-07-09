    WITH 
    combos AS (
        WITH 
        phillips_locations AS (
            SELECT phillips_sites_fips.site_name, originalspeciesbinomial, speciesbinomial, phillips_sites_fips.statecd, phillips_sites_fips.countycd
            FROM phillips_sites_fips
            LEFT JOIN worm_sp_occur_phillips 
            ON phillips_sites_fips.site_name = worm_sp_occur_phillips.site_name
-- check that this where clause makes sense after rejig
            WHERE worm_sp_occur_phillips.native = 'Non-native'
        ), 
      	drake_combined AS (
        	SELECT worms_drake.family, worms_drake.genus, worms_drake.species, worms_drake.name, worms_drake.origin, worms_drake.source, worms_drake.statecd, worms_drake.countycd, drake_nativeness.native_to_east_us
            FROM worms_drake
            LEFT JOIN drake_nativeness
            ON LOWER(TRIM(BOTH ' ' FROM worms_drake.name)) = LOWER(TRIM(BOTH ' ' FROM drake_nativeness.name))
        )
        -- find all combinations of counties and ecoregions (ecoregions are displayed as booleans for whether they equal epi-endogeic)
        SELECT 
            east_us_counties.statecd, 
            east_us_counties.countycd, 
            ecological_groups.ecological_group,
            COALESCE(ecological_groups.ecological_group = 'Epi-Endogeic', false) AS is_epiendogeic_row
        FROM east_us_counties
        LEFT JOIN drake_combined 
        ON 
            (
                drake_combined.origin != 'Nearctic' 
                OR  drake_combined.native_to_east_us = 'FALSE'      -- for worms native to the Nearctic, but not specifically the eastern US
            )
            AND east_us_counties.statecd = drake_combined.statecd AND east_us_counties.countycd = drake_combined.countycd
        LEFT JOIN chang_fips
        ON chang_fips.statecd = east_us_counties.statecd AND chang_fips.countycd = east_us_counties.countycd
        LEFT JOIN phillips_locations
        ON phillips_locations.statecd = east_us_counties.statecd AND phillips_locations.countycd = east_us_counties.countycd
        LEFT JOIN ecological_groups
        ON 
            (ecological_groups.family = drake_combined.family AND ecological_groups.name = drake_combined.name) 
            OR (ecological_groups.species = chang_fips.species)
            OR (LOWER(REGEXP_REPLACE(phillips_locations.speciesbinomial, '.*\s', '')) = LOWER(ecological_groups.species))
        GROUP BY east_us_counties.statecd, east_us_counties.countycd, ecological_groups.ecological_group
        ORDER BY east_us_counties.statecd, east_us_counties.countycd, ecological_groups.ecological_group
    )
    SELECT statecd, countycd, BOOL_OR(is_epiendogeic_row) AS has_epiendogeic
    FROM combos
    GROUP BY statecd, countycd
    ORDER BY statecd, countycd;
    