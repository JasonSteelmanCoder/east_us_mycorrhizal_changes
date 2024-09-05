
ROUND(((COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0) 
+ 
(0.5 * COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0))) 

/ 

(COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0) 
+ 
COALESCE(SUM(CASE WHEN association = 'AM' AND fire_classification IS NOT NULL THEN basal_area END), 0) 
+ 
COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0))) 

* 100, 1) 

AS pct_em,

