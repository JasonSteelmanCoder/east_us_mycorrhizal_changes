COALESCE(
    
    round(
        (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') / ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM'))::decimal
        , 2
    ), 
    
    CASE 
        WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL 
        AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NOT NULL) 
        THEN 0 
        WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NULL 
        AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL) 
        THEN NULL 
        ELSE 1 
        END

) AS am_dominance_t2,




COALESCE(
    
    round(
        (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') / ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM'))::decimal
        , 2
    ), 
    
    CASE 
        WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL 
        AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NOT NULL) 
        THEN 0 
        WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NULL 
        AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL) 
        THEN NULL 
        ELSE 1 
        END

) AS am_dominance_t2,