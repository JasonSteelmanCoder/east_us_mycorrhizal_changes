-- show all rows that measure traits
SELECT * FROM new_try_data WHERE traitid IS NOT NULL 

-- show all traits
SELECT traitname FROM new_try_data GROUP BY traitname

-- show all trait ids
SELECT traitid FROM new_try_data GROUP BY traitid




-- how many species have data for litter decomposition (963)
SELECT accspeciesid FROM new_try_data WHERE traitid = 39 GROUP BY accspeciesid

-- how many species have c/n? (176)
SELECT accspeciesid FROM new_try_data WHERE traitid = 150 GROUP BY accspeciesid

-- how many species have bark thickness per stem diameter (119)
SELECT accspeciesid FROM new_try_data WHERE traitid = 839 GROUP BY accspeciesid




-- which value should we use for litter decomp? (origvaluestr)
SELECT origvaluestr, stdvalue, stdvaluestr 
FROM new_try_data 
WHERE 
	traitid = 39 
  AND stdvaluestr IS NOT NULL
GROUP BY origvaluestr, stdvalue, stdvaluestr

-- which value should we use for c/n? (origvaluestr)
SELECT origvaluestr, stdvalue, stdvaluestr 
FROM new_try_data 
WHERE 
	traitid = 150 
  AND stdvalue IS NOT NULL
  AND stdvalue::text != origvaluestr
GROUP BY origvaluestr, stdvalue, stdvaluestr

-- which value should we use for bark thickness per stem diameter? (origvaluestr)
SELECT origvaluestr, stdvalue, stdvaluestr 
FROM new_try_data 
WHERE 
	traitid = 839 
    AND stdvalue IS NOT NULL
GROUP BY origvaluestr, stdvalue, stdvaluestr



-- are origvaluestr's all in the same units for litter decomp? (no! there are several)
SELECT origunitstr, COUNT(origunitstr) AS frequency FROM new_try_data WHERE traitid = 39 GROUP BY origunitstr ORDER BY frequency DESC

-- are origvaluestr's all in the same units for c/n? (not quite, but it doesn't matter, because it's a ratio)
SELECT origunitstr, COUNT(origunitstr) AS frequency FROM new_try_data WHERE traitid = 150 GROUP BY origunitstr ORDER BY frequency DESC

-- are origvaluestr's all in the same units for bark thickness per stem diameter? (no! some are percent and some are ratio)
SELECT origunitstr, COUNT(origunitstr) AS frequency FROM new_try_data WHERE traitid = 839 GROUP BY origunitstr ORDER BY frequency DESC


-- get a feel for what data we have for an individual species
SELECT * FROM new_try_data WHERE traitid IS NOT NULL AND accspeciesid = 859

SELECT * FROM new_try_data WHERE traitid IS NOT NULL AND accspeciesid = 33707

SELECT * FROM new_try_data WHERE traitid IS NOT NULL AND accspeciesid = 45431
