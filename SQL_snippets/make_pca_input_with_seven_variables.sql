SELECT 
	fire_characteristics.scientific_name, 
  necn_characteristics.common_name, 
  necn_characteristics.foliagelittercn, 
  fire_characteristics.mean_litter_cn, 
  ROUND(necn_characteristics.foliagelittercn::decimal / fire_characteristics.mean_litter_cn::decimal, 2) AS factor, 
  fire_characteristics.mean_litter_cn_source
FROM necn_characteristics
INNER JOIN fire_characteristics
ON LOWER(TRIM(BOTH ' ' FROM necn_characteristics.common_name)) = LOWER(TRIM(BOTH ' ' FROM fire_characteristics.common_name))
