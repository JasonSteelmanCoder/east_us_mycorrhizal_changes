SELECT traitname, COUNT(traitname) FROM old_try_data_2 GROUP BY traitname

SELECT traitname, origunitstr FROM old_try_data_2 GROUP BY origunitstr, traitname

SELECT dataname, COUNT(dataname) FROM old_try_data_2 GROUP BY dataname;

SELECT accspeciesname FROM old_try_data_2 WHERE dataname = 'Leaf Litter decomposition: decomposition rate constant k value: single exponential model: Yt=Yoe-kt' GROUP BY accspeciesname





WITH 
limited_trees AS (
	SELECT * FROM common_trees ORDER BY basal_area DESC LIMIT 70
)
SELECT rank_by_basal_area, spcd common_name, genus, species, accspeciesname, origvaluestr
FROM limited_trees
INNER JOIN old_try_data_2
ON 
    dataname = 'Leaf Litter decomposition: decomposition rate constant k value: single exponential model: Yt=Yoe-kt'
  AND LOWER(TRIM(REGEXP_REPLACE(accspeciesname, '^(([^ ]+ ){2}).*$', '\1'))) = LOWER(TRIM(genus || ' ' || species))
  
