ROUND((SUM(CASE WHEN fire_classification IS NULL THEN basal_area END) 

/ 

(SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END) 
+ SUM(CASE WHEN fire_classification = 'intolerant' THEN basal_area END) 
+ SUM(CASE WHEN fire_classification IS NULL THEN basal_area END))) 

* 100, 2) 

AS pct_area_excluded,