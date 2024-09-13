        WITH trees AS (
            SELECT 
                east_us_tree.statecd AS statecd,
                east_us_tree.countycd AS countycd,
                east_us_tree.spcd AS spcd,
                fire_classification,
                ROUND(((PI() * (east_us_tree.dia::DECIMAL * 2.54 / 2) ^ 2) / 10000)::DECIMAL, 2) AS basal_area,
                ref_species.association
            FROM east_us_tree
            LEFT JOIN fire_adaptation
                ON east_us_tree.spcd = fire_adaptation.spcd
            LEFT JOIN ref_species
            ON ref_species.spcd = east_us_tree.spcd
            WHERE 
                east_us_tree.statecd = {statecd} 
                AND east_us_tree.countycd = {countycd}
        )
        SELECT 
            trees.statecd, 
        trees.countycd,
            COALESCE(SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END), 0) AS adapted_area,
            COALESCE(SUM(CASE WHEN fire_classification = 'intolerant' THEN basal_area END), 0) AS intolerant_area,
            -- note that pct_adapted is the percent of trees belonging to the 75 selected species that are adapted
            ROUND(COALESCE(SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END), 0) / (COALESCE(SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END), 0) + COALESCE(SUM(CASE WHEN fire_classification = 'intolerant' THEN basal_area END), 0)) * 100, 1) AS pct_adapted,
            COALESCE(SUM(CASE WHEN fire_classification IS NULL THEN basal_area END), 0) AS excluded_bas_area,  
            ROUND((SUM(CASE WHEN fire_classification IS NULL THEN basal_area END) / (SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END) + SUM(CASE WHEN fire_classification = 'intolerant' THEN basal_area END) + SUM(CASE WHEN fire_classification IS NULL THEN basal_area END))) * 100, 2) AS pct_area_excluded,
            ROUND(COALESCE(SUM(CASE WHEN association = 'AM' AND fire_classification IS NOT NULL THEN basal_area END), 0) + 0.5 * COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0), 2) AS am_area,
            ROUND(COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0) + 0.5 * COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0), 2) AS em_area,
            -- note that pct_em is the percent of trees belonging to the 75 selected species that are Ectomycorrhizal
            ROUND(((COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0) + (0.5 * COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0))) / (COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0) + COALESCE(SUM(CASE WHEN association = 'AM' AND fire_classification IS NOT NULL THEN basal_area END), 0) + COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0))) * 100, 1) AS pct_em,
            -- not_counted_area is the basal area of trees that are not part of the 75 species, plus ericoid sourwood trees
            COALESCE(SUM(CASE WHEN fire_classification IS NULL OR (association != 'AM' AND association != 'EM' AND association != 'AM-EM') THEN basal_area END), 0) AS not_counted_area,
            -- pct_not_counted is the not_counted_area as a percent of the total basal area in the county, including all species, association types, and fire adaptation types
            ROUND((COALESCE(SUM(CASE WHEN fire_classification IS NULL OR (association != 'AM' AND association != 'EM' AND association != 'AM-EM') THEN basal_area END), 0) / (COALESCE(SUM(CASE WHEN fire_classification IS NULL OR (association != 'AM' AND association != 'EM' AND association != 'AM-EM') THEN basal_area END), 0) + ROUND(COALESCE(SUM(CASE WHEN association = 'AM' AND fire_classification IS NOT NULL THEN basal_area END), 0), 2) + ROUND(COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0), 2) + COALESCE(ROUND(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 2), 0))) * 100 , 2) AS pct_not_counted,
            east_us_region.region_id AS region
        FROM trees
        LEFT JOIN east_us_region
        ON east_us_region.statecd = trees.statecd AND east_us_region.countycd = trees.countycd  
        GROUP BY trees.statecd, trees.countycd, east_us_region.region_id;