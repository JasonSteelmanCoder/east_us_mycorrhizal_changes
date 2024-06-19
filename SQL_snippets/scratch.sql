COALESCE(
    round(
        ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') 
        + 
        COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0)) 
        / 
        ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') 
        + 
        (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') 
        + 
        COALESCE((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM'), 0))::DECIMAL
        
        , 2
    ), 
    CASE 
        WHEN 
            ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL 
            AND 
            (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NOT NULL) 
            THEN 0 
        WHEN 
            ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NULL 
            AND 
            (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL) 
            THEN NULL 
        ELSE 1 
    END
) AS am_dominance_t1,





SELECT statecd, COUNT(countycd) AS counties 
FROM fire_frequency 
WHERE burnedplots = 0
GROUP BY statecd
ORDER BY counties DESC; 

SELECT COUNT(countycd) 
FROM fire_frequency
WHERE statecd = 55;


