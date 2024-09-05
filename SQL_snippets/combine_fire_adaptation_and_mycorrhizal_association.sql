CREATE TABLE a_temp AS (
  SELECT 
  	fire_adaptation.spcd, 
  	fire_adaptation.common_name,
  	fire_adaptation.genus, 
  	fire_adaptation.species, 
  	fire_adaptation.basal_area, 
  	fire_adaptation.fire_classification, 
  	fire_adaptation.source AS f_adapt_source, 
  	ref_species.association, 
  	mycorrhiza_mkt.source AS myco_source
  FROM fire_adaptation
  JOIN ref_species 
  ON fire_adaptation.spcd = ref_species.spcd
  LEFT JOIN mycorrhiza_mkt
  ON fire_adaptation.spcd = mycorrhiza_mkt.spcd
)

UPDATE a_temp
SET myco_source = 'Brundrett & Tedersoo, 2020'
FROM mycorrhiza_brundrett_tedersoo
WHERE 
	myco_source IS NULL 
	AND a_temp.genus = mycorrhiza_brundrett_tedersoo.genus
	AND a_temp.association = mycorrhiza_brundrett_tedersoo.mycorrhiza
