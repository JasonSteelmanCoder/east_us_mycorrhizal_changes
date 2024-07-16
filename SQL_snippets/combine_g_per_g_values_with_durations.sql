-- view the data for Cornelissen, neatly arranged
SELECT * 
FROM new_try_data 
WHERE reference LIKE 'Cornelissen%'
ORDER BY observationid, dataid

-- combine measurements with durations for Cornelissen data
WITH 
durations AS (
  SELECT accspeciesname, observationid, origlname, origvaluestr, comment 
  FROM new_try_data 
  WHERE 
    reference LIKE 'Cornelissen%'
    AND origlname = 'length of decomp period'
  ORDER BY observationid, dataid
), 
measurements AS (  
  SELECT speciesname, observationid, origlname, origvaluestr, origunitstr 
  FROM new_try_data
  WHERE 
    reference LIKE 'Cornelissen%'
    AND origlname LIKE 'PROPORTION%'
  ORDER BY observationid, dataid
)
SELECT measurements.speciesname, measurements.observationid, measurements.origvaluestr AS proportion_mass_loss, measurements.origunitstr, durations.origvaluestr AS length_decomp_days 
FROM measurements
LEFT JOIN durations 
ON durations.observationid = measurements.observationid

-- combine measurements with durations for Quested data
WITH 
durations AS (
	SELECT speciesname, observationid, obsdataid, origlname, origvaluestr 
  FROM new_try_data 
  WHERE 
    reference LIKE 'Quested%' 
    AND origlname = 'length of decomp period'
  ORDER BY observationid
),
ks AS (
  SELECT speciesname, observationid, obsdataid, origlname, origvaluestr, origunitstr 
  FROM new_try_data 
  WHERE 
    reference LIKE 'Quested%' 
    AND origlname LIKE 'PROPORTION%'
  ORDER BY observationid
)
SELECT durations.speciesname, durations.observationid, durations.origvaluestr AS length_decomp_days, ks.origvaluestr AS proportion_mass_loss, ks.origunitstr 
FROM durations
LEFT JOIN ks
ON durations.observationid = ks.observationid