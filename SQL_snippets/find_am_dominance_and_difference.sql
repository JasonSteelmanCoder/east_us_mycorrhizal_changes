        WITH t1 
        AS (
            WITH association_basal_areas
            AS (
                WITH county_trees
                AS (
                    SELECT east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.invyr, tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 2) as basal_area, east_us_tree.spcd, ref_species.association
                    FROM east_us_tree 
                    LEFT JOIN ref_species
                    ON east_us_tree.spcd = ref_species.spcd
                    LEFT JOIN east_us_cond
                    ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot
                    WHERE 

                    east_us_tree.invyr > 1979 AND east_us_tree.invyr < 1999 AND										-- at T1

                    east_us_tree.statecd = {statecd} AND  
                    east_us_tree.unitcd = {unitcd} AND
                    east_us_tree.countycd = {countycd} AND 
                    
                    (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland
                    east_us_tree.statuscd = 1			-- only count live trees

                    ORDER BY association ASC
                )
                SELECT association, SUM(basal_area) AS basal_area_for_county
                FROM county_trees
                GROUP BY association
            )
            SELECT  
            sum(basal_area_for_county) AS total_basal_area_t1,
            (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2) AS am_basal_area_t1,
            (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2) AS em_basal_area_t1,
            COALESCE(round((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2) / ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM'))::decimal, 2), CASE WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NOT NULL) THEN 0 WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NULL AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL) THEN NULL ELSE 1 END) AS am_dominance_t1,
            ROW_NUMBER() OVER() AS rownum
            FROM association_basal_areas
        ), 

        t2 AS (
            WITH association_basal_areas
            AS (
                WITH county_trees
                    AS (
                    SELECT east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.invyr, tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 2) as basal_area, east_us_tree.spcd, ref_species.association
                    FROM east_us_tree 
                    LEFT JOIN ref_species
                    ON east_us_tree.spcd = ref_species.spcd
                    LEFT JOIN east_us_cond
                    ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot

                    WHERE 

                    east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2023 AND									-- at T2

                    east_us_tree.statecd = {statecd} AND  
                    east_us_tree.unitcd = {unitcd} AND
                    east_us_tree.countycd = {countycd} AND

                    (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland            
                    east_us_tree.statuscd = 1			-- only count live trees            

                    ORDER BY association ASC
                )
                SELECT association, SUM(basal_area) AS basal_area_for_county
                FROM county_trees
                GROUP BY association
            )
            SELECT  
            sum(basal_area_for_county) AS total_trees_t2,
            (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2) AS am_basal_area_t2,
            (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2) AS em_basal_area_t2,
            COALESCE(round((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2) / ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM'))::decimal, 2), CASE WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NOT NULL) THEN 0 WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NULL AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL) THEN NULL ELSE 1 END) AS am_dominance_t2,
            ROW_NUMBER() OVER() AS rownum
            FROM association_basal_areas
        )
        SELECT 
            total_basal_area_t1, 
            am_basal_area_t1, 
            em_basal_area_t1, 
            am_dominance_t1, 
            total_trees_t2, 
            am_basal_area_t2, 
            em_basal_area_t2, 
            am_dominance_t2,
            round(am_dominance_t2::decimal - am_dominance_t1::decimal, 2) difference_in_am_dominance
        FROM t1
        LEFT JOIN t2
        ON true;