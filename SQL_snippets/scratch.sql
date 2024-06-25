ROUND(
    (
        (
            SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END) 
            
            + 
            
            (
                0.5 
                
                * 
                
                COALESCE(
                    
                    SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END)
                    
                    , 
                    
                    0)
                
            ) 
        )

        / 
        
        (
            SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END) 
            
            + 
            
            SUM(CASE WHEN association = 'AM' AND fire_classification IS NOT NULL THEN basal_area END) 
            
            + 
            
            SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END)
            
        ) 
    )

    * 
    
    100
    
, 1) AS pct_em,