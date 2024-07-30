SELECT 
	CASE 
  	WHEN species = 'MKH' THEN 'Carya tomentosa'
    WHEN species = 'SRO' THEN 'Quercus falcata'
    WHEN species = 'WO' THEN 'Quercus alba'
    WHEN species = 'MPL' THEN 'Acer rubrum'
    WHEN species = 'WE' THEN 'Ulmus alata'
  END AS scientific_name, 
  AVG(dbh_cm * 10) AS dbh_mm, 
  AVG(thick_mm) AS thick_mm,
  (AVG(thick_mm)) / (AVG(dbh_cm * 10)) AS bark_diameter_ratio
FROM siegert_bark_thickness
GROUP BY species