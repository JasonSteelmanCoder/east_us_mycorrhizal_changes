SELECT * FROM east_us_percents_and_ratios WHERE 
	tot_bas_t1 != 'None' AND 
  ambasar_t1 != 'None' AND 
  embasar_t1 != 'None' AND  
  am_dom_t1 != 'None' AND 
  tot_bas_t2 != 'None' AND 
  ambasar_t2 != 'None' AND (
    embasar_t2 = 'None' OR 
    am_dom_t2 = 'None' OR 
    dif_am_dom = 'None'
	)
-- ORDER BY tot_bas_t1, ambasar_t1, am_dom_t1, tot_bas_t2, ambasar_t2, embasar_t2, am_dom_t2, dif_am_dom DESC
ORDER BY ambasar_t2 DESC
;



SELECT * FROM east_us_percents_and_ratios WHERE 
		tot_bas_t1 = 'None' OR 
  	ambasar_t1 = 'None' OR 
  	embasar_t1 = 'None' OR  
  	am_dom_t1 = 'None' OR 
  	tot_bas_t2 = 'None' OR 
  	ambasar_t2 = 'None' OR
    embasar_t2 = 'None' OR 
    am_dom_t2 = 'None' OR 
    dif_am_dom = 'None'
-- ORDER BY tot_bas_t1, ambasar_t1, am_dom_t1, tot_bas_t2, ambasar_t2, embasar_t2, am_dom_t2, dif_am_dom DESC
ORDER BY ambasar_t2 DESC
;